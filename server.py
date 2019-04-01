from flask import Flask
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)

# === MOCK DATABASE ====
bathroom_queue = ["Anders", "Stian"]


# === REST API ===
@app.route('/')
def index():
    return "<a href='/api/queue'>Check queue</a> "


@app.route('/api/queue')
def get_queue():
    return json.dumps(bathroom_queue)


@app.route('/api/queue/add/<user>')
def add_user_to_queue(user):
    bathroom_queue.append(user)
    return json.dumps(bathroom_queue)


@app.route('/api/queue/remove/<user>')
def remove_user_from_queue(user):
    bathroom_queue.remove(user)
    return json.dumps(bathroom_queue)


if __name__ == '__main__':
    app.run(debug=True)
