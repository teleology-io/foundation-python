import websocket
import requests
import json
import threading
from typing import Optional, Callable

def realtime(self):
    ws = websocket.WebSocketApp(self.socketUrl, on_message=self._on_message, on_close=self._on_close)
    ws.run_forever(reconnect=5)

class Foundation:
    def __init__(self, url: str, apiKey: str, uid: Optional[str] = None):
        self.url = url
        self.apiKey = apiKey
        self.uid = uid
        self.config = None
        self.environment = None
        self.variables = {}
        self.callback = None
        self.socketUrl = f"{url}/v1/realtime?apiKey={apiKey}".replace("http", "ws")
        self.client = requests.Session()
        self.client.headers.update({'X-Api-Key': apiKey})

        t = threading.Thread(name='realtime', target=realtime, args=[self])
        t.start()

    def getEnvironment(self):
        if not self.environment:
            response = self.client.get(f"{self.url}/v1/environment")
            if response.status_code == 200:
                self.environment = response.json()
            else:
                raise Exception(response.json())
            
        return self.environment

    def getConfiguration(self):
        if not self.config:
            response = self.client.get(f"{self.url}/v1/configuration")
            if response.status_code == 200:
                result = response.json()
                if response.headers.get('Content-Type') == 'application/json':
                    self.config = json.loads(result['content'])
                else:
                    self.config = result['content']
            else:
                raise Exception(response.json())
            

        return self.config

    def getVariable(self, name: str, uid: Optional[str] = None, fallback=None):
        if name in self.variables:
            return self.variables[name]['value']
    
        response = self.client.post(f"{self.url}/v1/variable", json={ 'name': name, 'uid': uid or self.uid })
        if response.status_code == 200:
            self.variables[name] = response.json()
            return self.variables[name]['value']
        elif response.status_code == 404:
            return fallback
        else:
            raise Exception(response.json())

    def subscribe(self, cb: Callable[[Optional[str], any], None]):
        self.callback = cb

    def _on_message(self, ws, message):
        try:
            data = json.loads(message)
            event = data.get('type')
            if event == 'variable.updated':
                name = data['payload']['name']

                self.variables.pop(name, None)
                self.getVariable(name)
                
                if self.callback is not None:
                    self.callback(event, self.variables[name])
            elif event == 'configuration.published':
                self.config = None

                if self.callback is not None:
                    self.callback(event, self.getConfiguration())
            elif event == 'environment.updated':
                self.environment = None
                
                if self.callback is not None:
                    self.callback(event, self.getEnvironment())
        except Exception as e:
            return

    def _on_close(self, ws):
        ws.run_forever()
       