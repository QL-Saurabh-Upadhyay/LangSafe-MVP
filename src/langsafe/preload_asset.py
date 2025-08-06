import torch
from transformers import pipeline

def preload_asset():
    # Preload some models to cache them
    try:
        # Toxicity model
        _ = pipeline("text-classification", model="unitary/unbiased-toxic-roberta", device_map="auto")
        print("✅ Toxicity model cached")
    except:
        print("⚠️ Could not cache toxicity model")

    try:
        # Language detection model
        _ = pipeline("text-classification", model="papluca/xlm-roberta-base-language-detection", device_map="auto")
        print("✅ Language detection model cached")
    except:
        print("⚠️ Could not cache language detection model")

    try:
        # Prompt injection model
        _ = pipeline("text-classification", model="ProtectAI/deberta-v3-base-prompt-injection-v2", device_map="auto")
        print("✅ Prompt injection model cached")
    except:
        print("⚠️ Could not cache prompt injection model")