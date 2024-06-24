from flask import Flask
from src.endpoints import item

app = Flask(__name__)
app.register_blueprint(item)

app.run(port=5000, host='0.0.0.0', debug=True)
