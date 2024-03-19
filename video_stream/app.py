from pathlib import Path, PurePath
from flask import Flask, render_template, request, Response

credential = {}
filenames = []

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('signup.html')

@app.route('/credential', methods=["POST"])
def authenticate():
    global credential
    username = request.form["username"]
    password = request.form["password"]
    credential.update({username:password})
    return render_template('login.html')

@app.route('/stream', methods=["POST"])
def stream_page():
    global credential
    global filenames
    username = request.form["username"]
    password = request.form["password"]
    if username in credential and credential[username] == password:
       # List of filenames
       filenames = ["dora1.mp4","toy.mp4","littleangel.mp4","dora2.mp4","powerranger.mp4"]
       return render_template('index.html', filenames=filenames)
    return render_template('login.html')


@app.route('/static/<path:filename>')
def stream(filename):
    def generate():
        with open(Path(filename), 'rb') as f:
            while True:
                chunk = f.read(1024)
                if not chunk:
                    break
                yield chunk

    return Response(generate(), mimetype='video/mp4')

@app.route('/create_file_web', methods=["POST"])
def create_file():
    global filenames
    file = request.files["file"]
    filename = file.filename
    root_path = Path().absolute()
    file_path = str(PurePath(root_path,"static",filename))
    file.save(file_path)
    filenames.append(filename)
    return render_template('index.html', filenames=filenames)

@app.route('/create_file', methods=["POST"])
def create_file_api():
    global filenames
    file = request.files["file"]
    filename = file.filename
    root_path = Path().absolute()
    file_path = str(PurePath(root_path,"static",filename))
    file.save(file_path)
    filenames.append(filename)
    return {"status":200, "message":fr"The {filename} has been successfully uploads"}

@app.route('/delete_file_web', methods=["POST"])
def delete_file():
    global filenames
    filename = request.form["filename"]
    root_path = Path().absolute()
    file_path = Path(str(PurePath(root_path,"static",filename)))
    if file_path.is_file():
       file_path.unlink()

    if filename in filenames:
       filenames.remove(filename)
    return render_template('index.html', filenames=filenames)

@app.route('/delete_file', methods=["POST"])
def delete_file_api():
    global filenames
    filename = request.form["filename"]
    root_path = Path().absolute()
    file_path = Path(str(PurePath(root_path,"static",filename)))
    if file_path.is_file():
       file_path.unlink()

    if filename in filenames:
       filenames.remove(filename)
    return {"status":200, "message":fr"The {filename} has been successfully deleted"}

@app.route('/modify_file_web', methods=["POST"])
def modify_file():
    global filenames
    filename = request.form["filename"]
    root_path = Path().absolute()
    file_path = Path(str(PurePath(root_path,"static",filename)))
    if file_path.is_file():
       file_path.unlink()

    if filename in filenames:
       filenames.remove(filename)

    file = request.files["file"]
    filename = file.filename
    root_path = Path().absolute()
    file_path = str(PurePath(root_path,"static",filename))
    file.save(file_path)
    filenames.append(filename)

    return render_template('index.html', filenames=filenames)

@app.route('/modify_file', methods=["POST"])
def modify_file_api():
    global filenames
    filename_mod = request.form["filename"]
    root_path = Path().absolute()
    file_path = Path(str(PurePath(root_path,"static",filename_mod)))
    if file_path.is_file():
       file_path.unlink()

    if filename_mod in filenames:
       filenames.remove(filename_mod)

    file = request.files["file"]
    filename = file.filename
    root_path = Path().absolute()
    file_path = str(PurePath(root_path,"static",filename))
    file.save(file_path)
    filenames.append(filename)

    return {"status":200, "message":fr"The {filename} has been successfully modified"}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, threaded=True, debug=True)
