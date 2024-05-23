from flask import Flask, jsonify,render_template
import requests

app = Flask(__name__)

def getDestinasi():
    try:
        response = requests.get('http://localhost:8000/api/destinasi')
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        destinasi_data = data['data']  # Mengambil hanya bagian 'data' dari respons
        return destinasi_data
    except requests.exceptions.RequestException as e:
        print('Error fetching data:', e)
        return None

def tiket():
    response = requests.get('http://localhost:8000/api/tiket')
    return response.text

def getReviewsView():
    response = requests.get('http://localhost:5000/reviews_view')
    return response.text

def getform():
    response = requests.get('http://localhost:5000/add_review')
    return response.text

@app.route('/tes')
def tes():
    form = getform()
    return render_template('contact.html', form = form)


@app.route('/cobagabung')
def FungsiDestinasi():
    destinasi_data = getDestinasi()
    reviews_html = getReviewsView()
    return render_template('index.html', destinasi_data=destinasi_data, reviews_html=reviews_html )


if __name__ == "__main__":
    app.run(debug=True, port=8080)
