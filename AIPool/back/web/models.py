from pydantic import BaseModel, BaseSettings, Field


class Pool(BaseModel):
    name: str = ''
    desc: str = ''

class Scheme(BaseModel):
    name: str = ''
    desc: str = ''
    pool: str = ''

class Camera(BaseModel):
    name: str = ''
    desc: str = ''
    rtsp: str = ''
    schm: str = ''