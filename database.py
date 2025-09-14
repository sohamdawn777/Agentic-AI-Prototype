import requests


url=f"https://firestore.googleapis.com/v1/projects/{project}/databases/(default)/documents/whispers?key=AIzaSyD5jRoFS0zvIr4pLE7I-nw00J-uRcwWkUw"       
      requests.post(url,headers={"Content-Type":"application/json"},json=data)

