from flask import Blueprint,request,jsonify
from middleware.auth import authenticate_token

books_bp=Blueprint("books",__name__)

books=[]   #in memory storage
# Middleware :token authentication check
# before request build in app

@books_bp.before_request
def before_request():
    authenticate_token()

# Get endpoint to fetch all todos item
@books_bp.route("/", methods=["GET"])
def get_books():
    return jsonify(books)



@books_bp.route("/<int:id>", methods=["GET"])
def get_book(id):
    book = next((b for b in books if b["id"] == id), None)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book)


@books_bp.route("/completed/<bool:completed_status>", methods=["GET"])
def get_books_by_completed(completed_status):
    filtered_books = [b for b in books if b["completed"] == completed_status]
    return jsonify(filtered_books)


@books_bp.route("/title/<string:title>", methods=["GET"])
def get_book_by_title(title):
    book = next((b for b in books if b["title"].lower() == title.lower()), None)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book)

# post endpoint to create a new todo item

@books_bp.route("/", methods=["POST"])
def create_book():
    book = {
        "id": len(books) + 1,
        "title": request.json.get("title"),
        "completed": request.json.get("completed", False)
    }
    books.append(book)
    return jsonify(book), 201


# PUT endpoint to update
@books_bp.route("/<int:id>", methods=["PUT"])
def update_book(id):
    book = next((t for t in books if t["id"] == id), None)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    book["title"] = request.json.get("title", book["title"])
    book["completed"] = request.json.get("completed", book["completed"])
    return jsonify(book)
# Delete todo item

@books_bp.route("/<int:id>",methods=["DELETE"])
def delete_book(id):
    global books
    books=[t for t in books if t["id"]!=id]
    return '',204

