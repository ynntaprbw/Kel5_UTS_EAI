from flask import Flask, render_template, request, send_file
from pymongo import MongoClient
from bson import Binary, ObjectId
import io

app = Flask(__name__)

# Initialize connection to MongoDB
client = MongoClient("localhost:27017")
db = client['reviews']
collection = db['datareviews']

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        # Ambil data dari form
        tour = request.form['tour']
        rating = request.form['rating']
        date_go = request.form['date_go']
        go_with = request.form['go_with']
        review_text = request.form['review']
        title_review = request.form['title_review']
        
        # Ambil file gambar jika ada
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                image_data = image_file.read()
                # Simpan gambar sebagai data biner di MongoDB
                image_doc = {'image': Binary(image_data), 'filename': image_file.filename}
                
                # Simpan data review dan gambar ke MongoDB
                review_doc = {
                    'tour': tour,
                    'rating': rating,
                    'date_go': date_go,
                    'go_with': go_with,
                    'review_text': review_text,
                    'title_review': title_review,
                    'image': image_doc
                }
                inserted_id = collection.insert_one(review_doc).inserted_id
                return f'Review and image uploaded successfully with ID: {inserted_id}'
    return 'No image selected for upload'

@app.route('/image/<image_id>')
def get_image(image_id):
    image_doc = collection.find_one({'_id': ObjectId(image_id)})
    if image_doc:
        image_data = image_doc['image']['image']
        return send_file(
            io.BytesIO(image_data), 
            mimetype='image/png'
        )
    return 'Image not found'

@app.route('/add_review', methods=['GET', 'POST'])
def add_review():
    if request.method == 'POST':
        # Ambil data dari form
        tour = request.form['tour']
        rating = request.form['rating']
        date_go = request.form['date_go']
        go_with = request.form['go_with']
        review_text = request.form['review']
        title_review = request.form['title_review']
        
        # Ambil file gambar jika ada
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                image_data = image_file.read()
                # Simpan gambar sebagai data biner di MongoDB
                image_doc = {'image': Binary(image_data), 'filename': image_file.filename}
                
                # Simpan data review dan gambar ke MongoDB
                review_doc = {
                    'tour': tour,
                    'rating': rating,
                    'date_go': date_go,
                    'go_with': go_with,
                    'review_text': review_text,
                    'title_review': title_review,
                    'image': image_doc
                }
                inserted_id = collection.insert_one(review_doc).inserted_id
                return render_template('reviews_view.html')

    return render_template('add_review_form.html')

@app.route('/reviews_view', methods=['GET'])
def reviews_view():
    # Ambil semua data ulasan dari MongoDB
    reviews_data = list(collection.find())
    return render_template('reviews_view.html', reviews_data=reviews_data)

if __name__ == '__main__':
    app.run(debug=True)
