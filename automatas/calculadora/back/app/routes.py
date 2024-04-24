
from lexer.lexer import calculate_expression  # Asegúrate que esta importación es correcta
from flask import Blueprint, request, jsonify, make_response
import logging

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/calculate', methods=['POST', 'OPTIONS'])
def calculate():
    if request.method == 'OPTIONS':
        response = _build_cors_prelight_response()
        logging.debug("Sending OPTIONS response with headers: %s", response.headers)
        return response
    elif request.method == 'POST':
        data = request.get_json()
        expression = data.get('expression', '')
        try:
            result = calculate_expression(expression)
            response = jsonify({'result': result})
            logging.debug("Sending POST response with result: %s", result)
            return jsonify({
            'result': result['result'],
            'tokens': result['original_tokens'],
            'rpn': result['rpn_tokens'],
            'status': 'success'
        }), 200
        except Exception as e:
            error_msg = str(e)
            logging.error("Error processing expression: %s", error_msg, exc_info=True)
            return jsonify({'error': str(e), 'status': 'error'}), 400

def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    logging.debug("Preflight response headers set for CORS")
    return response
