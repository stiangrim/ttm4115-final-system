from flask import Flask
from flask_restful import Resource, Api
from flask_mqtt import Mqtt
import json

app = Flask(__name__)
api = Api(app)

# === MOCK DATABASE ====
bathroom_queue = ["Anders", "Stian"]
users = {
    "Anders": "123",
    "Stian": "password1",
    "Dennis": "hunter2",
    "Miriam": "sol",
    "Aleksander": "pizza"
}

# === MQTT SETUP ===
app.config['MQTT_BROKER_URL'] = '127.0.0.1'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'user'
app.config['MQTT_PASSWORD'] = 'secret'
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
mqtt = Mqtt(app)


# === MQQT ===
def publish_queue():
    mqtt.publish("client", json.dumps(bathroom_queue))


def login(username, password):
    if password == users[username]:
        mqtt.publish("client", json.dumps("Login successful!"))
    else:
        mqtt.publish("client", json.dumps("Wrong username or password"))


def register_user(username, password):
    if username in users:
        mqtt.publish("client", json.dumps("User already exists. Try another username!"))
    else:
        users[username] = password
        mqtt.publish("client", json.dumps("User: {} registered successfully!".format(username)))


def add_user_to_queue(user):
    bathroom_queue.append(user)
    publish_queue()


def remove_user_from_queue(user):
    bathroom_queue.remove(user)
    return json.dumps(bathroom_queue)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('queue/#')
    mqtt.subscribe('queue')
    mqtt.subscribe('status')
    mqtt.subscribe('login')
    print('client connected')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode()
    if topic == "queue":
        publish_queue()
    elif topic == "queue/add":
        add_user_to_queue(payload)
    elif topic == "login":
        credentials = payload.split(":")
        login(credentials[0], credentials[1])
    elif topic == "register":
        credentials = payload.split(":")
        register_user(credentials[0], credentials[1])


if __name__ == '__main__':
    app.run(debug=True)
