from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_BASE_URL: str = "http://localhost:8000"
    ENVIRONMENT: str = "development"

    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/ledger"

    ZOHO_CLIENT_ID: str = ""
    ZOHO_CLIENT_SECRET: str = ""
    ZOHO_BASE: str = "https://www.zohoapis.com"
    ZOHO_ACCOUNTS_BASE: str = "https://accounts.zoho.com"
    ZOHO_SCOPES: str = "ZohoExpense.expenses.READ,ZohoExpense.reports.READ,ZohoExpense.files.READ"

    ENCRYPTION_KEY: str = ""
    SYNC_INTERVAL_MINUTES: int = 15
    ADMIN_TOKEN: str = "dev_admin_token"

    class Config:
        env_file = ".env"

settings = Settings()
