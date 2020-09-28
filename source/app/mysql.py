# PyMySQL-0.10.1 flask-mysql-1.5.1
from flaskext.mysql import MySQL
from source.app import app

mysql = MySQL()
mysql.init_app(app)

cursor = mysql.get_db().cursor()
