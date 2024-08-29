import os

class Config:
    SECRET_KEY = '292b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
    SOCK_SERVER_OPTIONS = {'ping_interval': 1}
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER =  {'HTTP_X_FORWARDED_PROTO': 'https'}
    
    path_cur = os.path.dirname(os.path.abspath(__file__))
    path_parent = os.sep.join(path_cur.split(os.sep)[:-1])
    TEMPLATE_FOLDER = os.getenv('TEMPLATE_FOLDER', os.path.join(path_parent, 'front', 'demo'))
    STATIC_FOLDER = os.getenv('STATIC_FOLDER', os.path.join(path_parent, 'front', 'demo'))
    STATIC_URL_PATH = os.getenv('STATIC_URL_PATH', '/demo/')
    
class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    
class ProductionConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    
cfg = [ProductionConfig, DevelopmentConfig]