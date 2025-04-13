from pydantic_settings import BaseSettings
import logging

_log = logging.getLogger(__name__)


class Settings(BaseSettings):
    URL_CORS: str

    TG_API_ID: int
    TG_API_HASH: str
    TG_PHONE: str
    TG_SESSION_NAME: str
    TG_2FA_PASSWORD: str

    def __init__(self):
        super().__init__(
            _env_file=".env",
            _env_file_encoding="utf-8",
        )

        self.config_logging()

    def config_logging(self, level=logging.INFO) -> None:
        logging.basicConfig(
            level=level,
            datefmt="%Y-%m-%d %H:%M:%S",
            format="[%(asctime)s.%(msecs)03d] %(module)20s:%(lineno)-3d %(levelname)-7s - %(message)s",
        )

    @property
    def LIST_CORS(self):
        return self.URL_CORS.split(",")


settings = Settings()
