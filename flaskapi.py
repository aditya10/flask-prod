from flask import Flask, jsonify, request
from fastai.text import load_learner
import json
import heapq

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

app = Flask(__name__)
learn = load_learner('', 'export.pkl')

@app.route('/classify', methods=['POST'])
def post_tasks():
    classes = ['Accountability',
               'Autonomy',
               'Employee_motivation',
               'Great_communication',
               'Growth_and_development',
               'Management_skills',
               'Performance']

    data = json.loads(request.data)
    sample = data["sample"]
    prediction_array = (learn.predict(sample)[2]).tolist()
    sorted_biggest = heapq.nlargest(2, prediction_array)
    prediction = dict()
    prediction["sample"] = sample
    prediction["categories"] = {}
    for x in sorted_biggest:
        index = prediction_array.index(x)
        prediction["categories"][classes[index]] = x
    prediction = json.dumps(prediction)
    return jsonify(prediction)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    