from flask import Flask, jsonify, request, render_template, flash

from config import flask_secret_key
# from joblib import dump, load
from map import accessibility_gdf, traffic_gdf, walkability_gdf, current_crowd_prediction_gdf, create_map_with_features
import folium
from route_planning import find_route

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
app.config['SECRET_KEY'] = flask_secret_key


@app.route('/', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        destination = request.form['destination']

        if not destination:
            flash('Destination is required.')
        else:
            folium_map = create_map_with_features(False, False, False, False)
            try:
                find_route(folium_map, destination, request.form.get('avoid_low_accessibility'),
                           request.form.get('avoid_traffic'), request.form.get('avoid_low_walkability'),
                           request.form.get('avoid_crowd'), accessibility_gdf, traffic_gdf,
                           walkability_gdf,
                           current_crowd_prediction_gdf)
            except KeyError:
                flash('Error while trying to convert destination to coordinates. Please try a more specific one.')
    else:
        folium_map = create_map_with_features()

    folium.LayerControl(collapsed=False).add_to(folium_map)

    return render_template('index.html', map=folium_map._repr_html_())

    # return render_template('index.html')


#
# @app.route('/')
# def hello():
#     # return "hello"
#     # d = app.data['traffic_gdf'] = traffic_gdf
#     return m._repr_html_()


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
