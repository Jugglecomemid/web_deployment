import numpy as np
from flask import Flask, request, jsonify, render_template, url_for
from tqdm import tqdm
from trans_model import Zh2yue

app = Flask(__name__)
# model = pickle.load(open('model.pkl', 'rb'))
model = Zh2yue(vacob_input='static/translation_model/zh2yue/cmn_input.txt',
               vacob_output='static/translation_model/zh2yue/cmn_output.txt',
               model_path='static/translation_model/logs/model-zh2yue-300')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    int_features = [str(x) for x in request.form.values()]
    int_str = "".join(int_features)
    result = model.predict(int_str)

    # final_features = [np.array(int_features)]
    # prediction = model.predict(final_features)

    # output = round(prediction[0], 2)

    return render_template('index.html', prediction_text='Result: {}'.format(result))


@app.route('/results', methods=['POST'])
def results():
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
