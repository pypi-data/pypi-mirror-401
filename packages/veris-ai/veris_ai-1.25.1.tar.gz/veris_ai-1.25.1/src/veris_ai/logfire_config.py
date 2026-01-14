"""Logfire configuration for conditional trace collection.

This module handles automatic Logfire configuration that only sends traces
when a session_id exists (simulation mode). It uses a custom OpenTelemetry
sampler to conditionally create spans based on session context.
"""

import logging
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from opentelemetry.sdk.trace import Span, SpanProcessor
from opentelemetry.sdk.trace.sampling import (
    Decision,
    ParentBased,
    Sampler,
    SamplingResult,
)

if TYPE_CHECKING:
    from opentelemetry.context import Context
    from opentelemetry.trace import Link, SpanKind
    from opentelemetry.trace.span import TraceState
    from opentelemetry.util.types import Attributes

from veris_ai.context_vars import (
    _logfire_token_context,
    _session_id_context,
    _target_context,
    _thread_id_context,
)

logger = logging.getLogger(__name__)

# Module-level state for FastAPI instrumentation
_fastapi_app: Any = None  # noqa: ANN401
_fastapi_instrumented: bool = False


def set_fastapi_app(app: Any) -> None:  # noqa: ANN401
    """Store the FastAPI app for later instrumentation.

    Args:
        app: The FastAPI application instance.
    """
    global _fastapi_app  # noqa: PLW0603
    _fastapi_app = app


class VerisConditionalSampler(Sampler):
    """Custom OpenTelemetry sampler that only samples traces when session_id exists.

    This sampler checks if a Veris session_id is present in the context.
    If present, it samples the trace (simulation mode). If not, it drops
    the trace (production mode).
    """

    def should_sample(  # noqa: PLR0913
        self,
        parent_context: "Context | None" = None,  # noqa: ARG002
        trace_id: int | None = None,  # noqa: ARG002
        name: str | None = None,  # noqa: ARG002
        kind: "SpanKind | None" = None,  # noqa: ARG002
        attributes: "Attributes | None" = None,  # noqa: ARG002
        links: Sequence["Link"] | None = None,  # noqa: ARG002
        trace_state: "TraceState | None" = None,  # noqa: ARG002
    ) -> SamplingResult:
        """Determine whether to sample a trace based on session_id presence.

        Args:
            parent_context: Parent span context (unused)
            trace_id: Trace ID (unused)
            name: Span name (unused)
            kind: Span kind (unused)
            attributes: Span attributes (unused)
            links: Span links (unused)
            trace_state: Trace state (unused)

        Returns:
            SamplingResult with RECORD_AND_SAMPLE if session_id exists,
            DROP otherwise
        """
        session_id = _session_id_context.get()
        if session_id:
            return SamplingResult(Decision.RECORD_AND_SAMPLE)
        return SamplingResult(Decision.DROP)

    def get_description(self) -> str:
        """Return description of the sampler."""
        return "VerisConditionalSampler"

    def __repr__(self) -> str:
        """Return string representation of the sampler."""
        return f"{self.__class__.__name__}()"


class VerisBaggageSpanProcessor(SpanProcessor):
    """Span processor that adds Veris session_id, thread_id, and target as span attributes.

    This processor reads session_id, thread_id, and target from context variables and
    sets them as span attributes with prefixed keys 'veris_ai.session_id',
    'veris_ai.thread_id', and 'veris_ai.target'. This only runs for spans that are being sampled.
    """

    def on_start(
        self,
        span: Span,
        parent_context: "Context | None" = None,  # noqa: ARG002
    ) -> None:
        """Add Veris attributes to span when it starts."""
        session_id = _session_id_context.get()
        thread_id = _thread_id_context.get()
        target = _target_context.get()

        if session_id:
            span.set_attribute("veris_ai.session_id", str(session_id))
            if thread_id:
                span.set_attribute("veris_ai.thread_id", str(thread_id))
            if target:
                span.set_attribute("veris_ai.target", str(target))


