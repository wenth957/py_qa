from flask import Flask, render_template
from flask import request, jsonify
from models.TextClassification import TextClassification
from models.QuestionTemplate import QuestionTemplate

app = Flask(__name__)
template = QuestionTemplate()
question_classify = TextClassification()


def get_response(question):
    template_id = question_classify.predict(question)
    print(template_id)
    result = template.get_answer(question, template_id[0])
    return result


@app.get('/')
def index_get():
    return render_template('index.html')


@app.post("/predict")
def predict():
    question = request.get_json().get("message")
    response = get_response(question)
    message = {"answer": response}
    return jsonify(message)


def start_server():
    app.run(debug=True, use_reloader=False)
