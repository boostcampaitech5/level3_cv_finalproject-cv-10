import cv2
import socket

# 서버 주소와 포트
server_address = ("server ip", "port")

# 웹캠 열기
cap = cv2.VideoCapture(0)

# 소켓 생성 및 연결
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

while True:
    # 프레임 읽기
    ret, frame = cap.read()

    # 프레임 전송

    # 프레임 인코딩 및 전송
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]  # JPEG 압축 설정
    result, encoded_frame = cv2.imencode(".jpg", frame, encode_param)
    if result:
        frame_data = encoded_frame.tobytes()
        client_socket.sendall(frame_data)

    # 프레임 디스플레이
    cv2.imshow("Local Webcam", frame)
    if cv2.waitKey(1) == ord("q"):
        break

# 리소스 해제
cap.release()
# 연결 종료
client_socket.close()
cv2.destroyAllWindows()
