"""Model Fix Processor

OpenTelemetry span processor that repairs missing or incorrect
gen_ai attributes on AI model spans before export. It does three things:

- Detects the provider (OpenAI, Azure, OpenRouter, Ollama, AWS, etc.) using
    model prefixes, span name heuristics and endpoint URL patterns.
- Ensures `gen_ai.provider.name` is set (and preserves `gen_ai.system` for
    backwards compatibility when present).
- Normalizes/fills `gen_ai.request.model`, `gen_ai.response.model` and token
    usage attributes (including legacy token keys) using provider-specific
    fallbacks and JSON extraction where necessary.

Design notes:
- The processor prefers the new semantic `gen_ai.provider.name` but will read
    and maintain `gen_ai.system` to remain compatible with older instrumentation.
- Full model identifiers (region prefixes, dates, version suffixes) are
    preserved when available to avoid losing pricing/version semantics.
"""

import os
import logging
from collections import deque
from typing import Tuple, Optional, Any, Set, Dict
from opentelemetry.sdk.trace import SpanProcessor, ReadableSpan
from .helpers import safe_extract_nested

logger = logging.getLogger(__name__)

# ---- Provider Registry -------------------------------------------------

# Comprehensive registry of all supported AI providers with their detection patterns
PROVIDER_REGISTRY = {
    "openai": {
        "provider_name": "OpenAI",
        "span_name_patterns": ["openai"],  # Matches: openai.chat, openai.response, ChatOpenAI.chat, etc.
        "endpoint_keywords": [],  
        "model_prefixes": [],
        "default_port": None,
    },
    "azure": {
        "provider_name": "Azure",
        "span_name_patterns": ["azure"],  # Matches: AzureOpenAI.workflow, AzureChatOpenAI.chat, etc.
        "endpoint_keywords": ["azure"],
        "model_prefixes": [],
        "default_port": None,
    },
    "openrouter": {
        "provider_name": "OpenRouter",
        "span_name_patterns": ["openrouter"],  # Matches: OpenRouter.task, etc.
        "endpoint_keywords": ["openrouter"],
        "model_prefixes": [
            "google/", "anthropic/", "openai/", "meta-llama/", "meta/", "microsoft/",
            "mistralai/", "cohere/", "ai21/", "huggingfaceh4/", "teknium/",
            "nousresearch/", "openchat/", "codellama/", "phind/", "wizardlm/",
            "upstage/", "01-ai/", "alpindale/", "austism/", "cognitivecomputations/",
            "databricks/", "deepseek/", "gryphe/", "intel/", "jondurbin/",
            "lizpreciator/", "migtissera/", "neversleep/", "undi95/", "xwin-lm/"
        ],
        "default_port": None,
    },
    "ollama": {
        "provider_name": "Ollama",
        "span_name_patterns": ["ollama"],  # Matches: ChatOllama.chat, Ollama.workflow, etc.
        "endpoint_keywords": ["ollama"],
        "model_prefixes": [],
        "default_port": 11434,
    },
    "bedrock": {
        "provider_name": "AWS",
        "span_name_patterns": ["bedrock"],  # Matches: bedrock.converse, BedrockConverse.workflow, etc.
        "endpoint_keywords": ["bedrock"],
        "model_prefixes": [],
        "default_port": None,
    },
    "anthropic": {
        "provider_name": "Anthropic",
        "span_name_patterns": ["anthropic", "claude"],  # Matches: anthropic.converse, Anthropic.workflow, etc.
        "endpoint_keywords": ["anthropic"],
        "model_prefixes": ["claude-"],
        "default_port": None,
    },
    "sagemaker": {
        "provider_name": "SageMaker",
        "span_name_patterns": ["sagemaker"],  # Matches: SageMaker.workflow, etc.
        "endpoint_keywords": ["sagemaker"],
        "model_prefixes": [],
        "default_port": None,
    },
    "cohere": {
        "provider_name": "Cohere",
        "span_name_patterns": ["cohere"],  # Matches: cohere.chat, Cohere.workflow, etc.
        "endpoint_keywords": ["cohere"],
        "model_prefixes": ["command-"],
        "default_port": None,
    },
    "google": {
        "provider_name": "Google",
        "span_name_patterns": ["gemini"],  # Matches: gemini.chat, Gemini.workflow, etc.
        "endpoint_keywords": ["generativelanguage.googleapis.com"],
        "model_prefixes": ["gemini-"],
        "default_port": None,
    },
    "vertexai": {
        "provider_name": "VertexAI",
        "span_name_patterns": ["vertexai", "vertex"],  # Matches: VertexAI.workflow, etc.
        "endpoint_keywords": ["aiplatform.googleapis.com"],
        "model_prefixes": [],
        "default_port": None,
    },
    "groq": {
        "provider_name": "Groq",
        "span_name_patterns": ["groq"],  # Matches: groq.chat, Groq.workflow, etc.
        "endpoint_keywords": ["groq"],
        "model_prefixes": [],
        "default_port": None,
    },
    "huggingface": {
        "provider_name": "HuggingFace",
        "span_name_patterns": ["huggingface"],  # Matches: HuggingFace.workflow, etc.
        "endpoint_keywords": ["huggingface"],
        "model_prefixes": [],
        "default_port": None,
    },
    "mistral": {
        "provider_name": "Mistral",
        "span_name_patterns": ["mistral"],  # Matches: mistral.chat, Mistral.workflow, etc.
        "endpoint_keywords": ["mistral"],
        "model_prefixes": ["mistral-"],
        "default_port": None,
    },
}

