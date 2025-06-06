import os
from flask import Flask, request, jsonify
from schemas import CurriculumRequest, CurriculumResponse
from openai_client import generate_curriculum

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    """Endpoint to generate a curriculum for a given topic."""
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({'error': 'Invalid JSON payload'}), 400

    # Validate input using Pydantic
    try:
        req = CurriculumRequest(**data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    # Ensure topic is not empty
    if not req.topic.strip():
        return jsonify({'error': 'topic must not be empty'}), 400

    # Call the OpenAI client to generate curriculum
    try:
        curriculum_dict = generate_curriculum(req.topic)
    except Exception as e:
        return jsonify({'error': str(e)}), 502

    # Validate output using Pydantic
    try:
        curriculum = CurriculumResponse(**curriculum_dict)
    except Exception as e:
        return jsonify({'error': 'Invalid curriculum data returned from OpenAI'}), 502

    return jsonify(curriculum.dict()), 200

if __name__ == '__main__':
    # Run the Flask development server
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
