from flask import Flask, request, render_template, send_file, session, redirect, url_for
from ultralytics.models.yolo import YOLO
import subprocess
import os
import datetime

app = Flask(__name__, static_url_path='/runs', static_folder='runs')
app.secret_key = 'your_secret_key'

image_raw = ""

def check_login():
    return 'username' in session


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index_edit_js.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Kiểm tra thông tin đăng nhập
        if username == 'phuongnam' and password == '123':
            session['username'] = username
            return render_template('index_edit_js.html')
        else:
            return render_template('login.html', login_fail=True)

    return render_template('login.html', login_fail=False)


@app.route('/#logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    global image_raw
    model_path = "best_yolom.pt"
    if 'image' in request.files:
        image_data = request.files['image'].read()

        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        image_name = f"Image_{timestamp}.jpg"

        # Đường dẫn lưu trữ ảnh
        image_raw = os.path.join('D:/yolov8/runs/detect/ReceiveFromRPI', image_name)

        # Lưu ảnh vào đường dẫn đã tạo
        with open(image_raw, 'wb') as f:
            f.write(image_data)

        return 'Upload success!'
    return 'Upload failed.'


@app.route('/get')
def get_images():
    image_paths = []
    image_results = []
    base_path = r'./runs/detect/ReceiveFromRPI'

    for file_name in os.listdir(base_path):
        if file_name.endswith('.jpg'):
            image_path = os.path.join(base_path, file_name)
            image_paths.append(image_path)

            model = YOLO('best_yolom.pt')
            model_path = 'D:/yolov8/best_yolom.pt'

            results = model.predict(image_path)
            names = model.names
            riped = 0
            unriped = 0
            late = 0
            early = 0

            for r in results:
                for c in r.boxes.cls:
                    if names[int(c)] == 'Riped':
                        riped += 1
                    if names[int(c)] == 'Unriped':
                        unriped += 1
                    if names[int(c)] == 'LateBlight':
                        late += 1
                    if names[int(c)] == 'EarlyBlight':
                        early += 1
            # Lưu thông tin của hình ảnh và kết quả vào danh sách image_results
            image_results.append((image_path, riped, unriped, late, early))
            command = f"yolo task=detect mode=predict model={model_path} source={image_path}"
            subprocess.run(command, shell=True)

    return render_template('Images_edit.html', image_results=image_results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)