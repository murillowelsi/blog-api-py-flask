from flask import jsonify


def create_json_response(response_data, status_code):
    response = jsonify(response_data)
    response.status_code = status_code
    return response


def create_error_response(status_code, message):
    response_data = {'error': message}
    return jsonify(response_data), status_code
