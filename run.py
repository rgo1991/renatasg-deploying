# Import the app construct (That is made from Flask in __init__.py)
from main import create_app

# You can pass in an argument to this function to initialize app with any config file.
# If you dont specify anything it will use the default value
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