# Invalid/empty model values
INVALID_MODEL_VALUES = (None, "", "unknown")

# ---- Helper functions -------------------------------------------------


def _is_invalid_model(value: Optional[str]) -> bool:
    """Return True if value is None, empty or 'unknown'."""
    return value in INVALID_MODEL_VALUES

def _span_needs_fixing(attributes: dict, provider_key: Optional[str] = None) -> bool:
    """Return True if span is missing provider, models, or tokens.
    
    Args:
        attributes: Span attributes dictionary.
        provider_key: Optional pre-detected provider key to avoid re-detection.
        
    Returns:
        True when fixes are needed.
    """
    # Check provider/system
    provider_name = attributes.get("gen_ai.provider.name")
    legacy_system_name = attributes.get("gen_ai.system")
    # If both provider fields missing - needs fixing
    if not provider_name and not legacy_system_name:
        return True  # Missing provider

    # If a provider value exists but appears incorrect (e.g., legacy says 'openai'
    # but model/span indicates a different provider such as Ollama), detect the
    # provider from attributes and span name. If the detected provider doesn't
    # match the existing attribute, mark the span as needing a fix so we can
    # overwrite the incorrect provider value.
    
    # Use pre-detected provider_key
    detected_key = provider_key
    if detected_key:
        detected_name = PROVIDER_REGISTRY.get(detected_key, {}).get("provider_name")
        existing_name = provider_name or legacy_system_name
        if existing_name and detected_name and str(existing_name).lower() != str(detected_name).lower():
            return True  # Provider mismatch, needs fixing


    # Check models
    request_model = attributes.get("gen_ai.request.model")
    response_model = attributes.get("gen_ai.response.model")
    
    if _is_invalid_model(request_model) or _is_invalid_model(response_model):
        return True  # Missing or invalid model
    
    # Check for model mismatch
    if request_model and response_model and request_model != response_model:
        return True
    
    # Check for missing token attributes (all providers should track tokens)
    has_input_tokens = attributes.get("gen_ai.usage.input_tokens") not in (None, "", 0)
    has_output_tokens = attributes.get("gen_ai.usage.output_tokens") not in (None, "", 0)
    has_legacy_input = attributes.get("gen_ai.usage.prompt_tokens") not in (None, "", 0)
    has_legacy_output = attributes.get("gen_ai.usage.completion_tokens") not in (None, "", 0)
    
    if not (has_input_tokens or has_legacy_input) or not (has_output_tokens or has_legacy_output):
        return True  # Missing token data that should be present
    
    return False  # Span looks good

