from streamlit.testing.v1 import AppTest

def test_app_startup():
    # Increase timeout to 10 or 15 seconds to give Supabase time to respond
    at = AppTest.from_file("src/app.py").run(timeout=15)
    assert not at.exception