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

if __name__ == '__main__':
    app.run(debug=True, port=5001)