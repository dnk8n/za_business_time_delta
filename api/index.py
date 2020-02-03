from flask import Flask, jsonify, request

from za_business_time_delta.za_business_time_delta import get_time_delta

app = Flask(__name__)


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/")
def home():
    return """
        <!DOCTYPE html>
        <html>
        <body>
        
        <h2>Welcome to basic request helper.</h2>
        <p>This form will be submitted using the GET method to /time_delta endpoint</p>
        
        <form action="/time_delta" method="GET">
          Start time:<br>
          <input type="text" name="start_time" value="2019-01-01T00:00:00.000000+02:00">
          <br>
          End time:<br>
          <input type="text" name="end_time" value="2021-01-01T00:00:00.000000+02:00">
          <br><br>
          <input type="submit" value="Submit">
        </form>
        
        <p>After you submit, the form values are visible in the address bar of the current browser tab.</p>
        
        </body>
        </html>
    """


@app.route('/time_delta', methods=['GET'])
def get_time_delta_api():
    start_time = request.args.get('start_time', None)
    end_time = request.args.get('end_time', None)
    if start_time and end_time:
        try:
            return jsonify(get_time_delta(start_time, end_time))
        except ValueError as e:
            raise InvalidUsage(str(e), status_code=400)
    else:
        raise InvalidUsage(f'start_time: {start_time} and end_time: {end_time} invalid.', status_code=400)
