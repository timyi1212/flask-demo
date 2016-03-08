from flask import Flask
from flask import render_template
from kazoo.client import KazooClient
from flask import request
app = Flask(__name__)


def initZKClient():
	isconn = True
	zk = KazooClient(hosts="127.0.0.1:2181")
	try:
		zk.start(3)
	except BaseException,e:
		isconn = False
		print 'exception:', e
	finally:
		return isconn, zk


def get_children(zkclient, zkpath='/dbcp'):
	dslist = []
	try:
		for i in zkclient.get_children(zkpath):
			dslist.append(i)


			
	except BaseException, e:
		print 'exception:', e
	finally:
		return dslist

def get(zkclient, appname, property):
	zkpath = '/dbcp/' + appname + '/' + property
	try:
		return zkclient.get(zkpath)[0]
	except BaseException, e:
		print 'exception:', e
		return None



@app.route("/dbcp/dsname/add", methods=['POST', ])
def add():
	username = request.form['username']
	passwd = request.form['passwd']
	url = request.form['url']
	driver = request.form['driver']
	dsname = request.form['dsname']
	print username, passwd, url, driver, dsname
	isconn, zk = initZKClient()
	if isconn:
		dslist = get_children(zk)
		
		return render_template('index.htm',dslist=dslist)
	else:
		return("zk connect failed...")



@app.route("/dbcp/dsname")
def dbcpdsname():
	return render_template("addds.htm")



@app.route("/")
def index():
	isconn, zk = initZKClient()
	if isconn:
		dslist = get_children(zk)
		
		return render_template('index.htm',dslist=dslist)
	else:
		return("zk connect failed...")



#@app.route('/dbcp/app1-1/<username>')
#def index(username):
#	return 'user %s' % username
if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)