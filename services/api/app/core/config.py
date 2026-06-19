from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Compass"
    APP_ENV: str = "development"
    API_PREFIX: str = "/api/v1"
    DATABASE_URL: str = ""
    VOICE_TRANSCRIPTION_PROVIDER: str = ""
    VOICE_TRANSCRIPTION_API_KEY: str = ""
    VOICE_TRANSCRIPTION_MAX_BYTES: int = 5 * 1024 * 1024
    XFYUN_APP_ID: str = ""
    XFYUN_API_KEY: str = ""
    XFYUN_API_SECRET: str = ""
    XFYUN_ASR_ENDPOINT: str = ""
    XFYUN_ASR_AUDIO_FORMAT: str = "audio/wav"


settings = Settings()
