import os

from pathlib import Path

from dotenv import load_dotenv

from msal import PublicClientApplication


load_dotenv(
    Path(__file__).resolve().parents[3] / ".env"
)


class AuthService:

    def __init__(self):

        self.client_id = os.getenv(
            "CLIENT_ID"
        )

        self.tenant_id = os.getenv(
            "TENANT_ID"
        )

        self.authority = (
            f"https://login.microsoftonline.com/"
            f"{self.tenant_id}"
        )

        self.scopes = [
            "User.Read",
            "Files.ReadWrite",
            "Sites.ReadWrite.All"
        ]

    def get_access_token(self):

        app = PublicClientApplication(
            self.client_id,
            authority=self.authority
        )

        result = app.acquire_token_interactive(
            scopes=self.scopes
        )

        return result.get(
            "access_token"
        )