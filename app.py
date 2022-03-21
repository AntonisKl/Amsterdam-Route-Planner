from flask import Flask, jsonify, request, render_template
# from joblib import dump, load
from map import *

# import speech_recognition as sr
# import pyaudio
# from audio import speech2text
# import speech_recognition as sr
# import pyaudio

# from test import *


# d = app.data['traffic_gdf'] = traffic_gdf


# recognizer = sr.Recognizer()
# microphone = sr.Microphone()
# with microphone as source:
#     recognizer.adjust_for_ambient_noise(source)
#     audio = recognizer.listen(source)
#     command = recognizer.recognize_google(audio)
#     print(command)


app = Flask(__name__)


@app.route('/result', methods=['POST', 'GET'])
def result():
    # if request.method == 'POST':
    #    result = request.form
    # return render_template("result.html",result = result)
    return render_template('index.html')


@app.route('/')
def hello():
    # return "hello"
    # d = app.data['traffic_gdf'] = traffic_gdf
    return m._repr_html_()


# The above function returns the HTML code to be displayed on the page

@app.route('/incomes')
def get_incomes():
    return jsonify(incomes)


@app.route('/incomes', methods=['POST'])
def add_income():
    incomes.append(request.get_json())
    return '', 204


if __name__ == '__main__':
    app.run()
