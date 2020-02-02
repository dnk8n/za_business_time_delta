from flask import Flask, request

from .za_business_time_delta.za_business_time_delta import get_time_delta

app = Flask(__name__)


@app.route('/time_delta', methods=['GET'])
def get_time_delta_api():
    start_time = request.args.get('start_time', '')
    end_time = request.args.get('end_time', '')
    return str(get_time_delta(start_time, end_time))
