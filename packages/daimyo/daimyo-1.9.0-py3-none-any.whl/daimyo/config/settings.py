"""Configuration management using dynaconf."""

from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    envvar_prefix="DAIMYO",
    settings_files=[".daimyo/config/settings.toml", ".daimyo/config/.secrets.toml"],
    environments=True,
    load_dotenv=True,
    validators=[
        Validator("RULES_PATH", default=".daimyo/rules"),
        Validator("LOG_LEVEL", default="INFO"),
        Validator("LOG_FILE", default="logs/daimyo.log"),
        Validator("LOG_JSON_FILE", default="logs/daimyo.jsonl"),
        Validator("MAX_INHERITANCE_DEPTH", default=10, gte=1, lte=100),
        Validator("MASTER_SERVER_URL", default=""),
        Validator("REMOTE_TIMEOUT_SECONDS", default=5, gte=1, lte=60),
        Validator("REMOTE_MAX_RETRIES", default=3, gte=0, lte=10),
        Validator("REST_HOST", default="0.0.0.0"),
        Validator("REST_PORT", default=8000, gte=1, lte=65535),
        Validator("MCP_TRANSPORT", default="stdio", is_in=["stdio", "http"]),
        Validator("MCP_HOST", default="0.0.0.0"),
        Validator("MCP_PORT", default=8001, gte=1, lte=65535),
        Validator("ENABLED_PLUGINS", default=[]),
        Validator("RULES_MARKDOWN_PROLOGUE", default=""),
        Validator("RULES_MARKDOWN_EPILOGUE", default=""),
        Validator("INDEX_MARKDOWN_PROLOGUE", default=""),
        Validator("INDEX_MARKDOWN_EPILOGUE", default=""),
        Validator("DEFAULT_CATEGORY_DESCRIPTION", default="These rules apply at all times"),
        Validator("COMMANDMENTS_XML_TAG", default=""),
        Validator("SUGGESTIONS_XML_TAG", default=""),
        Validator("RULES_CATEGORIZED", default=True, is_type_of=bool),
    ],
)

__all__ = ["settings"]
