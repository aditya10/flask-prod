from flask import Flask, jsonify, request
from fastai.text import *
from flair.models import TextClassifier
from flair.data import Sentence
import json
import heapq

app = Flask(__name__)

classifier_sentiment = TextClassifier.load('models/best-model.pt')


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/classify', methods=['POST'])
def post_tasks():
    return_object = []
    data = json.loads(request.data)
    df = pd.DataFrame(data)
    items = TextList.from_df(df[['sample']])
    learn = load_learner('models', 'export.pkl', test=items)
    preds = learn.get_preds(ds_type=DatasetType.Test)[0].tolist()
    preds = [get_classes(item) for item in preds]
    for indx, sample in enumerate(data, start=0):
        sample["categories"] = preds[indx]
        return_object.append(sample)
    return jsonify(return_object)


def get_classes(arr):
    ret = []
    classes = ['Accountability',
               'Autonomy',
               'Employee_motivation',
               'Great_communication',
               'Growth_and_development',
               'Management_skills',
               'Performance']
    sorted_biggest = heapq.nlargest(2, arr)
    for x in sorted_biggest:
        if x > 0.20:
            index = arr.index(x)
            ret.append([classes[index]][0])
    return ret


@app.route('/get_sentiment', methods=['POST'])
def sentiment_task():
    return_object = []
    data = json.loads(request.data)
    for sample in data:
        sentence = Sentence(sample["sample"])
        classifier_sentiment.predict(sentence)
        sample["sentiment"] = sentence.labels[0].to_dict()["value"]
        return_object.append(sample)
    return jsonify(return_object)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
