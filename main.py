import cv2
import numpy as np
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
movenet = mp_pose.Pose(static_image_mode=False, model_complexity=1)

cap = cv2.VideoCapture(1)

while True:
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
      for id, landmark in enumerate(results.pose_landmarks.landmark):
          # print(f"ランドマーク {id} の x 座標: {landmark.x}")
          if landmark.x < 0.333:
            poses[0] += 1
          elif landmark.x < 0.666:
            poses[1] += 1
          elif landmark.x < 1:
            poses[2] += 1

          poses[3] += 1
            
      leftSide = poses[0] / poses[3]
      center = poses[1] / poses[3]
      rightSide = poses[2] / poses[3]
      
      position = max(leftSide, center, rightSide)
      if position == leftSide:
        print("左側")
      elif position == center:
        print("真ん中")
      else:
        print("右側")
    
    # 映像の表示
    cv2.imshow('MoveNet', frame)

    # 'q'キーで終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()