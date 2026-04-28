import importlib.util
import os
from dotenv import load_dotenv

def run_preflight_checks() -> None:
    # 1. Try to load .env, but don't fail if it's missing (it will be missing on GitHub)
    load_dotenv()

    # 2. Module Check (This is good, keep it)
    required_modules = ["dotenv", "pydantic", "requests", "supabase"]
    missing_modules = [m for m in required_modules if importlib.util.find_spec(m) is None]
    if missing_modules:
        missing_list = ", ".join(missing_modules)
        raise RuntimeError(f"Missing Python packages: {missing_list}. Install with: pip install -r requirements.txt")

    # 3. Environment Variable Check
    required_env = ["SUPABASE_URL", "SUPABASE_KEY", "ALPHA_VANTAGE_KEY"]
    
    # We check os.environ directly to ensure we see the GitHub injected secrets
    missing_env = [name for name in required_env if not os.environ.get(name)]
    
    if missing_env:
        missing_list = ", ".join(missing_env)
        # CHANGED: Generic error message (doesn't blame the .env file)
        raise RuntimeError(f"Missing environment variables: {missing_list}")

    print("✅ Preflight checks passed.")