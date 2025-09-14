import requests

class Database:
    def __init__(self, project, key):
        self.url=f"https://firestore.googleapis.com/v1/projects/{project}/databases/(default)/documents/whispers?key={key}     
    def store(self, uid):  
        data={"uid":uid, "memory_instance":
        requests.post(self.url,headers={"Content-Type":"application/json"},json=data)