

def process_data(data):
    # This is a good function
    print(data)

def risky_business():
    # TEST CASE 1: Hardcoded Path (System Risk, Explicit)
    config_path = "/etc/myapp/config.json"

    
    try:
        with open(config_path):
            pass
    # TEST CASE 2: Silent Failure (Buried, Silent)
    except Exception:
        pass

def another_silent_one():
    try:
        1 / 0
    except Exception: # assumeless: ignore
        pass
