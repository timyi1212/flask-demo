# -*- coding: utf-8 -*-
from kazoo.client import KazooClient

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

#获取节点名称
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

def create(zkclient, dsname, username, passwd, url, driver):
	zkusername = '/dbcp/' + dsname + '/username'
	zkpasswd = '/dbcp/' + dsname + '/passwd'
	zkurl = '/dbcp/' + dsname + '/url'
	zkdriver = '/dbcp/' + dsname + '/driver'
	try:
		zk.create(zkusername, value=username, makepath=True)
		zk.create(zkpasswd, value=passwd, makepath=True)
		zk.create(zkurl, value=url, makepath=True)
		zk.create(zkdriver, value=driver, makepath=True)
		return True
	except Exception, e:
		print 'exception:', e
		return False


isconn, zk = initZKClient()
zk.delete('/dbcp/app2-50000000005', recursive=True)