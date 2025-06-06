from flask import Flask, request, jsonify
from schemas import CurriculumRequest, CurriculumResponse
import openai_client
import time
import logging

app = Flask(__name__, static_folder='static', static_url_path='')
logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['GET'])
def homepage():
    return app.send_static_file('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({'error': 'Invalid JSON payload'}), 400

    try:
        req = CurriculumRequest(**data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    if not req.topic.strip():
        return jsonify({'error': 'topic must not be empty'}), 400

    start_time = time.time()
    try:
        curriculum_dict = openai_client.generate_curriculum(req.topic)
    except Exception as e:
        logging.error(f"Error generating curriculum: {e}")
        return jsonify({'error': str(e)}), 502
    latency = time.time() - start_time
    logging.info(f"Generated curriculum for '{req.topic}' in {latency:.2f}s")

    try:
        curriculum = CurriculumResponse(**curriculum_dict)
    except Exception as e:
        logging.error("Invalid curriculum data from OpenAI")
        return jsonify({'error': 'Invalid curriculum data from OpenAI'}), 502

    return jsonify(curriculum.dict()), 200

if __name__ == '__main__':
    app.run(debug=True)
