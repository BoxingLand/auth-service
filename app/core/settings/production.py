from app.core.settings.app import AppSettings


class ProdAppSettings(AppSettings):

    title: str = "Prod auth service"

    class Config(AppSettings.Config):
        env_file = ".env.prod"
