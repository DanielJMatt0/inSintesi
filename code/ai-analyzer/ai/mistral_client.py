import json
from mistralai import Mistral
from config import MISTRAL_API_KEY, MISTRAL_MODEL

client = Mistral(api_key=MISTRAL_API_KEY)

def ask_mistral(prompt: str, format_json: bool = True, temperature: float = 0.3):
    """
    Send a prompt to the Mistral API and optionally parse a JSON response.
    Returns either a dictionary or a plain string.
    """
    response = client.chat.complete(
        model=MISTRAL_MODEL,
        temperature=temperature,
        response_format={"type": "json_object"} if format_json else None,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.choices[0].message.content
    if format_json:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"raw": text}
    return text.strip()
