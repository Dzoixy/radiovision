# backend/app/services/postprocess.py

CLASS_NAMES = ["Normal", "Pneumonia"]


def run(prob, purpose):

    if purpose == "screening":
        threshold = 0.5
    else:
        threshold = 0.8

    idx = prob.argmax()
    confidence = float(prob[idx])

    label = CLASS_NAMES[idx]

    if confidence < threshold:
        label = "Normal"

    return {
        "label": label,
        "confidence": confidence
    }