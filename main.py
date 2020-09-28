from flask import Flask, flash, redirect, render_template, request, session, url_for, send_from_directory
import os
import json

app = Flask(__name__)


@app.route("/")
def main_page():
    return render_template("index.html")


@app.route("/status", methods=['GET'])
def step():
    import subprocess

    proc = subprocess.Popen([monPath], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print("program output:", out)

    return out


@app.route("/reset", methods=['POST'])
def reset_data():
    print("Done!")
    return redirect(url_for('supervise'))


# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    # monPath = os.path.join(app.root_path, 'static', "monitor.sh")
    monPath = "./monitor.sh"
    if not os.path.exists(monPath):
        with open(monPath, 'w') as f:
            f.write("#!/bin/sh\n\n")
            f.write("date=$(date '+%d/%m/%Y %H:%M:%S')\n")
            f.write("temp=$(vcgencmd measure_temp | egrep -o '[0-9]*\\.[0-9]*')\n")
            f.write("usage=$(top -bn 1 | head -n 3 | tail -n 1 | awk '{print 100-$8}')\n")
            f.write("tmp='${date};${temp};${usage}'\n")
            f.write("echo $tmp")

    app.static_folder = 'static'
    app.run('0.0.0.0', port=15050)
