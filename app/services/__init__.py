"""
services package

This package contains service-layer components used by the application,
including implementations of Speech-to-Text (STT) systems and other
processing utilities.

Modules
-------
speech_to_text
    Defines the abstract base class `SpeechToText` that all STT engines must implement.

whisper
    Provides a concrete implementation of the `SpeechToText` interface using Whisper
    or Faster-Whisper for audio transcription.

Purpose
-------
This package provides a unified interface for audio transcription services, allowing
different backend engines to be swapped easily while maintaining the same API contract.
"""
