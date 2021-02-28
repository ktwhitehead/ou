from websocket import WebSocket
from .over_under.crawler import Crawler as OverUnderCrawler

class Runner:
  def __init__(self):
    self.socket = WebSocket()
    self.socket.start()
    self.over_under_crawler = OverUnderCrawler(self.socket)

  def start_over_under(self):
    self.over_under_crawler.start()

  def stop_over_under(self):
    self.over_under_crawler.stop()
