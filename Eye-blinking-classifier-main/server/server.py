import argparse
import os

import numpy as np
np.bool = bool
import pandas as pd

from flask import Flask
from flask_cors import CORS
from flask_restful import Resource
from flask_restful import Api
from flask import jsonify, make_response, send_file

cwd = os.getcwd()

from transformers import pipeline, set_seed
generator = pipeline('text-generation', model='gpt2')
set_seed(42)



class GetHelp(Resource):

    def get(self, 
            emotion, 
            ):

        response = ""


        # if emotion == "Angry":
        #     response = "Calm down"
        # elif emotion == "Disgust":
        #     response = "Don't worry"
        # elif emotion == "Fear":
        #     response = "You are okay"
        # elif emotion == "Happy":
        #     response = "You are fine"
        # elif emotion == "Neutral":
        #     response = "You are fine"
        # elif emotion == "Sad":
        #     response = "Do something fun"
        # elif emotion == "Surprise":
        #     response = "You are fine"

        prompt = f"This is a conversation between a friendly, professional therapist and a human user.\n\nHuman: I am feeling {emotion.lower()}.\n\nTherapist: Try to"

        response = generator(prompt, max_length=100, num_return_sequences=1)

        response = response[0]['generated_text'].replace(prompt, "")

        response = response.split("\n")[0]

        return jsonify({
            'result': response
        })


def create_app():
    app = Flask(__name__)  # static_url_path, static_folder, template_folder...
    CORS(app, resources={r"/*": {"origins": "*", "allow_headers": "*"}})


    api = Api(app)

    api.add_resource(GetHelp, "/api/<string:emotion>")

    @app.route('/version')
    def version():
        return f"Job ID: {os.environ['JOB_ID']}\nCommit ID: {os.environ['COMMIT_ID']}"

    return app


def start_server():
    print("Starting server...")
    parser = argparse.ArgumentParser()

    # API flag
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="The host to run the server",
    )
    parser.add_argument(
        "--port",
        default=8000,
        help="The port to run the server",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Run Flask in debug mode",
    )

    args = parser.parse_args()

    server_app = create_app()

    server_app.run(debug=args.debug, host=args.host, port=args.port)


if __name__ == "__main__":
    start_server()
