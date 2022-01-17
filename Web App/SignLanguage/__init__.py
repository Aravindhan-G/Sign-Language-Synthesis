from flask import Flask
import MySQLdb
    
conn = MySQLdb.connect(host="localhost",
                        user = "root",
                        passwd = "8128",
                        db = "sld")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS LOGIN(Name varchar(30),Mail varchar(40),Pass varchar(20),Pass1 varchar(20))''')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'thisisasecret'

    from .views import views
    from .detect import detect
    app.register_blueprint(views,url_prefix="/")
    app.register_blueprint(detect,url_prefix='/')

    return app

