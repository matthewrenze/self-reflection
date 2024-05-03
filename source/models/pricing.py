def get_pricing(model_name):
    model_pricing = {
        "gpt-35-turbo": (0.0015, 0.002),
        "gpt-4": (0.03, 0.06),
        "llama-2-7b-chat": (0.00052, 0.00067),
        "llama-2-70b-chat": (0.00154, 0.00177),
        "mistral-large": (0.008, 0.024),
        "cohere-command-r-plus": (0.003, 0.015),
        "gemini-1.0-pro": (0.0005, 0.0015),
        "gemini-1.5-pro-preview-0409": (0.007, 0.021),
        "claude-3-opus-20240229": (0.015, 0.075)}
    return model_pricing.get(model_name)
