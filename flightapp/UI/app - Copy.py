from flask import Flask, render_template, request
from datetime import datetime
import requests

app = Flask(__name__)

# datetime_object = datetime.strptime


@app.route('/')
def home():
    return render_template('template.html')


@app.route('/submit', methods=['POST'])
def search():
        departure = str(request.form['departure'])
        destination = str(request.form['destination'])
        date = str(request.form['date'])
        if departure and destination and date:
            url = "http://localhost:5000/flights/from/{}/to/{}/on/{}".format(departure, destination, date)
            headers = {
                "Authorization": "justin",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                flight=response.json()
                flight=flight['data']
                return render_template('nyobaclick.html', data=flight,datetime=datetime)
                # Do something with the data
            else:
                print("Error:", response.status_code)
        elif departure and destination and not date:
            url = "http://localhost:5000/flights/from/{}/to/{}".format(departure, destination)
            headers = {
                "Authorization": "justin",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                flight=response.json()
                flight=flight['data']
                return render_template('nyobaclick.html', data=flight,datetime=datetime)
                # Do something with the data
            else:
                print("Error:", response.status_code)
        elif departure and not destination and date:
            url = "http://localhost:5000/flights/from/{}/on/{}".format(departure, date)
            headers = {
                "Authorization": "justin",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                flight=response.json()
                flight=flight['data']
                return render_template('nyobaclick.html', data=flight, datetime=datetime)
                # Do something with the data
            else:
                print("Error:", response.status_code) 
        elif departure and not destination and not date:
            url = "http://localhost:5000/flights/from/{}".format(departure)
            headers = {
                "Authorization": "justin",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                flight=response.json()
                flight=flight['data']
                return render_template('nyobaclick.html', data=flight, datetime=datetime)
                # Do something with the data
            else:
                print("Error:", response.status_code)   
        elif not departure and destination and date:
            url = "http://localhost:5000/flights/to/{}/on/{}".format(destination, date)
            headers = {
                "Authorization": "justin",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                flight=response.json()
                flight=flight['data']
                return render_template('nyobaclick.html', data=flight, datetime=datetime)
                # Do something with the data
            else:
                print("Error:", response.status_code) 
        elif departure and destination and not date:
            url = "http://localhost:5000/flights/to/{}".format(destination)
            headers = {
                "Authorization": "justin",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                flight=response.json()
                flight=flight['data']
                return render_template('nyobaclick.html', data=flight, datetime=datetime)
                # Do something with the data
            else:
                print("Error:", response.status_code) 
        elif not departure and not destination and date:
            url = "http://localhost:5000/flights/on/{}".format(date)
            headers = {
                "Authorization": "justin",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                flight=response.json()
                flight=flight['data']
                return render_template('nyobaclick.html', data=flight, datetime=datetime)
                # Do something with the data
            else:
                print("Error:", response.status_code)
        elif not departure and not destination and not date:
            url = "http://localhost:5000/flights".format(date)
            headers = {
                "Authorization": "justin",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                flight=response.json()
                flight=flight['data']
                return render_template('nyobaclick.html', data=flight, datetime=datetime)
                # Do something with the data
            else:
                print("Error:", response.status_code)

@app.route('/flights/<kode_penerbangan>')
def detail(kode_penerbangan):
    url = "http://localhost:5000/flights/{}".format(kode_penerbangan)
    headers = {
                "Authorization": "justin",
                "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        flight=response.json()
        flight=flight['data']
        return render_template('detail_pemesanan.html', data=flight, datetime=datetime)
                # Do something with the data
    else:
        print("Error:", response.status_code)   

# @app.route('/booking', methods=['POST'])
# def book():
#     totalHarga = str(request.form['hiddenTotalHarga'])
#     kodePenerbangan = str(request.form['hiddenKodePenerbangan'])
#     jumlahTiket = str(request.form['hiddenJumlahTiket'])

#     url = "http://localhost:5000/bookings/{}/{}/{}".format(totalHarga, kodePenerbangan, jumlahTiket)
#     headers = {
#             "Authorization": "justin",
#             "Content-Type": "application/json"
#         }
#     response = requests.post(url, headers=headers)
#     if response.status_code == 200:
#         return render_template('template.html')
#     else:
#         print("Error:", response.status_code)

@app.route('/booking', methods=['POST'])
def book():
    total_harga = request.form.get('hiddenTotalHarga')
    kode_penerbangan = request.form.get('hiddenKodePenerbangan')
    jumlah_tiket = request.form.get('jumlahTiket')

    if not (total_harga and kode_penerbangan and jumlah_tiket):
        return "Invalid form data", 400

    url = "http://localhost:5000/bookings/{}/{}/{}".format(total_harga,kode_penerbangan,jumlah_tiket)
    headers = {
            "Authorization": "justin",
            "Content-Type": "application/json"
        }
    response = requests.post(url, headers=headers)

    return render_template('template.html', response=response)
      


if __name__== '__main__':
    app.run(debug=True, port=5005)