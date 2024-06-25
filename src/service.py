from flask import Flask
from endpoints.item import item

app = Flask(__name__)
app.register_blueprint(item)

if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0', debug=True)