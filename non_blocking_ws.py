import json
import threading
import websocket

class NonBlockingWS:
    def __init__(self, ws_url: str, on_open = None, on_close = None, on_error = None, on_message = None):
        self.pub_array = []
        self.ws_url = ws_url
        self.on_open = on_open
        self.on_close = on_close
        self.on_error = on_error
        self.on_message = on_message
        
        self.ws: websocket.WebSocketApp = None
        
        #Setting up threads
        self.data_recv_thread = None
        
        #To close the threads
        self.isAlive = False


    def __initWS(self):
        try:
            self.ws = websocket.WebSocketApp(self.ws_url,
                                        on_open=self.__on_open,
                                        on_close=self.__on_close,
                                        on_error=self.__on_error,
                                        on_message=self.__on_message)

            self.ws.on_open = lambda ws: self.__start_publish_thread(ws)

            self.ws.run_forever()
            print("WebSocket connection closed. 2")
        except KeyboardInterrupt:
            self.ws.close()
            print("WebSocket connection closed due to keyboard interrupt.")
     
    def __on_open(self, ws):
        if self.on_open is not None:
            self.on_open()

    def __on_close(self, ws, close_status_code, close_msg):
        if self.on_close is not None:
            self.on_close(close_status_code, close_msg)

    def __on_error(self, ws, error):
        if self.on_error is not None:
            self.on_error(error)

    def __on_message(self, ws, message):
        if self.on_message is not None:
            self.on_message(message)
    
    def connect(self):
        self.isAlive = True
        #Starting recv thread
        self.data_recv_thread = threading.Thread(target=self.__initWS, args=())
        self.data_recv_thread.start()
    
    def terminate(self):
        self.isAlive = False
        self.ws.close(status=1002)
    
    def publish(self, data: dict):
        payload = json.dumps(data)
        self.ws.send(payload)