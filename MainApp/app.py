from flask import Flask, jsonify,render_template
import requests

app = Flask(__name__)

def getDestinasi():
    response = requests.get('http://localhost:8000/api/destinasi')
    return response.json()

def getReviewsView():
    response = requests.get('http://localhost:5000/reviews_view')
    return response.text

@app.route('/cobagabung')
def FungsiDestinasi():
    destinasi_data = getDestinasi()
    reviews_html = getReviewsView()
    return render_template('index.html', destinasi_data=destinasi_data, reviews_html=reviews_html)

if __name__ == "__main__":
    app.run(debug=True, port=8080)