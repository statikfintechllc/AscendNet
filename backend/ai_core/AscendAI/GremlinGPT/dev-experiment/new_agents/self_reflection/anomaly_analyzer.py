def analyze(logs):
    return [l for l in logs if "error" in l.lower()]
