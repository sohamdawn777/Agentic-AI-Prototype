import requests

class Database:
    def __init__(self, project, key, memory1, memory2):
        self.url=f"https://firestore.googleapis.com/v1/projects/{project}/databases/(default)/documents" 
        self.key=key  
        self.memory1=memory1
        self.memory2=memory2
    def store(self, uid): 
        urL=f"{self.url}/memoryDB/{uid}?key={self.key}"
        msgs1=[]
        msgs2=[]
        for j in self.memory1.chat_memory.messages:
            msgs1.append({"mapValue":{"fields":{"role":{"stringValue":j.type}, "message":{"stringValue":j.content}, "origin":{"stringValue":"creative"}}}})
        for k in self.memory2.chat_memory.messages:
            msgs2.append({"mapValue":{"fields":{"role":{"stringValue":k.type}, "message":{"stringValue":k.content}, "origin":{"stringValue":"fallback"}}}})    
        data={"fields":{"uid":{"stringValue":uid}, "memory_instance":{"arrayValue":{"values":msgs1+msgs2}}}}
        requests.patch(urL,headers={"Content-Type":"application/json"},json=data)