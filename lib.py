import threading
import argparse
from pythonosc import udp_client, osc_server, dispatcher

def set_osc():
  # 中央集権サーバー用のデータ転送
  clientServer = udp_client.SimpleUDPClient("192.168.50.152", 8000)
  # 描画用のTouchDesigner
  clientTD = udp_client.SimpleUDPClient("127.0.0.1", 7000)

  return clientServer, clientTD