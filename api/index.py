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
        
        <h1>Welcome to a very basic request helper for the <b>/time_delta</b> endpoint</h1> 
        <p>This form will be submitted using the <b>GET</b> method to the <b>/time_delta</b> endpoint</p>
        
        <form action="/time_delta" method="GET">
          Start time:<br>
          <input type="text" name="start_time" value="2019-01-01T00:00:00">
          <br>
          End time:<br>
          <input type="text" name="end_time" value="2021-01-01T00:00:00">
          <br><br>
          <input type="submit" value="Submit">
        </form>
        
        <p>After you submit, the form values are visible in the address bar of the current browser tab.</p>

        <hr>

        <h3>Description:</h3>
        <p>
        An API end point that will calculate the total number of South African business seconds between two
        <a href="https://en.wikipedia.org/wiki/ISO_8601">ISO 8601</a> formatted time strings.
        </p> 

        <h3>Brief:</h3>
        <p>
        Provide an API end point that will calculate the total number of business seconds between two given
        times. A business second is defined as any whole second that elapses after 08:00 and before 17:00 during a
        weekday (Monday - Friday) that is not a public holiday in the Republic of South Africa. The end point must
        support only list GET requests and must take two parameters: start_time and end_time. Parameter values will be
        in ISO-8601 format. You are guaranteed that start_time will be before end_time. The end point must respond with
        only a single integer value for successful requests or a suitable error message string for failed requests.
        </p>
        
        </body>
        </html>
    """


@app.route('/time_delta', methods=['GET'])
def get_time_delta_api():
    start_time = request.args.get('start_time', None)
    end_time = request.args.get('end_time', None)
    if start_time and end_time:
        # Sometimes '+' can come through to the GET request parameters as space
        start_time = start_time.replace(' ', '+')
        end_time = end_time.replace(' ', '+')
        try:
            return jsonify(get_time_delta(start_time, end_time))
        except ValueError as e:
            raise InvalidUsage(str(e), status_code=400)
    else:
        raise InvalidUsage(f'start_time: {start_time} and end_time: {end_time} invalid.', status_code=400)
