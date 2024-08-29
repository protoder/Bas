from flask import Response, Flask, render_template

def create_app(generate, cfg):

   
    app = Flask(__name__,
                template_folder=cfg.TEMPLATE_FOLDER,
                static_folder=cfg.STATIC_FOLDER,
                static_url_path=cfg.STATIC_URL_PATH)

    app.config.from_object(cfg)
    
    @app.route("/")
    def home():
        return render_template("index.html", test="none")
        
    @app.route("/flow/<string:name>/")
    def flow_imgs(name):
        return Response(generate(name),
            mimetype = "multipart/x-mixed-replace; boundary=frame")
                
    return app
