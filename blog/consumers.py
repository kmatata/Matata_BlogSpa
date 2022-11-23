from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from . import actions

class BlogConsumer(JsonWebsocketConsumer):
    room_name = "streams"

    def connect(self):
        #accept socket connect
        self.accept()
        # assign streams room name
        async_to_sync(self.channel_layer.group_add)(self.room_name,self.channel_name)

    def disconnect(self, code):
        pass

    def receive_json(self, data_received):
        # get the data
        data = data_received['data']
        match data_received["action"]:
            case "Change page":
                actions.send_page(self, data)
            case "Add next posts":
                actions.add_next_posts(self, data)

    def send_html(self,event):
        """event: send html to client"""
        data = {
            'selector': event['selector'],
            'html': event['html'],
            "append": "append" in event and event["append"],
            "url": event["url"] if "url" in event else "",
            #"append": "append" in event and event["append"],
        }
        self.send_json(data)
      