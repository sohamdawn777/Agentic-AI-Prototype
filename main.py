from fastapi import FastAPI, Request, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app= FastAPI()  #creates the app instance

app.mount("/static", StaticFiles(directory="static", name="static"))   #the /static is the url path prefix. the local static folder is mounted onto the browser side and the browser makes requests like /static/homepage.js and this maps the program to look into the local static folder (directory) for homepage.js. the name parameter is an optional parameter for internal reference to a particular static folder if multiple static folders are there...it does not affect the url.

templates= Jinja2Templates(directory: "templates")
@app.get("/


