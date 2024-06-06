from flask import Flask, jsonify, render_template, request, url_for
from werkzeug.utils import secure_filename
import requests
import os
from json.decoder import JSONDecodeError

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Define the folder to store uploaded images
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

########################## API RATING #####################

'''

app_id merupakan angka yang dicantumkan di url, logic sementara
selama url nya bener untuk akses api, ga harus ikutin dari nama id
masing masing api kayak ulasan_id atau pembelian_id

Kalau error kemungkinan memang untuk di ulasan dan pembelian butuh suatu
id yang di dua dua nya ada

'''

# fungsi untuk get rating + ulasan
def get_paket():
    response = requests.get("http://127.0.0.1:5001/paket")
    
    # Tambahkan pengecekan pada status kode dan tipe konten
    if response.status_code == 200 and response.headers['Content-Type'] == 'application/json':
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            print("Error decoding JSON")
            return None
    else:
        print(f"Error fetching data: {response.status_code}")
        return None
    
# fungsi untuk get rating + ulasan
def get_flight():
    response = requests.get("http://127.0.0.1:5004/flights")
    
    # Tambahkan pengecekan pada status kode dan tipe konten
    if response.status_code == 200 and response.headers['Content-Type'] == 'application/json':
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            print("Error decoding JSON")
            return None
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

# fungsi untuk get rating + ulasan
def get_ulasan():
    response = requests.get("http://127.0.0.1:5001/reviews")
    return response.json()

# fungsi untuk get rating + ulasan
def get_ulasan_gambar(image_id):
    response = requests.get(f"http://127.0.0.1:5001/review_image/{image_id}")
    return response.json()

# fungsi untuk get ulasan by id
def get_ulasan_id(review_id):
    response = requests.get(f"http://127.0.0.1:5001/reviews/{review_id}")
    return response.json()

# fungsi untuk post rating + ulasan
def post_ulasan():
    response = requests.post("http://127.0.0.1:5001/add_review")
    return response.json()

# fungsi untuk put rating + ulasan
def put_ulasan(review_id):
    response = requests.put(f'http://127.0.0.1:5001/update_review/{review_id}')
    return response.json()

# fungsi untuk delete rating + ulasan
def delete_ulasan(id):
    response = requests.delete(f'http://127.0.0.1:5001/delete_review/{id}')
    return response.json()


########################## API PEMBELIAN #####################

# fungsi untuk get data_pembelian
def get_pembelian():
    response = requests.get('http://localhost:5002/api/bookings')
    return response.json() # [] kalau mau nambahin kolom spesifik yang bakal di ambil

# fungsi untuk get gambar
def get_gambar():
    response = requests.get('http://localhost:5002/api/paymentproofs')
    return response.json()

# fungsi untuk post data_pembelian
def post_pembelian():
    response = requests.post(f'http://localhost:5002/api/bookings')
    return response.json()

# fungsi untuk post gambar
def post_gambar():
    response = requests.post('http://localhost:5002/api/upload')
    return response.json()
    
# fungsi untuk put data_pembelian
def put_pembelian():
    response = requests.put('http://localhost:5002/api/bookings')
    return response.json()

# fungsi untuk put gambar
def put_gambar():
    response = requests.put('http://localhost:5002/api/upload')
    return response.json()

# fungsi untuk delete data_pembelian
def delete_pembelian(id):
    response = requests.delete(f'http://localhost:5002/api/bookings/{id}')
    return response.json() # [] kalau mau nambahin kolom spesifik yang bakal di ambil

# fungsi untuk delete data_pembelian
def delete_gambar(id):
    response = requests.delete(f'http://localhost:5002/api/upload/{id}')
    return response.json() # [] kalau mau nambahin kolom spesifik yang bakal di ambil


########################## FUNGSI UTAMA PER ROUTE AN #####################

@app.route('/')
def all_get_methods():
    ulasan_get = get_ulasan()
    pembelian_get = get_pembelian()
    gambar_pembelian = get_gambar()
    flight_get = get_flight()

    paket_detail = None
    paket_id = request.args.get('paket_id')
    if paket_id:
        url = f'http://127.0.0.1:5001/paket/{paket_id}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            paket_detail = response.json()
        except requests.exceptions.RequestException as err:
            print(f"An error occurred: {err}")
            return "An error occurred", 500

    return render_template('main.html', ulasan=ulasan_get, beli=pembelian_get, gambar_pembelian=gambar_pembelian, paket_detail=paket_detail, flight=flight_get)

################################################################# FORM PEMBELIAN ##############################################################

