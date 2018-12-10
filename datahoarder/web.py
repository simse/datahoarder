import threading

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from datahoarder.source import *
from datahoarder.download import get_download_status
from datahoarder.run import sync

app = Flask(__name__)
CORS(app)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

ui_file_dir = 'datahoarder-ui/dist/'
ui_path = ui_file_dir


class WebThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self, name='WebThread')

    def run(self):
        app.run(host='0.0.0.0', port=4040)


def error_response(error, message):
    return jsonify({"error": error, "error_msg": message}), 500


@app.route('/')
def index():
    return 'Hello world!'


@app.route('/ui', methods=['GET'])
def serve_dir_directory_index():

    return send_from_directory(ui_path, 'index.html')


@app.route('/ui/<path:path>', methods=['GET'])
def serve_file_in_dir(path):
    if not os.path.isfile(os.path.join(ui_path, path)):
        path = os.path.join(path, 'index.html')

    return send_from_directory(ui_path, path)


@app.route('/api/get-active-sources')
def active_sources():
    return jsonify(get_active_sources())


@app.route('/api/get-available-sources')
def available_sources():
    return jsonify(get_available_sources())


@app.route('/api/add-source')
def add_source():
    source = request.args['source']
    args = request.args.get('args')

    # The following two checks are technically ignored
    if source is None:
        return error_response('NO_SOURCE_DEFINED', 'You must define a source to add one.')

    # If no arguments are provided, assume quick add
    if args is None:
        source_info = get_info_from_source(source)

        # Make sure source exists
        if not source_info:
            return error_response('SOURCE_NOT_FOUND', 'This source does not exist. Did you mistype?')

        args = {}

        for arg in source_info['args']:
            args[arg] = source_info['args'][arg]['default']

    # Add to config
    config['sources'][source] = args
    save_config(config)

    sync()

    return jsonify({'status': 'OK'})


@app.route('/api/remove-source')
def delete_source():
    source = request.args.get('source_id')

    if remove_source(source):
        return jsonify({'status': 'OK'})
    else:
        return error_response('SOURCE_NOT_REMOVED', 'An error happened when removing the source.')


@app.route('/api/download-status')
def download_status():
    if get_download_status() is {}:
        return {}

    return jsonify(get_download_status()[:10])


@app.route('/api/sync')
def sync_now():
    sync()

    return jsonify({'status': 'OK'})


@app.route('/api/test')
def test():
    get_available_sources()

    return 'hello'
