import socket
import fcntl
import struct
from flask import Flask, render_template, Response, request
import cv2
import threading
import serial

app = Flask(__name__)
capture = cv2.VideoCapture(-1)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
###two board
# 시리얼 포트 설정 (뉴클레오 보드와 통신)
ser_1 = serial.Serial('/dev/ttyACM1', 9600, timeout=1)  # 첫 번째 보드
ser_2 = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # 두 번째 보드

@app.route('/command/<cmd>', methods=['POST'])
def command(cmd):
    if cmd in ['i', 'j', 'k', 'l']:  # 첫 번째 보드 명령
        ser_1.write((cmd + '\n').encode())
        response = ser_1.readline().decode().strip()
        return f"Sent command {cmd} to board 1, Response: {response}"
    elif cmd in ['w', 'a', 's', 'd', 'x']:  # 두 번째 보드 명령
        ser_2.write((cmd + '\n').encode())
        response = ser_2.readline().decode().strip()
        return f"Sent command {cmd} to board 2, Response: {response}"
    else:
        return "Invalid command", 400

@app.route('/speed/<int:value>', methods=['POST'])
def set_speed(value):
    # 속도 값을 0-100 범위로 받아서 0-5 단계로 변환하여 전송
    if 0 <= value <= 20:
        speed_level = 'y'
    elif 21 <= value <= 40:
        speed_level = 'u'
    elif 41 <= value <= 60:
        speed_level = 'i'
    elif 61 <= value <= 80:
        speed_level = 'o'
    elif 81 <= value <= 100:
        speed_level = 'p'
    else:
        return "Invalid speed value", 400

    ser_2.write((speed_level + '\n').encode())
    response = ser_2.readline().decode().strip()
    return f"Speed set to level: {speed_level} on board 2, Response: {response}"

def gen_frames():
    while True:
        success, frame = capture.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip = socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', b'wlan0'[:15])
    )[20:24])
    return ip

def start_tcp_server(ip):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, 9999))
    server_socket.listen(1)
    print("TCP server listening on port 9999")
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        client_socket.send(ip.encode('utf-8'))
        client_socket.close()

if __name__ == "__main__":
    ip_address = get_ip_address()
    print(f"IP Address: {ip_address}")

    tcp_thread = threading.Thread(target=start_tcp_server, args=(ip_address,))
    tcp_thread.start()

    app.run(host="0.0.0.0", port=5000)
