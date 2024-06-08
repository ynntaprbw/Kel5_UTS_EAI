from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import io

app = Flask(__name__)

# Konfigurasi SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://avnadmin:AVNS_7Y1EtTwPt_0DMWTF0AX@mysql-16d53072-ynntaprbw.d.aivencloud.com:24694/reviews'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

db = SQLAlchemy(app)

class Paket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paket = db.Column(db.String(255), nullable=False)
    destinasi_1 = db.Column(db.String(255), nullable=False)
    destinasi_2 = db.Column(db.String(255), nullable=False)
    destinasi_3 = db.Column(db.String(255), nullable=False)
    destinasi_4 = db.Column(db.String(255))
    destinasi_5 = db.Column(db.String(255))
    deskripsi_1 = db.Column(db.Text)
    deskripsi_2 = db.Column(db.Text)
    deskripsi_3 = db.Column(db.Text)
    deskripsi_4 = db.Column(db.Text)
    deskripsi_5 = db.Column(db.Text)

    def __repr__(self):
        return f"Paket(id={self.id}, paket='{self.paket}', destinasi_1='{self.destinasi_1}', destinasi_2='{self.destinasi_2}', destinasi_3='{self.destinasi_3}', destinasi_4='{self.destinasi_4}', destinasi_5='{self.destinasi_5}', deskripsi_1='{self.deskripsi_1}', deskripsi_2='{self.deskripsi_2}', deskripsi_3='{self.deskripsi_3}', deskripsi_4='{self.deskripsi_4}', deskripsi_5='{self.deskripsi_5}')"


# Model untuk review
class Ulasan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(255))
    tour = db.Column(db.String(255))
    rating = db.Column(db.Integer)
    date_go = db.Column(db.Date)
    go_with = db.Column(db.String(255))
    review = db.Column(db.Text)
    title_review = db.Column(db.String(255))
    image = db.Column(db.LargeBinary)  # Menggunakan LargeBinary untuk menyimpan data gambar

    def __repr__(self):
        return f"Ulasan('{self.nama}', '{self.tour}', '{self.rating}')"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return jsonify({'message': 'Selamat Datang di ALAMY Tour'}), 200

@app.route('/add_review', methods=['POST'])
def add_review():
    data = request.form

    # if 'image' not in request.files:
    #     return jsonify({'error': 'Image not provided'}), 400

    # file = request.files['image']
    
    # if file and allowed_file(file.filename):
    #     image_data = file.read()  # Baca file sebagai biner
    # else:
    #     return jsonify({'error': 'Invalid file type'}), 400

    review_data = Ulasan(
        nama=data.get('nama'),
        tour=data.get('tour'),
        rating = data.get('rating'),
        date_go=data.get('date_go'),
        go_with=data.get('go_with'),
        review=data.get('review'),
        title_review=data.get('title_review'),
        # image=image_data #default image=image_data
    ) 

    db.session.add(review_data)
    db.session.commit()

    return jsonify({'msg': 'Review added successfully', 'id': review_data.id}), 201

@app.route('/update_review/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    review = Ulasan.query.get(review_id)
    if review:
        data = request.form
        file = request.files.get('image')

        if file and allowed_file(file.filename):
            image_data = file.read()
        else:
            image_data = review.image

        review.nama = data.get('nama', review.nama)
        review.tour = data.get('tour', review.tour)
        review.rating = int(data.get('rating', review.rating))
        review.date_go = datetime.strptime(data.get('date_go'), '%Y-%m-%d').date() if data.get('date_go') else review.date_go
        review.go_with = data.get('go_with', review.go_with)
        review.review = data.get('review', review.review)
        review.title_review = data.get('title_review', review.title_review)
        review.image = image_data

        db.session.commit()

        return jsonify({'msg': 'Review updated successfully'}), 200
    else:
        return jsonify({'error': 'Review not found'}), 404

@app.route('/delete_review/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = Ulasan.query.get(review_id)
    if review:
        db.session.delete(review)
        db.session.commit()
        return jsonify({'msg': 'Review deleted successfully'}), 200
    else:
        return jsonify({'error': 'Review not found'}), 404

@app.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = Ulasan.query.all()
    serialized_reviews = []

    for review in reviews:
        serialized_review = {
            'id': review.id,
            'nama': review.nama,
            'tour': review.tour,
            'rating': review.rating,
            'date_go': review.date_go.strftime('%Y-%m-%d'),
            'go_with': review.go_with,
            'review': review.review,
            'title_review': review.title_review,
            'image': f'/review_image/{review.id}'  # URL untuk mengambil gambar
        }
        serialized_reviews.append(serialized_review)

    return jsonify(serialized_reviews), 200

@app.route('/review/<int:review_id>', methods=['GET'])
def get_review_by_id(review_id):
    review = Ulasan.query.get(review_id)
    if review:
        serialized_review = {
            'id': review.id,
            'nama': review.nama,
            'tour': review.tour,
            'rating': review.rating,
            'date_go': review.date_go.strftime('%Y-%m-%d'),
            'go_with': review.go_with,
            'review': review.review,
            'title_review': review.title_review,
            'image': f'/review_image/{review.id}'  # URL untuk mengambil gambar
        }
        return jsonify(serialized_review), 200
    else:
        return jsonify({'error': 'Review not found'}), 404

@app.route('/review_image/<int:review_id>', methods=['GET'])
def get_review_image(review_id):
    review = Ulasan.query.get(review_id)
    if review and review.image:
        return send_file(io.BytesIO(review.image), mimetype='image/png', as_attachment=False, download_name='image.png')
    else:
        return jsonify({'error': 'Image not found'}), 404

@app.route('/paket', methods=['GET'])
def get_paket():
    paket = Paket.query.all()
    serialized_pakets = []

    for i in paket:
        serialized_paket = {
            'id': i.id,
            'paket': i.paket,
            'destinasi_1': i.destinasi_1,
            'destinasi_2': i.destinasi_2,
            'destinasi_3': i.destinasi_3,
            'destinasi_4': i.destinasi_4,
            'destinasi_5': i.destinasi_5,
            'deskripsi_1': i.deskripsi_1,
            'deskripsi_2': i.deskripsi_2,
            'deskripsi_3': i.deskripsi_3,
            'deskripsi_4': i.deskripsi_4,
            'deskripsi_5': i.deskripsi_5
        }
        serialized_pakets.append(serialized_paket)
    
    return jsonify(serialized_pakets), 200

@app.route('/paket/<int:id>', methods=['GET'])
def get_paket_by_id(id):
    paket = Paket.query.get_or_404(id)
    serialized_paket = {
        'id': paket.id,
        'paket': paket.paket,
        'destinasi_1': paket.destinasi_1,
        'destinasi_2': paket.destinasi_2,
        'destinasi_3': paket.destinasi_3,
        'destinasi_4': paket.destinasi_4,
        'destinasi_5': paket.destinasi_5,
        'deskripsi_1': paket.deskripsi_1,
        'deskripsi_2': paket.deskripsi_2,
        'deskripsi_3': paket.deskripsi_3,
        'deskripsi_4': paket.deskripsi_4,
        'deskripsi_5': paket.deskripsi_5
    }
    return jsonify(serialized_paket), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)