import os
from flask import Flask
from routes import create_routes
from models import set_up_db

app = Flask(__name__)

set_up_db(app)
create_routes(app)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='127.0.0.1', port=port, debug=True)
