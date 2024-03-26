from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

# Load data
popular_df = pd.read_pickle('popular.pkl') 
pt = pd.read_pickle('pt.pkl')
similarity_scores =pd.read_pickle('similarity.pkl')
books = pd.read_pickle('books.pkl')

@app.route('/')
def index():
    return jsonify({
        'book_name': popular_df['Book-Title'].values.tolist(),
        'author': popular_df['Book-Author'].values.tolist(),
        'image': popular_df['Image-URL-M'].values.tolist(),
        'votes': popular_df['Num-Rating'].values.tolist(),
        'rating': popular_df['Avg-Rating'].values.tolist()
    })



@app.route('/api/recommend', methods=['POST'])
def recommend():
    try:
        book_name = request.json.get('bookName')
        index = np.where(pt.index==book_name)[0][0]
        # print(book_name)
        similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:6]

        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            data.append(item)
        print(data)
        return jsonify({"recommendedBooks":data})
    except Exception as e:
        print("Error occurred:", e)
        return jsonify({"Error":str(e)}),500

if __name__ == '__main__':
    app.run(debug = True)
