from flask import Flask
from flask_restful import Resource, Api
from flask_mqtt import Mqtt
import json

app = Flask(__name__)
api = Api(app)

app.config['MQTT_BROKER_URL'] = '127.0.0.1'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'user'
app.config['MQTT_PASSWORD'] = 'secret'
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
mqtt = Mqtt(app)

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


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('queue')
    mqtt.subscribe('status')
    print('client connected')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print(data)
    if data["topic"] == "queue":
        print(get_queue())


if __name__ == '__main__':
    app.run(debug=True)