@app.route('/booking', methods=['POST'])
def buat_pesanan():
    nama = str(request.form['nama'])
    email = str(request.form['email'])
    jml_tiket = int(request.form['jml_tiket'])
    no_hp = str(request.form['no_hp'])
    harga = int(request.form['harga'])

    if not (nama and email and jml_tiket and no_hp and harga):
        return "Invalid form data", 400
    
    # Debugging: Print the data to ensure it is correct
    print(f"Data yang dikirim: nama={nama}, email={email}, jml_tiket={jml_tiket}, no_hp={no_hp}, harga={harga}")

    url = 'http://localhost:5002/api/bookings'

    data = {
        'nama': nama,
        'email': email,
        'jml_tiket': jml_tiket,
        'no_hp': no_hp,
        'harga': harga
    }

    response = requests.post(url, json=data)
    print(f"Response status: {response.status_code}")
    print(f"Response content: {response.json()}")

    if response.status_code == 201:
        pembelian_get = get_pembelian()
        ulasan_get = get_ulasan()
        gambar_pembelian = get_gambar()

        return render_template('main.html', ulasan=ulasan_get, beli=pembelian_get, gambar_pembelian=gambar_pembelian)
    else:
        error_message = response.json().get('message', 'Gagal menyimpan data pembelian')
        return error_message, response.status_code

@app.route('/update-booking', methods=['PUT'])
def update_beli():
    # Mendapatkan data dari form
    nama = request.form.get('nama')
    email = request.form.get('email')
    jml_tiket = request.form.get('jml_tiket')
    no_hp = request.form.get('no_hp')
    harga = request.form.get('harga')

    # Memeriksa apakah semua data diterima
    if not (nama and email and jml_tiket and no_hp and harga) :
        return "Invalid form data", 400

    # Membuat dictionary data untuk dikirim ke server
    data = {
        'nama': nama,
        'email': email,
        'jml_tiket': jml_tiket,
        'no_hp': no_hp,
        'harga': harga,
    }

    # URL endpoint untuk mengupdate ulasan berdasarkan ID
    url = 'http://localhost:5002/api/bookings'

    try:
        # Mengirim permintaan PUT ke server dengan data ulasan
        response = requests.put(url, json=data)
        response.raise_for_status()  # Raises an HTTPError if the request returned an unsuccessful status code

        if response.status_code == 200:
            # Jika berhasil, ambil data terbaru dan tampilkan di halaman utama
            pembelian_get = get_pembelian()
            ulasan_get = get_ulasan()
            gambar_pembelian = get_gambar()

            return render_template('main.html', ulasan=ulasan_get, beli=pembelian_get, gambar_pembelian=gambar_pembelian)
        else:
            # Jika ada kesalahan, tangani kesalahan dari respons server
            error_message = response.json().get('message', 'Gagal memperbarui data ulasan')
            print(f"Error: {error_message}")
            return error_message, response.status_code

    except requests.exceptions.RequestException as err:
        # Tangani kesalahan koneksi atau permintaan
        print(f"An error occurred: {err}")
        return "An error occurred", 500
    

@app.route('/delete-pembelian', methods=['DELETE'])
def delete_beli():
    # URL endpoint untuk menghapus ulasan berdasarkan ID
    url = f'http://127.0.0.1:5002/api/bookings'

    try:
        # Mengirim permintaan DELETE ke server
        response = requests.delete(url)
        response.raise_for_status()  # Raises an HTTPError if the request returned an unsuccessful status code

        if response.status_code == 200:
            # Jika berhasil, ambil data terbaru dan tampilkan di halaman utama
            pembelian_get = get_pembelian()
            ulasan_get = get_ulasan()
            gambar_pembelian = get_gambar()

            return render_template('main.html', ulasan=ulasan_get, beli=pembelian_get, gambar_pembelian=gambar_pembelian)
        else:
            # Jika ada kesalahan, tangani kesalahan dari respons server
            error_message = response.json().get('message', 'Gagal menghapus data ulasan')
            print(f"Error: {error_message}")
            return error_message, response.status_code

    except requests.exceptions.RequestException as err:
        # Tangani kesalahan koneksi atau permintaan
        print(f"An error occurred: {err}")
        return "An error occurred", 500
    
################################################################ ULASAN #########################################################################

@app.route('/review/<int:id>', methods=['GET'])
def get_review_by_id(id):
    url = "http://127.0.0.1:5001/review/{}".format(id)

    response = requests.get(url)
    if response.status_code == 200:
            pembelian_get = get_pembelian()
            ulasan_get = get_ulasan()
            gambar_pembelian = get_gambar()

            return render_template('main.html', ulasan=ulasan_get, beli=pembelian_get, gambar_pembelian=gambar_pembelian)
    else:
        print("Error:", response.status_code)

