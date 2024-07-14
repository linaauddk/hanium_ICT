import serial
import time

# 시리얼 포트 설정
ser = serial.Serial('/dev/serial0', 9600, timeout=1)
time.sleep(2)  # 시리얼 포트가 안정화될 때까지 대기

try:
    while True:
        # 사용자로부터 입력받기
        data_out = input("Enter data to send: ")
        ser.write(data_out.encode())  # 데이터를 Nucleo 보드로 전송
        time.sleep(1)

        # Nucleo 보드로부터 데이터 수신
        if ser.in_waiting > 0:
            data_in = ser.readline().decode('utf-8').rstrip()
            print("Received:", data_in)
except KeyboardInterrupt:
    print("Communication stopped")
finally:
    ser.close()