def _detect_provider(attributes: dict, span_name: Optional[str] = None) -> Optional[str]:
    """Detect provider using model prefixes, span name, and endpoint patterns.
    
    Priority: model prefixes > span name patterns > endpoint keywords/ports.
    
    Args:
        attributes: Span attributes dictionary.
        span_name: Optional span name for pattern matching.
        
    Returns:
        Provider key if detected, None otherwise
    """
    # Model prefixes (highest priority - handles OpenRouter-style model names)
    for model_key in ("gen_ai.request.model", "gen_ai.response.model", "traceloop.association.properties.ls_model_name"):
        model_name = attributes.get(model_key)
        if model_name:
            model_name_lower = str(model_name).lower()
            for provider_key, config in PROVIDER_REGISTRY.items():
                prefixes = config.get("model_prefixes") or []
                for prefix in prefixes:
                    if model_name_lower.startswith(prefix):
                        return provider_key

    
    # Endpoint detection (hostname, keywords, ports)
    api_base = attributes.get("gen_ai.openai.api_base", "")
    endpoint = attributes.get("server.address") or attributes.get("http.url") or api_base
    endpoint_str = str(endpoint or "").lower()
    
    if endpoint_str:
        for provider_key, config in PROVIDER_REGISTRY.items():
            # Check for endpoint keywords
            for keyword in config.get("endpoint_keywords", []):
                if keyword in endpoint_str:
                    return provider_key
            
            # Check for default port
            default_port = config.get("default_port")
            if default_port and f":{default_port}" in endpoint_str:
                return provider_key
    
    # Span name patterns with priority handling
    # Azure takes priority over OpenAI when both patterns match (e.g., "AzureChatOpenAI.chat")
    if span_name:
        span_name_lower = span_name.lower()
        
        # Check for Azure first (higher priority)
        if "azure" in span_name_lower:
            return "azure"
        
        # Then check other patterns
        for provider_key, config in PROVIDER_REGISTRY.items():
            # Skip azure since we already checked it
            if provider_key == "azure":
                continue
            for pattern in config["span_name_patterns"]:
                if pattern in span_name_lower:
                    return provider_key

    return None


