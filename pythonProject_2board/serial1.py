import serial

# 시리얼 포트 설정 (적절한 포트를 선택하세요)
ser = serial.Serial('/dev/tty0', 9600, timeout=1)


# 데이터 전송 및 수신 함수
def send_and_receive():
    while True:
        # 사용자 입력
        data_to_send = input("Enter data to send: ")

        # 데이터 전송
        ser.write(data_to_send.encode())

        # 데이터 수신
        data_received = ser.readline().decode('utf-8').strip()

        print("Data received from Nucleo: ", data_received)


# 시리얼 통신 시작
send_and_receive()