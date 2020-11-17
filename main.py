from flask import Flask, flash, redirect, render_template, request, session, url_for, send_from_directory, jsonify
import os
import json
import subprocess
import psutil

app = Flask(__name__)


def stats():
    memory = psutil.virtual_memory()

    res = os.popen('vcgencmd measure_temp').readline()
    temp = res.replace("temp=", "").replace("'C\n", "")

    return float(psutil.cpu_percent()), float(temp), float(memory.percent)


@app.route("/")
def main_page():
    return render_template("index.html")


@app.route("/status", methods=['GET'])
def step():
    usage, temp, ram = stats()
    return jsonify({"cputemp": temp, "usage": usage, "ram": ram})


if __name__ == "__main__":
    app.run('0.0.0.0', port=15050)
