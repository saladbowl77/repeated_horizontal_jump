import threading
import argparse
from pythonosc import udp_client, osc_server, dispatcher

def set_osc(set_status):
  # 中央集権サーバー用のデータ転送
  clientServer = udp_client.SimpleUDPClient("192.168.50.152", 8000)
  # 描画用のTouchDesigner
  clientTD = udp_client.SimpleUDPClient("127.0.0.1", 7000)

  # TouchDesignerからのデータ受信用
  # dispatcher_td = dispatcher.Dispatcher()
  # def td_k(address, *args):
  #   set_status(args[0])
  # dispatcher_td.map("/k", td_k)  # /filter というアドレスのメッセージを td_k に割り当てる
  # server = osc_server.ForkingOSCUDPServer(('127.0.0.1', 10001), dispatcher_td)
  # print("Serving on {}",format(server.server_address))
  # server_thread = threading.Thread(target=server.serve_forever)
  # server_thread.start()

  return clientServer, clientTD