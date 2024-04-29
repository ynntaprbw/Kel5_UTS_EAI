from flask import Flask, render_template 
from flask import jsonify
from flask import request
from flask_mysqldb import MySQL
import base64

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tugas_eai'


# Definisikan filter base64_encode untuk Flask
def base64_encode(blob_data):
    return base64.b64encode(blob_data).decode('utf-8')

# Tambahkan filter ke Jinja2
app.jinja_env.filters['base64_encode'] = base64_encode


#Tampilan Halaman Utama untuk menambah keluhan
@app.route('/')
def index():
    return render_template('index.html')

mysql = MySQL(app)

@app.route('/add_review', methods=['GET', 'POST'])
def add_review():
    if request.method == 'POST':
        try:
            nama = request.form['nama']
            tour = request.form['tour']
            rating = request.form['rating']
            date_go = request.form['date_go']
            go_with = request.form['go_with']
            review = request.form['review']
            title_review = request.form['title_review']
            photos = request.form['photos']

            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO add_reviews (nama,tour, rating, date_go, go_with, review, title_review, photos) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
               (nama, tour, rating, date_go, go_with, review, title_review, photos))
            mysql.connection.commit()
            cursor.close()

            return render_template('success.html')
        except Exception as e:
            return jsonify({'error': str(e), 'status_code': 500})

    else:
        return render_template('add_review_form.html')


@app.route('/reviews_view', methods=['GET'])
def reviews_view():
    try:
        # Membuka koneksi ke database
        cursor = mysql.connection.cursor()

        # Mengambil data review dari database
        cursor.execute("SELECT nama, tour, rating, date_go, go_with, review, title_review, photos FROM add_reviews")

        # Fetch data review
        reviews_data = cursor.fetchall()

        # Menutup kursor
        cursor.close()

        # Render template HTML dan kirim data review ke template
        return render_template('reviews_view.html', reviews_data=reviews_data)
    except Exception as e:
        # Menangani kesalahan jika terjadi
        return jsonify({'error': str(e), 'status_code': 500})


    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50, debug=True)