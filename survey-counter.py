from flask import Flask,request,jsonify
from flask_cors import CORS,cross_origin
import matplotlib.pyplot as plt
from io import BytesIO
import seaborn as sns
import base64

def count_responses(question):
    responses = question['response']
    answer_count = {answer: responses.count(answer) for answer in question['answers']}
    sorted_answers = sorted(answer_count.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_answers)

def plot_to_base64(question):
    responses = count_responses(question)
    sns.barplot(x=list(responses.values()), y=list(responses.keys()), palette='coolwarm')
    plt.title(question['question'])
    plt.xlabel('Cevaplar')
    plt.ylabel('Sayı')
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    return image_base64


app = Flask(__name__)
cors = CORS(app, resources={r"/": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/',methods=['GET','POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def main():
    if request.method == 'POST':
        try:
            data = dict(request.get_json())

            plotList = []

            for q in data['questions']:
                plotList.append(plot_to_base64(q))

            response = {
                'plots': plotList
            }


            return jsonify(response)
        except:
            return 'This is an count api'

    if request.method == 'GET':
        return 'This is an count api'


