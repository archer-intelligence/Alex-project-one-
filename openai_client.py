import os
import openai
import json
import logging
from typing import Any, Dict
from functools import lru_cache

logging.basicConfig(level=logging.INFO)
openai.api_key = os.getenv('OPENAI_API_KEY')

@lru_cache(maxsize=128)
def _call_openai_for_curriculum(topic: str) -> Dict[str, Any]:
    prompt = (
        'Generate a learning curriculum as JSON strictly following this schema:\n'
        '{"topic":"string","curriculum":[{"module_number":1,"title":"string",'
        '"description":"string","resources":[{"url":"string","description":"string"}],'
        '"exercise":"string","quiz":[{"question":"string","answers":["string"],"correct_answer_index":0}]}]}\n'
        f'\nTopic: {topic}\nReturn JSON only.'
    )
    try:
        response = openai.ChatCompletion.create(
            model=os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.2,
        )
    except Exception as e:
        logging.error(f"OpenAI API request failed: {e}")
        raise RuntimeError(f"OpenAI failure: {e}")

    try:
        content = response['choices'][0]['message']['content']
    except (KeyError, IndexError) as e:
        logging.error("Invalid response structure from OpenAI")
        raise RuntimeError("Invalid response structure from OpenAI") from e

    try:
        data = json.loads(content)
    except Exception as e:
        logging.error("Failed to parse JSON from OpenAI response")
        raise RuntimeError("JSON parse error") from e

    if 'topic' not in data or 'curriculum' not in data:
        logging.error("Missing fields in OpenAI response")
        raise RuntimeError("Missing expected fields in OpenAI response")
    return data

def generate_curriculum(topic: str) -> Dict[str, Any]:
    logging.info(f"Generating curriculum for topic: {topic}")
    return _call_openai_for_curriculum(topic)
