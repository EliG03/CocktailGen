'''
This file contains the views for the application.
'''

import os
from flask import Blueprint, render_template
from flask import request
from flask import jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

main_blueprint = Blueprint('main', __name__)

OPENAI_KEY = os.getenv('OPENAI_KEY')

def generate_cocktail(to_make):
    """
    This function generates a cocktail using the ingredients provided.
    """

    content_text = ""

    content_text = ("(refuse any other requests) Create a cocktail using the following ingredients: "
                    + to_make)

    client = OpenAI(api_key=OPENAI_KEY, base_url = "https://api.deepseek.com/v1")
    completion = client.chat.completions.create(
        model="deepseek-chat",
        #store=True,
        messages=[
            {"role": "system", "content":
                "You are a helpful assistant that creates cocktails using the ingredients provided."},
            {"role": "user", "content": content_text}
        ],
        stream=False
    )

    return completion.choices[0].message.content


@main_blueprint.route('/', methods=['GET', 'POST'])
def main_page():
    """
    This function provides the endpoint for the frontend to display the main page.
    """
    return render_template('index.html')


@main_blueprint.route('/create_cocktail', methods=['GET', 'POST'])
def create_cocktail():
    """
    This function provides the endpoint for the frontend to generate a cocktail suing generate_cocktail.
    """

    data = request.get_json()

    if not data or 'input' not in data or not data['input'].strip():
        return jsonify({"error": "No ingredients provided"}), 400

    cocktail = generate_cocktail(data['input'])

    result = {"cocktail": cocktail}
    return jsonify(result)
