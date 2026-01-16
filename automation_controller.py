from ai_key_validation_tf import validate_key
from ai_anomaly_detection_torch import detect_anomaly

def security_decision(key, qber):
    key_ok = validate_key(key)
    anomaly = detect_anomaly(qber, noise=0.02, mismatch=qber)

    if not key_ok:
        return "REJECT_KEY"
    if anomaly:
        return "ATTACK_DETECTED"
    return "PROCEED"
