import json


class EventController:
    def __init__(self):
        print("Instantiation du EventController...")
    
    def addEventData(self,event):
        self.client_data = json.loads(event)
        self.client_event = self.client_data["event"]
    
    def getClient_Data(self):
        return self.client_data
    def getClient_event(self):
        return self.client_event

    