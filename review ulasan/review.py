from flask import Flask, render_template, request, redirect, url_for, send_file
from pymongo import MongoClient
from bson import Binary, ObjectId
import io

app = Flask(__name__)

# Initialize connection to MongoDB
client = MongoClient("localhost:27017")
db = client['reviews']
collection = db['datareviews']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' in request.files:
        image_file = request.files['image']
        if image_file.filename != '':
            image_data = image_file.read()
            # Store image as binary data in MongoDB
            image_doc = {'image': Binary(image_data), 'filename': image_file.filename}
            inserted_id = collection.insert_one(image_doc).inserted_id
            return redirect(url_for('reviews_view'))  # Redirect to reviews_view after upload
    return 'No image selected for upload'

@app.route('/image/<review_id>')
def get_image(review_id):
    review_doc = collection.find_one({'_id': ObjectId(review_id)})
    if review_doc and 'image' in review_doc:
        image_data = review_doc['image']
        return send_file(
            io.BytesIO(image_data),
            mimetype='image/jpeg'  # Ubah mimeType sesuai kebutuhan
        )
    return 'Image not found'

@app.route('/add_review', methods=['GET', 'POST'])
def add_review():
    if request.method == 'POST':
        nama = request.form.get('nama', 'N/A')
        tour = request.form.get('tour', 'N/A')
        rating = request.form.get('rating', 'N/A')
        date_go = request.form.get('date_go', 'N/A')
        go_with = request.form.get('go_with', 'N/A')
        review = request.form.get('review', 'N/A')
        title_review = request.form.get('title_review', 'N/A')

        review_data = {
            'nama' : nama,
            'tour': tour,
            'rating': rating,
            'date_go': date_go,
            'go_with': go_with,
            'review': review,
            'title_review': title_review
        }

        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                image_data = image_file.read()
                review_data['image'] = Binary(image_data)  # Simpan gambar dalam dokumen review_data
                review_data['filename'] = image_file.filename

        # Simpan review_data ke dalam koleksi MongoDB
        collection.insert_one(review_data)

        # Tampilkan review_data di console untuk memeriksa isinya
        print(review_data)

        return render_template('success.html', review_data=review_data)

    else:
        return render_template('add_review_form.html')

@app.route('/reviews_view', methods=['GET'])
def reviews_view():
    reviews_data = list(collection.find())
    return render_template('reviews_view.html', reviews_data=reviews_data)

@app.route('/delete_review/<review_id>', methods=['POST'])
def delete_review(review_id):
    # Find review by ID
    review = collection.find_one({'_id': ObjectId(review_id)})
    if review:
        # If review found, delete the review
        collection.delete_one({'_id': ObjectId(review_id)})
        return redirect(url_for('reviews_view'))
    else:
        # If review not found, display message that review not found
        return 'Review not found'
    
if __name__ == '__main__':
    app.run(debug=True)
