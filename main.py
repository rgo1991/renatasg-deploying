from flask import Flask, render_template, url_for
app = Flask(__name__)


posts = [
    {
        'author': '123',
        'title': '123',
        'content': '123',
        'date_posted': '123'
    },
    {
        'author': '123',
        'title': '123',
        'content': '123',
        'date_posted': '123'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')


if __name__ == '__main__':
    app.run(debug=True)

