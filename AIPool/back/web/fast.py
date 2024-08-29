from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import json
import os
import uuid

def create_app(generate, cfg):
      
    app = FastAPI(docs_url="/doc")
    
    app.mount(cfg.STATIC_URL_PATH, StaticFiles(directory=cfg.STATIC_FOLDER, html=False),  name="static")  
    
    @app.get('/')
    async def home():
        return FileResponse(cfg.STATIC_FOLDER + os.sep + "index.html")
    
    @app.get('/flow/{name}/')
    async def flow_imgs(name: str):
        return StreamingResponse(content=generate(name), 
                        media_type="multipart/x-mixed-replace; boundary=frame")
                        
    @app.post('/save/{name}')
    async def save_data(name: str, request: Request):
        data = await request.json()
        if type(data) == list:
            for d in data:
                if type(d['_id']) == bool:
                    d['_id'] = str(uuid.uuid4())
        with open('data' + os.sep + name + '.json', 'w') as f:
            json.dump(data, f)
    
    @app.get('/load/{name}')
    async def load_data(name: str):
        data = []
        try:
            with open('data' + os.sep + name + '.json', 'r') as f:
                data = json.load(f)
        except: pass
        return data
        
        
    return app