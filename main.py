# coding=<UTF-8>

from flask import Flask, flash, redirect, render_template, request, session, url_for, send_from_directory, jsonify
import os
import json
import subprocess
from Plotter import Plotter


app = Flask(__name__)


def stats():
    proc = subprocess.Popen(["sudo " + monPath], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()

    with open(logPath, 'a') as f:
        f.write(str(out) + "\n")

    return out


@app.route("/")
def main_page():
    return render_template("index.html")


@app.route("/status", methods=['GET'])
def step():
    info = stats().split(";")
    return jsonify({"cputemp": float(info[1]), "usage": float(info[2])})


@app.route("/info")
def print_data():
    output = stats()

    plotter.do_plot()

    plotter.save(name="temps", format_="jpg")

    return render_template('info.html', data=output, plot="temps.jpg")

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    logPath = '.temp.log'
    # monPath = os.path.join(app.root_path, 'static', "monitor.sh")
    monPath = "./monitor.sh"
    if not os.path.exists(monPath):
        with open(monPath, 'w') as f:
            f.write("#!/bin/sh\n\n")
            f.write("date=$(date '+%d/%m/%Y %H:%M:%S')\n")
            f.write("temp=$(vcgencmd measure_temp | egrep -o '[0-9]*\\.[0-9]*')\n")
            f.write("usage=$(top -bn 1 | head -n 3 | tail -n 1 | awk '{print 100-$8}')\n")
            f.write("tmp=\"${date};${temp};${usage}\"\n")
            f.write("echo $tmp")

        os.system("chmod +x " + monPath)

    plotter = Plotter(log_file=logPath)

    app.static_folder = 'static'
    app.run('0.0.0.0', port=15050)
