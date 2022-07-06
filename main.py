from flask import Flask,request,jsonify
from flask_basicauth import BasicAuth
import os
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from textblob import TextBlob

modelo = pickle.load(open('models/modelo.pkl','rb'))
columnas = ['area','modelo','estacionamiento']

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')
basic_auth = BasicAuth(app)

@app.route('/')

def home():
    return 'Esta es mi primera API.'

@app.route('/sentimiento/<frase>')
@basic_auth.required
def sentimiento(frase):
    tb = TextBlob(frase)
    tb_en = tb.translate(from_lang='es', to='en')
    polaridad = tb_en.sentiment.polarity
    return f'La polaridad de la frase es: {polaridad}'

@app.route('/precio_casas/', methods=['POST'])
@basic_auth.required
def precio_casas():
    datos= request.get_json()
    datos_input = [datos[col] for col in columnas]
    precio = modelo.predict([datos_input])
    return jsonify(precio=precio[0])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')