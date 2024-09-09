class WebSocketSubscription(WebSocketClientProtocol):
    """_summary_

    Args:
        WebSocketClientProtocol (_type_): _description_
    """
    def __init__(self, callback=None):
        """_summary_

        Args:
            callback (_type_, optional): _description_. Defaults to None.
        """
        super().__init__()
        self.callback = callback
        WEBSOCKET_URL = config.get('websocket_url')
        self.factory = WebSocketClientFactory(WEBSOCKET_URL)
 
    def onConnect(self, response):
        """_summary_

        Args:
            response (_type_): _description_
        """
        print("Server connected: {0}".format(response.peer))
        logger.info(f"Server connected: {response.peer}")
 
    def onOpen(self):
        print("WebSocket connection open.")
        logger.info("WebSocket connection open.")
        TOPIC = config.get('topic')
        self.subscribe_to_topic(TOPIC)
 
    def subscribe_to_topic(self, topic):
        subscribe_message = {
 
            "method": "SUBSCRIBE",
            "params":[topic],
            "id": 1
        }
        self.sendMessage(json.dumps(subscribe_message).encode('utf8'))
        logger.info(f"Subscribed to topic: {topic}")
 
    def onMessage(self, payload, isBinary):
        if isBinary:
            message = f"Binary message received: {len(payload)} bytes"
        else:
            message = f"Text message received: {payload.decode('utf8')}"
        
        logger.info(message)
        
        # Invoke the callback if set
        if self.callback:
            self.callback(message)
 
    def onClose(self,wasClean, code, reason):
        print(f"WebSocket connection closed: {reason}")
        logger.error(f"WebSocket connection closed: {reason}")

    def onError(self, failure):
        print(f"WebSocket connection error: {failure}")
        logger.error(f"WebSocket connection error: {failure}")