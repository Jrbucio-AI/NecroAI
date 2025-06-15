# logic_engine.py

def analyze_input(prompt):
    alerts = []
    lowered = prompt.lower()

    if any(w in lowered for w in ["delete", "format", "erase", "shutdown"]) and "confirm" not in lowered:
        alerts.append("Destructive command detected without confirmation.")
    if lowered.strip() in ["yes", "sure", "okay"] and not memory_has_context():
        alerts.append("Ambiguous input: no context for agreement.")
    if "open" in lowered and ".exe" in lowered:
        alerts.append("Opening executable file. Are you sure this is safe?")

    return alerts

def memory_has_context():
    # Future implementation, currently always returns True
    return True