def configure_logfire_conditionally(  # noqa: PLR0912
    fastapi_app: Any = None,  # noqa: ANN401
) -> None:
    """Configure Logfire with conditional sampling based on session_id.

    If logfire_token is present, configures Logfire with:
    - Custom sampler that only samples spans when session_id exists
    - Span processor that adds veris_ai.session_id and veris_ai.thread_id attributes

    Args:
        fastapi_app: Optional FastAPI application instance to instrument.
            If provided, this takes precedence over any app set via set_fastapi_app().
            Can be obtained from within a route via `request.app`.

    Example:
        ```python
        from fastapi import Request

        @app.post("/my-route")
        async def my_route(request: Request):
            # Get app from request and configure logfire
            configure_logfire_conditionally(fastapi_app=request.app)
        ```
    """
    logfire_token = _logfire_token_context.get()
    if not logfire_token:
        # Backwards compatible: if no token, do nothing
        return

    try:
        import logfire
        from logfire.sampling import SamplingOptions
    except ImportError:
        # Logfire is optional dependency - handle gracefully
        logger.debug("Logfire not available, skipping configuration")
        return

    # Check if logfire is already configured with the same token to avoid re-instrumentation
    try:
        from logfire import DEFAULT_LOGFIRE_INSTANCE

        if hasattr(DEFAULT_LOGFIRE_INSTANCE, "_config"):
            config = DEFAULT_LOGFIRE_INSTANCE._config  # noqa: SLF001
            if hasattr(config, "token") and config.token:
                # Only skip if the token matches - allow reconfiguration with different token
                if config.token == logfire_token:
                    logfire.debug("Logfire already configured with same token, skipping")
                    return
                logfire.debug(
                    "Logfire token changed from ...{old_token} to ...{new_token}..., reconfiguring",
                    old_token=config.token[:-3],
                    new_token=logfire_token[:3],
                )
    except Exception as e:
        # If we can't check, proceed with configuration anyway
        # This is expected if logfire internals change or aren't accessible
        logfire.debug("Could not check logfire configuration state: {error}", error=str(e))

    # Configure logfire with conditional sampler and span processor
    # The sampler filters spans (only samples when session_id exists)
    # The span processor adds attributes to sampled spans
    logfire.configure(
        scrubbing=False,
        service_name="target_agent",
        sampling=SamplingOptions(head=ParentBased(VerisConditionalSampler())),
        token=logfire_token,
        add_baggage_to_attributes=True,
        send_to_logfire=True,
        additional_span_processors=[VerisBaggageSpanProcessor()],
    )

    # Instrument common libraries - each wrapped independently so failures don't block others
    global _fastapi_instrumented  # noqa: PLW0603
    instrumented_libraries: list[str] = []

    # Instrument FastAPI if app was provided (param or module-level) and not already instrumented
    app_to_instrument = fastapi_app or _fastapi_app
    if app_to_instrument is not None and not _fastapi_instrumented:
        try:
            logfire.instrument_fastapi(app_to_instrument)
            instrumented_libraries.append("FastAPI")
            _fastapi_instrumented = True
        except Exception:  # noqa: S110 - Silently fail if instrumentation fails
            pass

    try:
        logfire.instrument_openai()
        instrumented_libraries.append("OpenAI")
    except Exception:  # noqa: S110 - Silently fail if library not available
        pass

    try:
        logfire.instrument_anthropic()
        instrumented_libraries.append("Anthropic")
    except Exception:  # noqa: S110 - Silently fail if library not available
        pass

    try:
        logfire.instrument_google_genai()
        instrumented_libraries.append("Google GenAI")
    except Exception:  # noqa: S110 - Silently fail if library not available
        pass

    try:
        logfire.instrument_litellm()
        instrumented_libraries.append("LiteLLM")
    except Exception:  # noqa: S110 - Silently fail if library not available
        pass

    try:
        logfire.instrument_openai_agents()
        instrumented_libraries.append("OpenAI Agents")
    except Exception:  # noqa: S110 - Silently fail if library not available
        pass

    try:
        logfire.instrument_pydantic_ai()
        instrumented_libraries.append("Pydantic AI")
    except Exception:  # noqa: S110 - Silently fail if library not available
        pass

    # Create a dedicated span in Logfire to log the configuration status
    with logfire.span(
        "veris_ai_logfire_configuration",
        _tags=["veris-ai", "configuration"],
    ) as config_span:
        config_span.set_attribute("veris_ai.config.status", "enabled")
        config_span.set_attribute("veris_ai.config.instrumented_libraries", instrumented_libraries)
        config_span.set_attribute("veris_ai.config.instrumentor_count", len(instrumented_libraries))

        if instrumented_libraries:
            logfire.info(
                "Instrumented libraries for veris-ai simulations: {libraries}",
                libraries=", ".join(instrumented_libraries),
            )

        logfire.info("Simulation logs are being piped to Veris via Logfire")
