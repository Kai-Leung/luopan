"""ASR provider adapter framework.

This module only defines provider selection and adapter boundaries. It does not
implement any third-party provider protocol.
"""

from dataclasses import dataclass
from typing import Dict, Protocol


class VoiceTranscriptionProviderError(Exception):
    """Provider-level error safe to expose after mapping by the gateway."""


class VoiceTranscriptionProvider(Protocol):
    name: str

    def is_available(self) -> bool:
        ...

    def transcribe(self, *, audio_bytes: bytes, content_type: str) -> str:
        ...


@dataclass(frozen=True)
class ProviderConfig:
    name: str
    api_key: str = ""
    xfyun_app_id: str = ""
    xfyun_api_key: str = ""
    xfyun_api_secret: str = ""
    xfyun_asr_endpoint: str = ""
    xfyun_asr_audio_format: str = ""


class PlaceholderProvider:
    """Reserved adapter slot for future concrete ASR providers."""

    def __init__(self, name: str, api_key: str) -> None:
        self.name = name
        self._api_key = api_key

    def is_available(self) -> bool:
        return bool(self._api_key)

    def transcribe(self, *, audio_bytes: bytes, content_type: str) -> str:
        raise VoiceTranscriptionProviderError(
            "voice transcription provider is not implemented"
        )


class XfyunProvider:
    """科大讯飞开放平台语音听写 provider adapter boundary."""

    name = "xfyun"

    def __init__(self, config: ProviderConfig) -> None:
        self._app_id = config.xfyun_app_id.strip()
        self._api_key = config.xfyun_api_key.strip()
        self._api_secret = config.xfyun_api_secret.strip()
        self._endpoint = config.xfyun_asr_endpoint.strip()
        self._audio_format = config.xfyun_asr_audio_format.strip().lower()

    def is_available(self) -> bool:
        return all((self._app_id, self._api_key, self._api_secret, self._endpoint, self._audio_format))

    def transcribe(self, *, audio_bytes: bytes, content_type: str) -> str:
        self._require_configured()
        normalized_content_type = content_type.split(";")[0].strip().lower()
        if normalized_content_type != self._audio_format:
            raise VoiceTranscriptionProviderError("xfyun audio format is not supported")
        raise VoiceTranscriptionProviderError("xfyun provider protocol is not configured")

    def _require_configured(self) -> None:
        if not self._app_id:
            raise VoiceTranscriptionProviderError("xfyun app id is not configured")
        if not self._api_key:
            raise VoiceTranscriptionProviderError("xfyun api key is not configured")
        if not self._api_secret:
            raise VoiceTranscriptionProviderError("xfyun api secret is not configured")
        if not self._endpoint:
            raise VoiceTranscriptionProviderError("xfyun endpoint is not configured")
        if not self._audio_format:
            raise VoiceTranscriptionProviderError("xfyun audio format is not configured")


def _create_xfyun_provider(name: str, api_key: str, config: ProviderConfig) -> XfyunProvider:
    return XfyunProvider(config)


def _create_placeholder_provider(
    name: str,
    api_key: str,
    config: ProviderConfig,
) -> PlaceholderProvider:
    return PlaceholderProvider(name, api_key)


SUPPORTED_PROVIDER_FACTORIES = {
    "adapter_placeholder": _create_placeholder_provider,
    "xfyun": _create_xfyun_provider,
}


def create_voice_transcription_provider(
    config: ProviderConfig,
) -> VoiceTranscriptionProvider:
    provider_name = config.name.strip().lower()
    if not provider_name:
        raise VoiceTranscriptionProviderError("voice transcription provider is not configured")
    if provider_name != "xfyun" and not config.api_key.strip():
        raise VoiceTranscriptionProviderError("voice transcription provider key is not configured")

    provider_factory = SUPPORTED_PROVIDER_FACTORIES.get(provider_name)
    if provider_factory is None:
        raise VoiceTranscriptionProviderError("voice transcription provider is not supported")
    return provider_factory(provider_name, config.api_key.strip(), config)


def get_supported_provider_names() -> Dict[str, str]:
    return {provider_name: "adapter slot" for provider_name in SUPPORTED_PROVIDER_FACTORIES}
