"""Voiceground - Observability framework for Pipecat conversational AI."""

from voiceground.events import VoicegroundEvent
from voiceground.metrics import (
    VoicegroundLLMResponseTimeFrame,
    VoicegroundResponseTimeFrame,
    VoicegroundSystemOverheadFrame,
    VoicegroundToolUsageFrame,
    VoicegroundTranscriptionOverheadFrame,
    VoicegroundTurnDurationFrame,
    VoicegroundVoiceSynthesisOverheadFrame,
)
from voiceground.observer import VoicegroundObserver
from voiceground.reporters import BaseReporter, HTMLReporter, MetricsReporter

try:
    from importlib.metadata import PackageNotFoundError, version

    __version__ = version("voiceground")
except (PackageNotFoundError, Exception):
    # Fallback for development/editable installs
    # The actual version will be set by hatch-vcs during build
    __version__ = "0.0.0+dev"
__all__ = [
    "VoicegroundObserver",
    "VoicegroundEvent",
    "BaseReporter",
    "HTMLReporter",
    "MetricsReporter",
    "VoicegroundTurnDurationFrame",
    "VoicegroundResponseTimeFrame",
    "VoicegroundTranscriptionOverheadFrame",
    "VoicegroundVoiceSynthesisOverheadFrame",
    "VoicegroundLLMResponseTimeFrame",
    "VoicegroundSystemOverheadFrame",
    "VoicegroundToolUsageFrame",
    "__version__",
]
