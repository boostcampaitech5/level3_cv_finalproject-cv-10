import cv2
import socket
import numpy as np


# 서버 주소와 포트
server_address = ("0.0.0.0", "port")

# 소켓 생성 및 바인딩
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)

# 클라이언트 연결 대기
server_socket.listen(1)
print("Waiting for client connection...")

# 클라이언트 소켓 수락
client_socket, client_address = server_socket.accept()
print("Client connected:", client_address)

# 비디오 스트림 수신 및 디스플레이
while True:
    # 프레임 데이터 수신
    frame_data = b""
    while True:
        data = client_socket.recv(4096)

        if not data:
            break
        frame_data += data

    # 수신된 프레임 디코딩
    frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)

    # 프레임 디스플레이
    cv2.imshow("Received Frame", frame)
    if cv2.waitKey(1) == ord("q"):
        break

# 리소스 해제
client_socket.close()
server_socket.close()
cv2.destroyAllWindows()
