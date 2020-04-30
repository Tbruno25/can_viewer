from flask import Flask, Response, render_template, session, request
from random import randint
import json
import time

app = Flask(__name__)


def event_stream():
    dic = {}
    while True:

        time.sleep(0.025)
        # Simulate random CAN msg
        id, dlc = randint(100, 120), randint(1, 8)
        data = " ".join([str(randint(20, 80)) for _ in range(dlc)])

        msg = {"id": id, "dlc": dlc, "data": data, "new_id": False}

        if not dic.get(id):
            dic[id] = True
            msg["new_id"] = True

        obj = json.dumps(msg)
        yield f"data:{obj}\n\n"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stream")
def stream():
    return Response(event_stream(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run()
