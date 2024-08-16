import cv2
import numpy as np
import mediapipe as mp
import time

import argparse
from pythonosc import udp_client

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
movenet = mp_pose.Pose(static_image_mode=False, model_complexity=1)

parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1",
    help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=8080,
    help="The port the OSC server is listening on")
args = parser.parse_args()

client = udp_client.SimpleUDPClient(args.ip, args.port)

cap = cv2.VideoCapture(1)

beforePosition = 'C'
count = []

while True:
  # 各種変数のリセット
  nowPosition = ""
  nowHand = ""
  # カメラからの映像を取得
  ret, frame = cap.read()

  # BGRをRGBに変換
  image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

  # 骨格検出の実行
  results = movenet.process(image)

  # 骨格情報の表示
  mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
  
  # 点のx軸をプリント
  poses = [0, 0, 0, 0]
  if results.pose_landmarks:
    # 各点の位置を取得

    # 左腕の肩と肘の位置を取得
    left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
    left_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
    # 右腕の肩と肘の位置を取得
    right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    right_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]

    # nowHandで送るのは左右が反転するので、プログラム上のleftとRightが逆になる
    if left_elbow.y < 0.7 and left_shoulder.y > left_elbow.y:
      nowHand = "R"
    # 右腕が上げているかどうか判定
    elif right_elbow.y < 0.7 and right_shoulder.y > right_elbow.y:
      nowHand = "L"
      
    for id, landmark in enumerate(results.pose_landmarks.landmark):
      # 各点の位置がどの場所にあるのか配列に追加し確認する
      if landmark.x < 0.333:
        poses[0] += 1
      elif landmark.x < 0.666:
        poses[1] += 1
      elif landmark.x < 1:
        poses[2] += 1
      # 全部でなんぼの点があるか確認する
      poses[3] += 1
          
    # 現在の体の位置を判定
    # 配列に入ったpositionのデータがどの場所に一番多いか判定する
    leftSide = poses[0] / poses[3]
    center = poses[1] / poses[3]
    rightSide = poses[2] / poses[3]
    position = max(leftSide, center, rightSide)

    # 現在のポジションを設定
    if position == leftSide:
      nowPosition = "L"
    elif position == center:
      nowPosition = "C"
    else:
      nowPosition = "R"

    if nowPosition != beforePosition:
      nowtime = int(time.time() * 1000)
      count.append({"time" : nowtime, "pos": nowPosition})
      if nowHand == "L":
        client.send_message("/increment", 0)
      elif nowHand == "R":
        client.send_message("/increment", 1)
      else:
        client.send_message("/increment", 2)
      beforePosition = nowPosition

  # 画面に反復横跳びの回数を表示
  font = cv2.FONT_HERSHEY_SIMPLEX
  text = f"count : {len(count)} / position : {nowPosition}"
  text_size = cv2.getTextSize(text, font, 4, 3)[0]  # フォントサイズ: 4, 太さ:3
  text_x = frame.shape[1] - text_size[0] - 10  # 右端から10ピクセル左
  text_y = text_size[1] + 10  # 上端から10ピクセル下
  cv2.putText(frame, text, (text_x, text_y), font, 4, (0, 0, 0), 3, cv2.LINE_AA)  # フォントサイズ: 4, 太さ:3
  cv2.putText(frame, nowHand, (text_x, text_y + text_size[1] + 10), font, 4, (0, 0, 0), 3, cv2.LINE_AA)  # フォントサイズ: 4, 太さ:3

  
  # 映像の表示
  # cv2.namedWindow('MoveNet', cv2.WINDOW_NORMAL)
  # cv2.setWindowProperty('MoveNet', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
  cv2.imshow('MoveNet', frame)

  # 'r'キーでリセット, 'q'キーで終了
  if cv2.waitKey(1) & 0xFF == ord('r'):
    beforePosition = 'C'
    count = []

  if cv2.waitKey(1) & 0xFF == ord('q'):
      break

cap.release()
cv2.destroyAllWindows()


# 送信するデータは反復横跳びでincrementされた時に、右か左かどっちの手を上げているのかというデータさえ送れば良い
