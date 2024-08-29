
import os
from process_image import ProcessShot, detect

def handler(frame) -> tuple():
    return ProcessShot(detect, frame) 


if 'thread' == os.getenv('STREAM_MODE'):
    from stream import StreamThread as Stream
elif 'mono' == os.getenv('STREAM_MODE'):
    from stream import StreamMono as Stream
else:    
    from stream import Stream

stream = Stream(handler)
stream.run()

if '__main__' == __name__:
       
    debug = True if os.getenv('APP_DEBUG') or False else False
    host  = os.getenv('APP_HOST') or '0.0.0.0'
    port  = int(os.getenv('APP_PORT', '5000'))
    
    from config import cfg
    config = cfg[debug]
    
    if '1' == os.getenv('ASYNC_WEB'):
        import uvicorn  
        from web.fast import create_app
        app = create_app(stream.generate, config)
        uvicorn.run(app, host=host, port=port)
    else:
        from web.flask import create_app
        app = create_app(stream.generate, config)
        app.run(host=host, port=port,
            debug=debug, use_reloader=debug, use_debugger=debug)                     