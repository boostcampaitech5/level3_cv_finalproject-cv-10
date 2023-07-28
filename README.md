# Advanced Pedestrian Assistance system (APAS)

https://project-apas.streamlit.app/

## 🔎 프로젝트 소개

1. 프로젝트 개요
    
    차량을 위한 자율 주행 시스템은 이미 많이 개발되어 왔다. 이에 관점을 바꿔 차량을 위한 자율 주행 시스템이 아닌, 시각 장애인 등 보행에 어려움을 겪는 사람들을 위한 자율 주행시스템을 개발하고자 하였다. 
    
    AI 기술의 도움으로 보행에 위협 요소인 각종 장애물(자동차, 사람, 가로수, 가로등 등)을 피해 보다 안전하고 원할하게 이동할 수 있는 방안을 제시하였다.
    
    스마트폰을 목걸이에 걸고 거리를 걸어다니며, 카메라 기능과 연동된 웹을 통해 보행자 전방에 탐지되는 객체들의 위험 정도를 인식하여 사용자에게 알리고, 사전에 피해갈 수 있도록 돕는 매커니즘을 구현하는 것이 목적이다.
    
2. 기대 효과
    
    사회적 측면 : 눈이 잘 안보이는 보행자들에게 보다 안전한 보행 환경을 제공해줄 수 있다.
    
    기술적 측면 : 배송 로봇을 포함한 다양한 기기에서 활용 가능할 수 있다.
    
<br/>

## 🪛 기능 소개

1. 온라인
    - 실시간으로 카메라 데이터를 활용하여 전방에 장애물이 있는지 탐지하는 기능이다.
2. 오프라인
    - 이미지/영상을 넣어 모델의 결과가 어떻게 나오는지 확인해볼 수 있는 기능이다.
    
<br/>

## 🖼️ 서비스 아키텍쳐

<img width="1344" alt="APAS architecture" src="https://github.com/boostcampaitech5/level2_cv_semanticsegmentation-cv-10/assets/50127209/9d22a937-3435-46f4-b912-1df78b5f00a1">

<br/>

## 🛠️ 사용 기술 소개

1. **streamlit / streamlit cloud**
    - 별도의 어플을 깔지 않고 웹으로 기능을 체험해보기 위해 웹으로 구현하고자 하여 streamlit을 활용하였다.
    - 원격 호스트에서 로컬 디바이스에 접근하기 위해서 getUserMedia() API를 사용하는데, 이는 HTTPS 서빙을 필요로 한다. streamlit community cloud는 기본적으로 HTTPS로 서빙이 가능하여 사용하였다.

2. **streamlit webrtc**
    - realtime inference를 수행하기 위해 서버와 클라이언트 사이의 소켓 전송 방식을 사용해 프레임을 실시간 전송하는 기능을 사용 → 클라이언트에서 전송 코드를 실행해야하는 문제점이 발생
    - 빠른 통신과 유저의 편의성을 위해 webrtc 기능을 탑재한 streamlit-webrtc 라이브러리를 활용하였다.
    - webrtc의 video frame callback을 커스터마이징하여 활용하여 매 프레임 탐지된 위험물을 warning level에 맞춰 bbox를 출력하도록 하였다.
    - 추가로 50프레임마다 현재의 위험물의 개수, 거리에 따라 warning mode 여부를 탐지하고 사용자에게 음성 TTS파일로 알림을 제공하였다.

3. **warning algorithm**
    - 위험도와 방향에 우선순위를 두어 알림을 제공하고자 warning system을 개발하였다.
    - 거리에 따라 사다리꼴 모양으로 구획선을 나눈 후, 각도에 따라 진행 방향 상 충돌 가능 영역을 설정하였다.
    - 위험도를 분석하여 가장 위험도가 높은 물체를 유저에게 tts로 알려준다.
    - 탐지된 사람의 수에 따라 warning mode와 normal mode로 나누어 추가적인 정보를 제공하였다.

<br/>


## 👨‍👨‍👧‍👦 Members


| 이름 | github | 맡은 역할 |
| --- | --- | --- |
| 김보경 &nbsp;| [github](https://github.com/bogeoung) | Streamlit web/app 구현, realtime inference 설계 및 구현|
| 양재민 | [github](https://github.com/Yang-jaemin) | Data 전처리, Warning system algorithm Logic 설계 |
| 임준표 | [github](https://github.com/anonlim) | Data 전처리, Warning system algorithm Logic 설계 |
| 정남교 | [github](https://github.com/jnamq97) | Streamlit web/app 구현, realtime inference 설계 및 구현|
<br/>


