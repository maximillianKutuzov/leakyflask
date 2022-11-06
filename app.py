import os

from flask import Flask, jsonify, render_template_string, request, Response, render_template
import subprocess
from werkzeug.datastructures import Headers
from werkzeug.utils import secure_filename
import sqlite3
import logging
import socket
import pickle


app = Flask(__name__, template_folder='static', static_folder='static')
app.config['UPLOAD_FOLDER'] = os.curdir
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000


@app.route("/")
def main_page():
    return render_template('index.html')


@app.route("/user/<string:name>")
def search_user(name):
    con = sqlite3.connect("app.db")
    cur = con.cursor()
    cur.execute(f"select * from gpg_keys")
    data = str(cur.fetchall())
    con.close()
    logging.basicConfig(filename="access_logs.log", filemode='w', level=logging.DEBUG)
    logging.debug(data)
    return jsonify(data=data), 200


@app.route("/welcome/<string:name>")
def welcome(name):
    data = "Welcome " + name
    return jsonify(data=data), 200


@app.route("/hello/<string:name>")
def hello_ssti(name):
    if request.args.get('name'):
        name = request.args.get('name')
    else:
        template = f'''
            <div>
            <h1>Hello {name}</h1>
            Here are the encrypt and decrypt commands
            <br>
            <h2>echo $1 | openssl aes-256-cbc -a -salt -pass pass:somepassword<h2/>
            <h2>echo $1 | openssl aes-256-cbc -d -a -pass pass:somepassword<h2/>
            <br>
            <br>
            <div style="position: absolute; bottom: 2px; background-color: white">
                U2FsdGVkX18V/yyuJHUwDXcKayEkCmR0fA+kdi+YR29/nCauaFUAtyEqBanCDpAe
            </div>
            </div>
        '''
        logging.basicConfig(filename="access_logs.log", filemode='w', level=logging.DEBUG)
        logging.debug(str(template))
        return render_template_string(template)


@app.route("/get_users")
def get_users():
    try:
        hostname = request.args.get('hostname')
        command = "dig " + hostname
        data = subprocess.check_output(command, shell=True)
        return data
    except:
        data = str(hostname) + "Could not find username"
        return data


@app.route("/get_log")
def get_log():
    try:
        command = "cat access_logs.log"
        data = subprocess.check_output(command, shell=True)
        return data
    except:
        return jsonify(data="Failed to execute"), 200


@app.route("/read_file/<string:filename>")
def read_file():
    filename = request.args.get('filename')
    file = open(filename, "r")
    data = file.read()
    file.close()
    logging.basicConfig(filename="access_logs.log", filemode='w', level=logging.DEBUG)
    logging.debug(str(data))
    return jsonify(data=data), 200


@app.route("/deserialization/")
def deserialization():
    try:
        HOST = "0.0.0.0"
        PORT = 8001
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            connection, address = s.accept()
            with connection:
                received_data = connection.recv(1024)
                data = pickle.loads(received_data)
                return str(data)
    except:
        return jsonify(data="Connect to port 8081"), 200


@app.route("/get_admin_mail/<string:control>")
def get_admin_mail(control):
    if control == "admin":
        data = "admin@spam.com"
        import logging
        logging.basicConfig(filename="access_logs.log", filemode='w', level=logging.DEBUG)
        logging.debug(data)
        return jsonify(data=data), 200
    else:
        return jsonify(data="Could not get admin details"), 200


@app.route("/run_file")
def run_file():
    try:
        filename = request.args.get("filename")
        command = "/bin/bash " + filename
        data = subprocess.check_output(command, shell=True)
        return data
    except:
        return jsonify(data="File failed to run"), 200


@app.route("/new_file")
def new_file():
    try:
        filename = request.args.get("filename")
        text = request.args.get("text")
        file = open(filename, "w")
        file.write(text)
        file.close()
        return jsonify(data="Created file"), 200
    except:
        return jsonify(data="Could not create file"), 200


connection = {}
max_con = 10


def factorial(number):
    if number == 1:
        return 1
    else:
        return number * factorial(number - 1)


@app.route('/factorial/<int:n>')
def factroial(n: int):
    if request.remote_addr in connection:
        if connection[request.remote_addr] > 2:
            return jsonify(data="Too many req."), 403
        connection[request.remote_addr] += 1
    else:
        connection[request.remote_addr] = 1
    result = factorial(n)
    if connection[request.remote_addr] == 1:
        del connection[request.remote_addr]
    else:
        connection[request.remote_addr] -= 1
    return jsonify(data=result), 200


@app.route('/login', methods=["GET"])
def login():
    username = request.args.get("user")
    passwd = request.args.get("password")
    if "admin" in username and "P@$$w0rd123" in passwd:
        return jsonify(data="Login successful"), 200
    elif "kevin" in username and "SamePAsswordDifferentDay!" in passwd:
        return jsonify(data="Login successful"), 200
    elif "cat" in username and "gr33n3gg$&$p@m" in passwd:
        return jsonify(data="Login successful"), 200
    else:
        return jsonify(data="Login unsuccessful"), 403


@app.route('/route')
def route():
    content_type = request.args.get("Content-Type")
    response = Response()
    headers = Headers()
    headers.add("Content-Type", content_type)
    response.headers = headers
    return response


@app.route('/logs')
def ImproperOutputNeutralizationforLogs():
    data = request.args.get('data')
    import logging
    logging.basicConfig(filename="access_logs.log", filemode='w', level=logging.DEBUG)
    logging.debug(data)
    return jsonify(data="Logging ok"), 200


@app.route("/user_pass_control")
def user_pass_control():
    import re
    username = request.form.get("username")
    password = request.form.get("password")
    if re.search(username, password):
        return jsonify(data="Password include username"), 200
    else:
        return jsonify(data="Password doesn't include username"), 200


@app.route('/upload', methods=['GET', 'POST'])
def uploadfile():
    import os
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File uploaded successfully'
    else:
        return '''
                <html>
                   <body>
                      <form  method = "POST"  enctype = "multipart/form-data">
                         <input type = "file" name = "file" />
                         <input type = "submit"/>
                      </form>   
                   </body>
                </html>
            '''


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8085)

