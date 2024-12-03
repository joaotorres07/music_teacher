import os
import openai
from flask import Flask, render_template, request

application = Flask(__name__, template_folder=os.environ['TEMPLATE_PATH'])

openai.api_key = os.environ["GPT_KEY"]

@application.route("/", methods=["GET", "POST"])
def index():
    response= ""
    if request.method == "POST":
        user = request.form["user_question"]
        prompt = f"You: {user} \n English Teacher: "
        response = call_gpt(prompt)

    return render_template("index.html", response=response)


def call_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a music teacher, anwser in English"},
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
            temperature=0.7,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error in communication with teacher, try again in fell minutes. Error: {str(e)}"


application.run(debug=True)