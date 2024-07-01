import cv2
import numpy as np
import mediapipe as mp
import time

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
movenet = mp_pose.Pose(static_image_mode=False, model_complexity=1)

cap = cv2.VideoCapture(1)

beforePosition = 'C'
count = []

while True:
  # 各種変数のリセット
  nowPosition = ""
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
      beforePosition = nowPosition

  # 画面に反復横跳びの回数を表示
  font = cv2.FONT_HERSHEY_SIMPLEX
  text = f"count : {len(count)} / position : {nowPosition}"
  text_size = cv2.getTextSize(text, font, 2, 3)[0]  # フォントサイズ: 2, 太さ:3
  text_x = frame.shape[1] - text_size[0] - 10  # 右端から10ピクセル左
  text_y = text_size[1] + 10  # 上端から10ピクセル下
  cv2.putText(frame, text, (text_x, text_y), font, 2, (0, 0, 0), 3, cv2.LINE_AA)  # フォントサイズ: 2, 太さ:3

  
  # 映像の表示
  cv2.imshow('MoveNet', frame)

  # 'r'キーでリセット, 'q'キーで終了
  if cv2.waitKey(1) & 0xFF == ord('r'):
    beforePosition = 'C'
    count = []

  if cv2.waitKey(1) & 0xFF == ord('q'):
      break

cap.release()
cv2.destroyAllWindows()