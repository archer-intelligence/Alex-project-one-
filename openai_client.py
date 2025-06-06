import os
import openai
import json
from typing import Any, Dict

# Retrieve the API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_curriculum(topic: str) -> Dict[str, Any]:
    """Call the OpenAI API to generate curriculum data."""
    if not openai.api_key:
        raise RuntimeError('OPENAI_API_KEY environment variable not set')

    prompt = (
        'Generate a learning curriculum as JSON strictly following this schema:\n'
        '{"topic": "string", "curriculum": [{"module_number": 1, "title": "string",'
        ' "description": "string", "resources": [{"url": "string", "description": "string"}],'
        ' "exercise": "string", "quiz": [{"question": "string", "answers": ["string"],'
        ' "correct_answer_index": 0}]}]}'
        f'\nTopic: {topic}\nReturn JSON only.'
    )

    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.7,
        )
    except Exception as e:
        raise RuntimeError(f'OpenAI API request failed: {e}')

    try:
        content = response['choices'][0]['message']['content']
    except (KeyError, IndexError) as e:
        raise RuntimeError('Invalid response structure from OpenAI') from e

    try:
        data = json.loads(content)
    except Exception as e:
        raise RuntimeError('Failed to parse JSON from OpenAI response') from e

    # Basic validation of expected keys
    if 'topic' not in data or 'curriculum' not in data:
        raise RuntimeError('Missing expected fields in OpenAI response')
    return data
