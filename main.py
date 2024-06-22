from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def load_books():
    with open('bookshelf.json', 'r') as file:
        books = json.load(file)
    return books

def filter_books(title, author, genre, read_status, publish_year, goodreads_rating):
    books = load_books()
    matching_books = []
    for book_title, book_info in books.items():
        if (title.lower() in book_title.lower() or not title) \
           and (author.lower() in book_info['author'].lower() or not author) \
           and (genre.lower() in book_info['genre'].lower() or not genre) \
           and (read_status.lower() in book_info['read_status'].lower() or not read_status) \
           and (str(publish_year) in str(book_info['publication_year']) or not publish_year) \
           and (float(book_info['goodreads_rating']) >= float(goodreads_rating) or not goodreads_rating):
            book_info['title'] = book_title  # Add the title to the book info
            matching_books.append(book_info)
    return matching_books

@app.route('/search', methods=['GET'])
def search_books():
    title = request.args.get('title', '')
    author = request.args.get('author', '')
    genre = request.args.get('genre', '')
    read_status = request.args.get('read_status', '')
    publish_year = request.args.get('publish_year', '')
    goodreads_rating = request.args.get('goodreads_rating', '')

    try:
        matching_books = filter_books(title, author, genre, read_status, publish_year, goodreads_rating)
        return jsonify(matching_books)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/submit_recommendation', methods=['POST'])
def submit_recommendation():
    title = request.form.get('title')
    author = request.form.get('author')

    with open('recommendations.txt', 'a') as file:
        file.write(f"Title: {title}, Author: {author}\n")

    return 'Recommendation submitted successfully!'

if __name__ == '__main__':
    app.run(debug=True)
