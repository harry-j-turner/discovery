from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # Agent
    agent_origin: str = "http://localhost"
    agent_port: int = 3000

    class Config:
        env_file = ".env"


settings = Settings()
