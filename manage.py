from jobplus.app import create_app
from jobplus.models import db


app = create_app('test')

if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=True)
