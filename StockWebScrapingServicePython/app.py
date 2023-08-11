from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False


@app.route('/', methods=['GET'])
def get_test():
    return 'Successful'


if __name__ == '__main__':
    app.run()
