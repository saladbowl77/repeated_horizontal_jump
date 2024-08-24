# repeated_horizontal_jump
反復横跳びを検知するPythonのプログラムです。

## 仕組み
MediaPipe Poseを活用して、反復横跳びの回数を計測するコードです。  
体のポイントが左・真ん中・右のどこに一番多いかを計算し、一番多かったポイントを現在の位置として計測します。  

これらのデータは回数が増えたタイミングでインクリメントされ、中央のサーバー並びに表示用のTouchDesignerにOSC経由で飛び各種処理が行われます。

## 実行方法
仮想環境としてvenvを活用してください

```shell
python3 -m venv .venv
. ./venv/bin/activate
pip install -r requirements.txt
```

## インストール物
実行に必要なパッケージ類は`requirements.txt`にまとめてあります。

```shell
pip install -r requirements.txt
```

上記のコードでインストールをしてください。