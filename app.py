from flask import Flask
from flask import render_template
from kazoo.client import KazooClient
from flask import request
app = Flask(__name__)


def create(zkclient, dsname, username, passwd, url, driver):
	zkusername = '/dbcp/' + dsname + '/username'
	zkpasswd = '/dbcp/' + dsname + '/passwd'
	zkurl = '/dbcp/' + dsname + '/url'
	zkdriver = '/dbcp/' + dsname + '/driver'
	print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~' + username 
	try:
		zkclient.create(zkusername, value=str(username), makepath=True)
		zkclient.create(zkpasswd, value=str(passwd), makepath=True)
		zkclient.create(zkurl, value=str(url), makepath=True)
		zkclient.create(zkdriver, value=str(driver), makepath=True)
		return True
	except Exception, e:
		print 'exception:', e
		raise
		return False

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
	print username
	isdone = False
	isconn, zk = initZKClient()
	if isconn:
		
		isdone = create(zk, dsname, username, passwd, url, driver)
		dslist = get_children(zk)
		if isdone:
			return render_template('index.htm',dslist=dslist)
		else:
			return('zk create failed...')
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