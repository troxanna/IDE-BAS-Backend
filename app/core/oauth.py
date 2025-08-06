import os
from pathlib import Path
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from app.core.config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

config = Config(environ=os.environ)

oauth = OAuth(config)

oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"}
)