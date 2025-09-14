import requests

class Database:
    def __init__(self, project, key, memory):
        self.url=f"https://firestore.googleapis.com/v1/projects/{project}/databases/(default)/documents" 
        self.key=key    
    def store(self, uid): 
        urL=f"{self.url}/memoryDB/{uid}?key={self.key}"
        msgs=[]
        for j in self.memory.chat_memory.messages:
            msgs.append({"mapValue":{"fields":{"role":{"stringValue":j.type}, "message":{"stringValue":j.content}}}})
        data={"fields":{"uid":{"stringValue":uid}, "memory_instance":{"arrayValue":{"values":msgs}}}}
        requests.patch(urL,headers={"Content-Type":"application/json"},json=data)
                