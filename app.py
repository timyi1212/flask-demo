from flask import Flask
from flask import render_template
from kazoo.client import KazooClient
from flask import request
from flask import redirect
from flask import url_for
app = Flask(__name__)

def zk_delete(zkclient,dsname):
	zkdsrootpath = '/dbcp/' + dsname
	try:
		zkclient.delete(zkdsrootpath, recursive=True)
		return True
	except Exception, e:
		print 'exception:', e
		raise
		return False


def zk_set(zkclient, dsname, username, passwd, url, driver):
	zkusername = '/dbcp/' + dsname + '/username'
	zkpasswd = '/dbcp/' + dsname + '/passwd'
	zkurl = '/dbcp/' + dsname + '/url'
	zkdriver = '/dbcp/' + dsname + '/driver'
	try:
		zkclient.set(zkusername, str(username))
		zkclient.set(zkpasswd, str(passwd))
		zkclient.set(zkurl, str(url))
		zkclient.set(zkdriver, str(driver))
		return True
	except Exception, e:
		print 'exception:', e
		raise
		return False



def create(zkclient, dsname, username, passwd, url, driver):
	zkusername = '/dbcp/' + dsname + '/username'
	zkpasswd = '/dbcp/' + dsname + '/passwd'
	zkurl = '/dbcp/' + dsname + '/url'
	zkdriver = '/dbcp/' + dsname + '/driver'
	
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

def zk_get(zkclient, dsname, property):
	zkpath = '/dbcp/' + dsname + '/' + property
	try:
		return zkclient.get(zkpath)[0]
	except BaseException, e:
		print 'exception:', e
		return None





	






@app.route("/dbcp/dsname")
def dbcpdsname():
	return render_template("addds.htm")

@app.route("/dbcp/dsname/<dsname>")
def editds(dsname):
	isconn, zk = initZKClient()
	if isconn:
		username = zk_get(zk, dsname, 'username')
		passwd = zk_get(zk, dsname, 'passwd')
		url = zk_get(zk, dsname, 'url')
		driver = zk_get(zk, dsname, 'driver')
		return render_template('editds.htm', dsname=dsname, username=username, passwd=passwd, url=url, driver=driver)
	else:
		return("zk connect failed...")
	

@app.route("/dbcp/dsname/delete/<dsname>")
def delds(dsname):
	isconn, zk = initZKClient()
	isdone = zk_delete(zk, dsname)
	if isdone:
		return redirect(url_for('index'))
	else:
		return('zk delete failed...')




@app.route("/", methods=['POST', 'GET'])
def index():
	isconn, zk = initZKClient()
	if isconn:
		
		if request.method == 'GET':
			dslist = get_children(zk)
			return render_template('index.htm',dslist=dslist)
		elif request.method == 'POST':
			if request.form['_method'] == 'post':
				username = request.form['username']
				passwd = request.form['passwd']
				url = request.form['url']
				driver = request.form['driver']
				dsname = request.form['dsname']
				isdone = create(zk, dsname, username, passwd, url, driver)
				if isdone:
					dslist = get_children(zk)
					return redirect(url_for('index'))
				else:
					return('zk create failed...')
			elif request.form['_method'] == 'put':
				username = request.form['username']
				passwd = request.form['passwd']
				url = request.form['url']
				driver = request.form['driver']
				dsname = request.form['dsname']
				isdone = zk_set(zk, dsname, username, passwd, url, driver)
				if isdone:
					return redirect(url_for('index'))
				else:
					return('zk edit failed...')



	else:
		return('zk connect failed...')







#@app.route('/dbcp/app1-1/<username>')
#def index(username):
#	return 'user %s' % username
if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)