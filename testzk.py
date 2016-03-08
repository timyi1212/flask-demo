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




isconn, zk = initZKClient()
if isconn:
	print get_children(zk)
	print get(zk, 'app1-1', 'username')
	print get(zk, 'app1-1', 'passwd')
	print get(zk, 'app1-1', 'driver')
	print get(zk, 'app1-1', 'url')
else:
	print 'b'