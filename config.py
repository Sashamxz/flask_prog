import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

    def __init__(self, app):
        self.app = app

    def productionConfig(self):    
        self.app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:123@localhost/test.db'
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.app.config["SECRET_KEY"] = "FDSAFASFDASFDASGBFRSHBDSSFASDF"
        self.app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size' : 100, 'pool_recycle' : 280}
        self.app.config["WTF_CSRF_ENABLED"] = False
        return self.app

    def developmentConfig(self):    
        self.app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:123@localhost/test.db'
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.app.config["SECRET_KEY"] = "FDSAFASFDASFDASGBFRSHBDSSFASDF"
        self.app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size' : 100, 'pool_recycle' : 280}
        self.app.config["WTF_CSRF_ENABLED"] = False
        return self.app

    def testConfig(self):
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, 'test.db')
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.app.config["WTF_CSRF_ENABLED"] = False
        return self.app