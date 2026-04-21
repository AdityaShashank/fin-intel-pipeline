import importlib.util
import os

from dotenv import load_dotenv


def run_preflight_checks() -> None:
    load_dotenv()

    required_modules = [
        "dotenv",
        "pydantic",
        "requests",
        "supabase",
    ]
    missing_modules = [m for m in required_modules if importlib.util.find_spec(m) is None]
    if missing_modules:
        missing_list = ", ".join(missing_modules)
        raise RuntimeError(
            f"Missing Python packages: {missing_list}. "
            "Install with: python -m pip install -r requirements.txt"
        )

    required_env = [
        "SUPABASE_URL",
        "SUPABASE_KEY",
        "ALPHA_VANTAGE_KEY",
    ]
    missing_env = [name for name in required_env if not os.getenv(name)]
    if missing_env:
        missing_list = ", ".join(missing_env)
        raise RuntimeError(f"Missing environment variables in .env: {missing_list}")

    print("Preflight checks passed.")
