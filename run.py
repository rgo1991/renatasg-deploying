# Import the app construct (That is made from Flask in __init__.py)
from main import app

if __name__ == '__main__':
    app.run(debug=True)

