from app import app
from settings import config
from apiv1 import blueprint
import os


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', '5000'))
