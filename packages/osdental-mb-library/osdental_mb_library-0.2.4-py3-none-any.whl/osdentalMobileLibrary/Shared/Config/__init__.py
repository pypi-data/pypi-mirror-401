import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)


class Config:
    SECURITY_MOB_GRPC_HOSTMOB = os.getenv("SECURITY_MOB_GRPC_HOST")
    SECURITY_MOB_GRPC_PORTMOB = os.getenv("SECURITY_MOB_GRPC_PORT", None)

    APPLICATIONINSIGHTS_CONNECTION_STRING = os.getenv(
        "APPLICATIONINSIGHTS_CONNECTION_STRING"
    )
