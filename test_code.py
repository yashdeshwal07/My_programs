import requests


def ask_ai(prompt):
    import requests

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": "Bearer API_KEY",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}]
    }

    r = requests.post(url, headers=headers, json=data)
    response = r.json()

    if "choices" not in response:
        return f"Groq error: {response}"

    return response["choices"][0]["message"]["content"]


print(ask_ai("hello"))