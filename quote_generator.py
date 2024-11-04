import os
import json
from dotenv import load_dotenv
import requests

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def gen_text(message):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }
    data = {
        "model": "gpt-4o-2024-08-06",
        "messages": message,
        "max_tokens": 1300,
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()

        # print("Response:", response_data)

        if response_data.get('error'):
            print(f"An error occurred: {response_data['error']['message']}")
            return None

        return response_data['choices'][0]['message']['content'].strip()

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def parse_jokes(jokes_text):
    jokes_list = []
    joke_lines = jokes_text.split("\n\n")

    for i, joke in enumerate(joke_lines, start=1):
        parts = joke.split("\n")
        if len(parts) < 3:
            continue

        name = parts[0].strip()
        answer = parts[1].strip()

        tags_line = parts[2].replace("Tags:", "").strip()
        tags = ["Tags"] + [tag.strip().strip('[]') for tag in tags_line.split(",")]

        jokes_list.append({
            "id": i,
            "name": name,
            "answer": answer,
            "tags": tags
        })

    print("Parsed Jokes List:", jokes_list)
    return jokes_list


def save_to_json(data, filename):
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, filename)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Data saved to {output_path}")


topic = "jokes for kids"

message = [
    {
        "role": "system",
        "content": "You are a helpful assistant."
    },
    {
        "role": "user",
        "content": f"I am creating a joke website with lots of categories. Come up with 50 jokes for this topic {topic} but all jokes need to be clean, no racist jokes and no controversial jokes. Also come up with 3 tags for each joke that I can categorize them with on my website. Please don't include any numbering, symbols or special characters in the jokes."
    }
]

jokes_text = gen_text(message)

if jokes_text:
    parsed_jokes = parse_jokes(jokes_text)
    save_to_json(parsed_jokes, f"{topic}.json")
