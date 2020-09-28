import MySQLdb


def check(user):
	try:
		db = MySQLdb.connect(user='loginuser', passwd = "705ae97d0fcd9781ba54aff2390b401aa6d6fc2ff79e430a468169ac854598ba", db = "Users")
		c = db.cursor()
		c.execute("""SELECT username, password FROM users WHERE username = '%s';""" % user)
		r = c.fetchone()

		if r is None:
			return False

		return True
	except:
		return False
