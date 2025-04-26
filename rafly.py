from flask import Flask, render_template, request, redirect, jsonify
import csv
import random

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        title = request.form["title"]
        major = request.form["major"]
        status = request.form["status"]
        price = request.form["price"]
        contact = request.form["contact"]

        with open("books.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([name, title, major, status, price, contact])

        return render_template("add_book.html", message="Book added successfully!")

    return render_template("add_book.html")

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data["message"].lower()

    try:
        with open("books.csv", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            books = list(reader)
    except FileNotFoundError:
        books = []

    matched_books = []
    for book in books:
        if len(book) == 6:
            name, title, major, status, price, contact = book
            if major.lower() in user_msg:
                matched_books.append(book)

    if matched_books:
        response = "<strong>Here are the books we found for you:</strong><br><br>"
        for i, selected in enumerate(matched_books):
            whatsapp_link = f"https://wa.me/966{selected[5]}"
            book_info = (
                f"\ud83d\udcd8 <strong>Title:</strong> {selected[1]}<br>"
                f"\ud83d\udc64 <strong>Owner:</strong> {selected[0]}<br>"
                f"\ud83d\udcda <strong>Major:</strong> {selected[2]}<br>"
                f"\ud83d\udccc <strong>Status:</strong> {selected[3]}<br>"
                f"\ud83d\udcb0 <strong>Price:</strong> {selected[4]} SAR<br>"
                f"\ud83d\udcde <strong>Contact:</strong> +966{selected[5]}<br>"
                f"<a href='{whatsapp_link}' target='_blank'>💬 Contact via WhatsApp</a><br>"
            )
            response += f"<div id='book{i}'>{book_info}<button onclick=\"copyToClipboard('book{i}')\">📋 Copy Info</button><span id='msg{i}' style='color:green; display:none;'> ✔ Copied!</span><br><br></div>"
        response += """
        <script>
        function copyToClipboard(id) {
            const text = document.getElementById(id).innerText;
            navigator.clipboard.writeText(text).then(() => {
                const msgId = 'msg' + id.replace('book', '');
                const msgEl = document.getElementById(msgId);
                msgEl.style.display = 'inline';
                setTimeout(() => { msgEl.style.display = 'none'; }, 2000);
            });
        }
        </script>"""
    else:
        response = (
            "Sorry, I couldn't find a matching book,"
            "Try asking about another book."
        )

    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(debug=True)

