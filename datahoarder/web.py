import os

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from datahoarder.source import *
from datahoarder.download import get_download_status
from datahoarder.run import sync

app = Flask(__name__)
CORS(app)

# Disable Flask logging
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Find UI path
ui_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
ui_path += os.path.sep + 'datahoarder-ui' + os.path.sep + 'dist'


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
    args = None

    if request.args.get('args') is not None:
        args = json.loads(request.args.get('args'))

    # The following two checks are technically ignored
    if source is None:
        return error_response('NO_SOURCE_DEFINED', 'You must define a source to add one.')

    # If no arguments are provided, assume quick add
    if args is None:
        source_args = Source(source).arguments

        args = {}

        for arg in source_args:
            args[arg] = source_args[arg]['default']

        Source(source).create_path()

    # Add to config
    config['sources'][source] = args
    save_config(config)

    sync()

    return jsonify({'status': 'OK'})


@app.route('/api/remove-source')
def delete_source():
    source = request.args.get('source_id')

    if Source(source).remove():
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