class ModelFixProcessor(SpanProcessor):
    """Span processor that repairs gen_ai attributes on AI model spans.

    Detects provider, sets `gen_ai.provider.name` (preserving `gen_ai.system`
    for backward compatibility), normalizes model identifiers and fills token
    usage attributes. Uses a small LRU to avoid duplicate processing.

    Args:
        debug: Enable verbose debugging (also via OBSERVABILITY_DEBUG env var).
        max_processed_spans: LRU size for duplicate prevention (default 10000).
    """

    def __init__(self, debug: bool = False, max_processed_spans: int = 10000):
        # Track processed spans with LRU eviction to prevent unbounded memory growth
        # Using deque for O(1) append and automatic size limiting
        self._processed_spans_deque: deque = deque(maxlen=max_processed_spans)
        self._processed_spans_set: Set[Tuple[int, int]] = set()
        
        # Debug flag - check env var or use parameter
        self.debug_enabled = debug or os.getenv('OBSERVABILITY_DEBUG', '').lower() in ('1', 'true', 'yes')
        
        if self.debug_enabled:
            logger.info(f"ModelFixProcessor initialized with debug mode enabled, max_processed_spans={max_processed_spans}")
    
    def on_start(self, span: Any, parent_context=None) -> None:
        """SpanProcessor interface; no action on start.
        
        Args:
            span: Span being started.
            parent_context: Optional parent context.
        """
        pass
    
    def on_end(self, readable_span: ReadableSpan) -> None:
        """Inspect and fix gen_ai attributes when span ends.

        Skips non-LLM spans, already-processed spans, and spans needing no fixes.
        
        Args:
            readable_span: Finished span to potentially fix.
        """
        # checking if the span should be processed (also detects provider once)
        should_process, provider_key = self._should_process_span(readable_span)
        if not should_process:
            return
        
        # marking span as processed to prevent double-processing
        self._mark_span_as_processed(readable_span)
        
        # build context with all needed information (reusing cached provider_key)
        context = self._build_span_context(readable_span, provider_key)
        
        # log before processing (debug only)
        self._log_before_processing(context)
        
        # apply all fixes
        self._apply_attribute_fixes(
            readable_span=context['span'],
            span_name=context['span_name'],
            provider_key=context['provider_key'],
            provider_attr=context['provider_attr'],
            correct_provider=context['correct_provider'],
            request_model_attr=context['request_model'],
            response_model_attr=context['response_model'],
            correct_model_name=context['correct_model'],
        )
        
        # log after processing (debug only)
        self._log_after_processing(context)
    
    def _should_process_span(self, readable_span: ReadableSpan) -> tuple[bool, Optional[str]]:
        """Return True if span is an LLM span needing fixes and not yet processed.
        
        Args:
            readable_span: Span to check.
            
        Returns:
            Tuple of (should_process, provider_key) where provider_key is cached for reuse.
        """
        attributes = readable_span.attributes or {}
        
        # skip if not an LLM span
        if not any(key.startswith("gen_ai.") for key in attributes):
            if self.debug_enabled:
                logger.debug(f"Span '{readable_span.name}' is not an LLM span, skipping")
            return False, None
        
        # Detect provider once - will be reused in _build_span_context
        provider_key = _detect_provider(attributes, readable_span.name)
        
        # missing attributes or mismatched attributes
        if not _span_needs_fixing(attributes, provider_key):
            if self.debug_enabled:
                logger.debug(f"Span '{readable_span.name}' doesn't need fixing, skipping")
            return False, None
        
        # is it processed already?
        span_context_id = (readable_span.context.span_id, readable_span.context.trace_id)
        if span_context_id in self._processed_spans_set:
            if self.debug_enabled:
                logger.debug(f"Span '{readable_span.name}' already processed, skipping")
            return False, None
        
        return True, provider_key
    
    def _mark_span_as_processed(self, readable_span: ReadableSpan) -> None:
        """Mark span as processed using LRU-evicted set.
        
        Args:
            readable_span: Span to mark.
        """
        span_context_id = (readable_span.context.span_id, readable_span.context.trace_id)
        
        # Add to both deque and set
        self._processed_spans_deque.append(span_context_id)
        self._processed_spans_set.add(span_context_id)
        
        # Clean up set when deque evicts old items (deque auto-evicts at maxlen)
        if len(self._processed_spans_set) > len(self._processed_spans_deque):
            # Rebuild set from deque to match current LRU state
            self._processed_spans_set = set(self._processed_spans_deque)
    
    def _build_span_context(self, readable_span: ReadableSpan, provider_key: Optional[str] = None) -> Dict[str, Any]:
        """Build dictionary with span info for fixing.
        
        Args:
            readable_span: Span to build context for.
            provider_key: Pre-detected provider key from _should_process_span.
            
        Returns:
            Dictionary with span details.
        """
        attributes = dict(readable_span.attributes or {})
        span_name = readable_span.name
        
        # Extract current attribute values
        request_model = attributes.get("gen_ai.request.model")
        response_model = attributes.get("gen_ai.response.model")
        provider_attr = attributes.get("gen_ai.provider.name") or attributes.get("gen_ai.system")
        
        # Use the provider_key already detected in _should_process_span
        correct_model = self._get_correct_model_name(attributes, provider_key)
        correct_provider = self._get_correct_provider_from_key(provider_key)
        
        return {
            'span': readable_span,
            'span_name': span_name,
            'attributes': attributes,
            'provider_key': provider_key,
            'correct_provider': correct_provider,
            'correct_model': correct_model,
            'request_model': request_model,
            'response_model': response_model,
            'provider_attr': provider_attr,
        }
    
    def _log_before_processing(self, context: Dict[str, Any]) -> None:
        """Log span state before fixes (debug only).
        
        Args:
            context: Span context dictionary.
        """
        if not self.debug_enabled:
            return
        
        print(f"\n{'='*80}")
        print(f"[ModelFixProcessor.on_end] Processing span: {context['span_name']}")
        print(f"{'='*80}\n")
        logger.debug(f"on_end called for span: {context['span_name']}")
        
        print(f"[ModelFixProcessor] BEFORE: request={context['request_model']}, "
              f"response={context['response_model']}, provider={context['provider_attr']}")
        logger.debug(f"Attributes before fixes: request_model={context['request_model']}, "
                    f"response_model={context['response_model']}, provider={context['provider_attr']}")
    
    def _log_after_processing(self, context: Dict[str, Any]) -> None:
        """Log span state after fixes (debug only).
        
        Args:
            context: Span context dictionary.
        """
        if not self.debug_enabled:
            return
        
        final_attrs = self._get_writable_attributes(context['span'])
        if final_attrs:
            final_provider = final_attrs.get('gen_ai.provider.name') or final_attrs.get('gen_ai.system')
            final_request = final_attrs.get('gen_ai.request.model')
            final_response = final_attrs.get('gen_ai.response.model')
            
            print(f"[ModelFixProcessor] AFTER: request={final_request}, "
                  f"response={final_response}, provider={final_provider}")
        print(f"{'='*80}\n")
    
    def _get_correct_model_name(self, attributes: dict, provider_key: Optional[str]) -> Optional[str]:
        """Extract model name from attributes, preserving full identifiers.
        
        Args:
            attributes: Span attributes dictionary.
            provider_key: Provider key from _detect_provider.
            
        Returns:
            Full model identifier or None.
        """
        # For Bedrock spans, prioritize request model since response model is often missing
        if provider_key == "bedrock":
            request_model = attributes.get("gen_ai.request.model")
            if request_model and not _is_invalid_model(request_model):
                return request_model
        
        # For other spans, try to get from standard response model if it's valid
        response_model = attributes.get("gen_ai.response.model")
        if response_model and not _is_invalid_model(response_model):
            return response_model
        
        # For Ollama spans, check the traceloop association properties
        if provider_key == "ollama":
            ls_model_name = attributes.get("traceloop.association.properties.ls_model_name")
            if ls_model_name:
                return ls_model_name
            
        return None


    def _get_correct_provider_from_key(self, provider_key: Optional[str]) -> Optional[str]:
        """
        Get the correct provider name from cached provider key.
        """
        if provider_key:
            return PROVIDER_REGISTRY[provider_key]["provider_name"]

        # Default to Unknown when we cannot reliably determine provider
        return "Unknown"
    
    def _set_token_attributes(self, attributes_dict: dict, input_tokens: int, output_tokens: int) -> None:
        """Write token usage with new and legacy attribute names.
        
        Args:
            attributes_dict: Span attributes to modify.
            input_tokens: Input/prompt token count.
            output_tokens: Output/completion token count.
        """
        # Set new attribute names when missing or falsy
        if not attributes_dict.get("gen_ai.usage.input_tokens") and input_tokens > 0:
            attributes_dict["gen_ai.usage.input_tokens"] = input_tokens
        
        # Update legacy key only if it already existed on the span
        if "gen_ai.usage.prompt_tokens" in attributes_dict:
            attributes_dict["gen_ai.usage.prompt_tokens"] = input_tokens
        
        if not attributes_dict.get("gen_ai.usage.output_tokens") and output_tokens > 0:
            attributes_dict["gen_ai.usage.output_tokens"] = output_tokens
        
        if "gen_ai.usage.completion_tokens" in attributes_dict:
            attributes_dict["gen_ai.usage.completion_tokens"] = output_tokens
        
        # Set total tokens if missing
        if attributes_dict.get("llm.usage.total_tokens") in (None, "", 0) and (input_tokens > 0 or output_tokens > 0):
            attributes_dict["llm.usage.total_tokens"] = input_tokens + output_tokens

    def _fix_ollama_usage_attributes(self, attributes_dict: dict) -> None:
        """Populate token usage from Ollama-specific fields or JSON.
        
        Args:
            attributes_dict: Span attributes to modify.
        """
        try:
            # Look for Ollama-specific attributes
            prompt_eval_count = attributes_dict.get("prompt_eval_count")
            eval_count = attributes_dict.get("eval_count")
            
            # Try to extract from traceloop entity output (JSON response data)
            if prompt_eval_count is None or eval_count is None:
                entity_output = attributes_dict.get("traceloop.entity.output")
                if entity_output and isinstance(entity_output, str):
                    prompt_eval_count, eval_count = self._extract_ollama_tokens_from_json(entity_output)
            
            if prompt_eval_count is not None and eval_count is not None:
                # Convert to integers
                input_tokens = int(prompt_eval_count) if isinstance(prompt_eval_count, (str, int, float)) else 0
                output_tokens = int(eval_count) if isinstance(eval_count, (str, int, float)) else 0
                
                # Use consolidated helper method
                self._set_token_attributes(attributes_dict, input_tokens, output_tokens)
                    
        except (ValueError, TypeError, AttributeError):
            pass

    def _fix_bedrock_usage_attributes(self, attributes_dict: dict) -> None:
        """Populate token usage from Bedrock JSON response.
        
        Args:
            attributes_dict: Span attributes to modify.
        """
        try:
            # Quick check: if all attributes already present with valid values, no need to extract
            has_input = attributes_dict.get("gen_ai.usage.input_tokens") or attributes_dict.get("gen_ai.usage.prompt_tokens")
            has_output = attributes_dict.get("gen_ai.usage.output_tokens") or attributes_dict.get("gen_ai.usage.completion_tokens")
            has_total = attributes_dict.get("llm.usage.total_tokens") not in (None, "", 0)
            
            if has_input and has_output and has_total:
                return
            
            # Try to extract from traceloop entity output (JSON response data)
            entity_output = attributes_dict.get("traceloop.entity.output")
            if entity_output and isinstance(entity_output, str):
                prompt_tokens, completion_tokens, total_tokens = self._extract_bedrock_tokens_from_json(entity_output)
                
                if prompt_tokens is not None and completion_tokens is not None:
                    # Use consolidated helper method
                    self._set_token_attributes(attributes_dict, prompt_tokens, completion_tokens)
                    
                    # Override total tokens if Bedrock provided explicit value
                    if total_tokens is not None and total_tokens > 0:
                        attributes_dict["llm.usage.total_tokens"] = total_tokens
                    
        except (ValueError, TypeError, AttributeError):
            pass

    
    def _extract_tokens_from_json(self, json_output: str, extraction_config: Dict[str, list]) -> Dict[str, Optional[int]]:
        """Parse token counts from JSON using configurable paths.
        
        Args:
            json_output: JSON string to parse (may be double-encoded).
            extraction_config: Maps token types to JSON paths, e.g.
                {'input': ['raw', 'usage', 'inputTokens']}
        
        Returns:
            Dictionary with extracted token values (None if not found).
        """
        result = {key: None for key in extraction_config.keys()}
        
        try:
            import json
            data = json.loads(json_output)
            
            # Handle double-encoded JSON
            if isinstance(data, str):
                data = json.loads(data)
            
            # Extract each configured path
            for token_type, path in extraction_config.items():
                value = safe_extract_nested(data, *path, debug=self.debug_enabled)
                if value is not None:
                    result[token_type] = int(value)
                    
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            if self.debug_enabled:
                logger.warning(f"Failed to extract tokens from JSON: {e}")
        
        return result
    
    def _extract_ollama_tokens_from_json(self, json_output: str) -> Tuple[Optional[int], Optional[int]]:
        """Extract prompt_eval_count and eval_count from Ollama JSON response.
        
        Args:
            json_output: JSON string from traceloop.entity.output
            
        Returns:
            Tuple of (prompt_eval_count, eval_count) or (None, None) if not found
        """
        config = {
            'input': ['raw', 'prompt_eval_count'],
            'output': ['raw', 'eval_count']
        }
        tokens = self._extract_tokens_from_json(json_output, config)
        return tokens['input'], tokens['output']

    def _extract_bedrock_tokens_from_json(self, json_output: str) -> Tuple[Optional[int], Optional[int], Optional[int]]:
        """Extract token usage from Bedrock JSON response.
        
        Tries two formats:
        1. Bedrock native: {"raw": {"usage": {"inputTokens": X, ...}}}
        2. Alternative: {"additional_kwargs": {"prompt_tokens": X, ...}}
        
        Args:
            json_output: JSON string from traceloop.entity.output
            
        Returns:
            Tuple of (prompt_tokens, completion_tokens, total_tokens) or (None, None, None) if not found
        """
        # Try raw.usage format first (Bedrock native)
        config_native = {
            'input': ['raw', 'usage', 'inputTokens'],
            'output': ['raw', 'usage', 'outputTokens'],
            'total': ['raw', 'usage', 'totalTokens']
        }
        tokens = self._extract_tokens_from_json(json_output, config_native)
        
        if tokens['input'] is not None and tokens['output'] is not None:
            return tokens['input'], tokens['output'], tokens['total']
        
        # Try additional_kwargs format (alternative)
        config_alt = {
            'input': ['additional_kwargs', 'prompt_tokens'],
            'output': ['additional_kwargs', 'completion_tokens'],
            'total': ['additional_kwargs', 'total_tokens']
        }
        tokens = self._extract_tokens_from_json(json_output, config_alt)
        return tokens['input'], tokens['output'], tokens['total']

    # ---- Internal helper methods -------------------------------------------------

    def _get_writable_attributes(self, readable_span: ReadableSpan) -> Optional[dict]:
        """Return writable attributes dict or None.

        Prefers `_attributes` over public `attributes` (may be read-only).
        
        Args:
            readable_span: Span to access.
            
        Returns:
            Writable attributes dict or None.
        """
        if hasattr(readable_span, '_attributes'):
            readable_span._attributes = readable_span._attributes or {}
            logger.debug(f"Got writable attributes via _attributes, type={type(readable_span._attributes)}")
            return readable_span._attributes
        elif hasattr(readable_span, 'attributes') and isinstance(readable_span.attributes, dict):
            logger.warning("Using attributes property directly (may not persist changes)")
            return readable_span.attributes
        
        logger.error(f"Could not find writable attributes on span '{readable_span.name}'!")
        return None

    def _fix_provider_attribute(self, target_attrs: dict, provider_attr: Optional[str], correct_provider: Optional[str]) -> None:
        """Write provider name to `gen_ai.provider.name` and legacy keys.

        Updates `gen_ai.system` only if it already exists on the span.

        Args:
            target_attrs: Span attributes to modify.
            provider_attr: Current provider value.
            correct_provider: Provider name to set (e.g., "OpenAI").
        """
        if correct_provider and provider_attr != correct_provider:
            if self.debug_enabled:
                logger.debug(f"Fixing gen_ai.provider.name/gen_ai.system: '{provider_attr}' -> '{correct_provider}'")
            target_attrs["gen_ai.provider.name"] = correct_provider
            if "gen_ai.system" in target_attrs:
                target_attrs["gen_ai.system"] = correct_provider  # Backwards compatibility
            target_attrs["traceloop.association.properties.ls_provider"] = correct_provider

    def _fix_model_attributes(
        self, 
        target_attrs: dict, 
        provider_key: Optional[str],
        request_model_attr: Optional[str], 
        response_model_attr: Optional[str], 
        correct_model_name: Optional[str]
    ) -> None:
        """Write model names to request/response attributes.

        Bedrock: uses request model. Others: prefer response > request > fallback.

        Args:
            target_attrs: Span attributes to modify.
            provider_key: Provider key (e.g., 'openai', 'bedrock').
            request_model_attr: Current request model.
            response_model_attr: Current response model.
            correct_model_name: Fallback model name.
        """
        
        # For Bedrock spans, always use request model as the source of truth
        if provider_key == "bedrock":
            if request_model_attr and not _is_invalid_model(request_model_attr):
                # Keep the full model name to preserve regional and version information
                logger.debug(f"Bedrock span: using full model name {request_model_attr}")
                
                # Set both request and response model to the full model name
                target_attrs["gen_ai.request.model"] = request_model_attr
                target_attrs["gen_ai.response.model"] = request_model_attr
            else:
                logger.warning(f"Cannot set Bedrock model: request_model={request_model_attr}")
            return
        
        # For non-Bedrock spans, determine the primary model value
        # Priority: response > request > correct_model_name
        primary_model = (
            response_model_attr if not _is_invalid_model(response_model_attr)
            else request_model_attr if not _is_invalid_model(request_model_attr)
            else correct_model_name
        )
        
        # Early return if no valid model found
        if not primary_model:
            return
        
        # Apply fixes: set both request and response to the primary value
        if primary_model != request_model_attr:
            if self.debug_enabled:
                logger.debug(f"Fixing gen_ai.request.model: '{request_model_attr}' -> '{primary_model}'")
            target_attrs["gen_ai.request.model"] = primary_model
        
        if primary_model != response_model_attr:
            if self.debug_enabled:
                logger.debug(f"Fixing gen_ai.response.model: '{response_model_attr}' -> '{primary_model}'")
            target_attrs["gen_ai.response.model"] = primary_model

    def _apply_attribute_fixes(
        self,
        *,
        readable_span: ReadableSpan,
        span_name: str,
        provider_key: Optional[str],
        provider_attr: Optional[str],
        correct_provider: Optional[str],
        request_model_attr: Optional[str],
        response_model_attr: Optional[str],
        correct_model_name: Optional[str],
    ) -> None:
        """Apply provider, model and token fixes to span attributes.

        Args:
            readable_span: The span to fix
            span_name: Name of the span being processed
            provider_key: Cached provider key from _detect_provider
            provider_attr: Current gen_ai.provider.name or gen_ai.system value
            correct_provider: Correct provider value
            request_model_attr: Current request model value
            response_model_attr: Current response model value
            correct_model_name: Correct model name value
        """
        try:
            target_attrs = self._get_writable_attributes(readable_span)
            if target_attrs is None:
                logger.warning(f"Cannot apply fixes to span '{span_name}': no writable attributes found")
                return

            self._fix_provider_attribute(target_attrs, provider_attr, correct_provider)
            self._fix_model_attributes(target_attrs, provider_key, request_model_attr, response_model_attr, correct_model_name)
            
            # Provider-specific token usage metrics (using cached provider_key)
            if provider_key == "ollama":
                self._fix_ollama_usage_attributes(target_attrs)
            elif provider_key == "bedrock":
                self._fix_bedrock_usage_attributes(target_attrs)
        except Exception as e:
            logger.error(f"ModelFixProcessor._apply_attribute_fixes failed for span '{span_name}': {e}", exc_info=self.debug_enabled)

    def shutdown(self) -> None:
        """
        Called when the processor is shut down.
        
        This is part of the SpanProcessor interface. Currently no cleanup is needed
        as the processor doesn't hold any resources that require explicit cleanup.
        """
        pass

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        """
        Called to force flush any buffered spans.
        
        This is part of the SpanProcessor interface. Since this processor doesn't
        buffer spans (it processes them synchronously in on_end), this always returns True.
        
        Args:
            timeout_millis: Maximum time to wait for flush in milliseconds (unused)
            
        Returns:
            True indicating successful flush (no-op in this processor)
        """
        return True
