from flask import Flask, Response, render_template, session, request
from random import randint
import json
import time

app = Flask(__name__)


def event_stream():
    data_dic = {}
    while True:

        time.sleep(0.005)
        # Simulate random CAN msg
        id, dlc = randint(100, 120), randint(1, 8)
        bytes = " ".join([str(randint(20, 80)) for _ in range(dlc)])

        event = "update"
        msg = {"id": id, "dlc": dlc, "bytes": bytes}

        if not data_dic.get(id):
            event = "new_id"

        data_dic[id] = msg
        data = json.dumps(msg) if event == "update" else json.dumps(data_dic)
        yield f"event:{event}\ndata:{data}\n\n"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stream")
def stream():
    return Response(event_stream(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run()