@app.route('/ulasan', methods=['POST'])
def buat_ulasan():
    nama = request.form.get('nama')
    tour = request.form.get('tour')
    rating = request.form.get('rating')
    date_go = request.form.get('date_go')
    go_with = request.form.get('go_with')
    review = request.form.get('review')
    title_review = request.form.get('title_review')
    # image = request.files.get('image')

    if not (nama and tour and rating and date_go and go_with and review and title_review):
        return "Invalid form data", 400

    # image_path = None
    # if image and allowed_file(image.filename):
    #     filename = secure_filename(image.filename)
    #     image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    #     image.save(image_path)
    # elif image:
    #     print("Invalid file type")
    #     return "Invalid file type", 400

    # Gunakan nilai default kosong untuk image_path jika tidak ada file gambar

    data = {
        'nama': nama,
        'tour': tour,
        'rating': rating,
        'date_go': date_go,
        'go_with': go_with,
        'review': review,
        'title_review': title_review
        # 'image_path': image_path if image_path else ''
    }

    url = 'http://127.0.0.1:5001/add_review'

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()  # Raises an HTTPError if the request returned an unsuccessful status code

        if response.status_code == 201:
            pembelian_get = get_pembelian()
            ulasan_get = get_ulasan()
            gambar_pembelian = get_gambar()

            return render_template('main.html', ulasan=ulasan_get, beli=pembelian_get, gambar_pembelian=gambar_pembelian)
        else:
            error_message = response.json().get('message', 'Gagal menyimpan data ulasan')
            print(f"Error: {error_message}")
            return error_message, response.status_code

    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
        return "An error occurred", 500

@app.route('/update-ulasan/<int:id>', methods=['PUT'])
def update_ulasan(id):
    # Mendapatkan data dari form
    nama = request.form.get('nama')
    tour = request.form.get('tour')
    rating = request.form.get('rating')
    date_go = request.form.get('date_go')
    go_with = request.form.get('go_with')
    review = request.form.get('review')
    title_review = request.form.get('title_review')

    # Memeriksa apakah semua data diterima
    if not (nama and tour and rating and date_go and go_with and review and title_review):
        return "Invalid form data", 400

    # Membuat dictionary data untuk dikirim ke server
    data = {
        'nama': nama,
        'tour': tour,
        'rating': rating,
        'date_go': date_go,
        'go_with': go_with,
        'review': review,
        'title_review': title_review
    }

    # URL endpoint untuk mengupdate ulasan berdasarkan ID
    url = f'http://127.0.0.1:5001/update_review/{id}'

    try:
        # Mengirim permintaan PUT ke server dengan data ulasan
        response = requests.put(url, json=data)
        response.raise_for_status()  # Raises an HTTPError if the request returned an unsuccessful status code

        if response.status_code == 200:
            # Jika berhasil, ambil data terbaru dan tampilkan di halaman utama
            pembelian_get = get_pembelian()
            ulasan_get = get_ulasan()
            gambar_pembelian = get_gambar()

            return render_template('main.html', ulasan=ulasan_get, beli=pembelian_get, gambar_pembelian=gambar_pembelian)
        else:
            # Jika ada kesalahan, tangani kesalahan dari respons server
            error_message = response.json().get('message', 'Gagal memperbarui data ulasan')
            print(f"Error: {error_message}")
            return error_message, response.status_code

    except requests.exceptions.RequestException as err:
        # Tangani kesalahan koneksi atau permintaan
        print(f"An error occurred: {err}")
        return "An error occurred", 500

@app.route('/delete-ulasan/<int:id>', methods=['DELETE'])
def delete_ulasan(id):
    # URL endpoint untuk menghapus ulasan berdasarkan ID
    url = f'http://127.0.0.1:5001/delete_review/{id}'

    try:
        # Mengirim permintaan DELETE ke server
        response = requests.delete(url)
        response.raise_for_status()  # Raises an HTTPError if the request returned an unsuccessful status code

        if response.status_code == 204:
            # Jika berhasil, ambil data terbaru dan tampilkan di halaman utama
            pembelian_get = get_pembelian()
            ulasan_get = get_ulasan()
            gambar_pembelian = get_gambar()

            return render_template('main.html', ulasan=ulasan_get, beli=pembelian_get, gambar_pembelian=gambar_pembelian)
        else:
            # Jika ada kesalahan, tangani kesalahan dari respons server
            error_message = response.json().get('message', 'Gagal menghapus data ulasan')
            print(f"Error: {error_message}")
            return error_message, response.status_code

    except requests.exceptions.RequestException as err:
        # Tangani kesalahan koneksi atau permintaan
        print(f"An error occurred: {err}")
        return "An error occurred", 500

# Ini buat jalanin app.py nya
if __name__ == '__main__':
    app.run(debug=True, port=5000)

