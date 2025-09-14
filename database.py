import requests

class Database:
    def __init__(self, project):
        self.url=f"https://firestore.googleapis.com/v1/projects/{project}/databases/(default)/documents/whispers?key=AIzaSyD5jRoFS0zvIr4pLE7I-nw00J-uRcwWkUw"      
    def store(self, uid):  
        data={"uid":uid, "memory_instance":
        requests.post(self.url,headers={"Content-Type":"application/json"},json=data)