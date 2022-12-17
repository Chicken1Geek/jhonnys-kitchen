import sqlite3 as sql

dbconn = sql.connect('orders.db')
db = dbconn.cursor()

db.execute('CREATE TABLE IF NOT EXISTS orders(cid INT,name TEXT,orders TEXT,total INT,balance INT,stats INT);')

global menu
menu = {
"1":{'name':'Chicken Briyani','price':140},
'2':{'name':'Lollipop','price':65}
}

def parseOrder(orderList):
	global menu
	total = 0
	finalList = ""
	rawList = ''
	for item in orderList.rstrip('!').split('!'):
		total += menu[item]['price']
		finalList += menu[item]['name'] + '\n'
		rawList += str(item)+'!'
	return total , finalList , rawList.rstrip('!')

def createOrder(cid,name,orders,credit):
	data = parseOrder(orders)
	orderList = data[2]
	total = data[0]
	balance = int(credit) - total
	stats = 0
	db.execute('INSERT INTO orders values (?,?,?,?,?,?)',(cid,name,orderList,total,balance,stats))
	dbconn.commit()	

def getOrder(cid):
	data = db.execute(f'SELECT * FROM orders WHERE cid = {cid}').fetchall()
	return data

def deleteOrder(cid):
	db.execute(f'delete from orders where cid = {cid}')
	dbconn.commit()

def balanceList():
	raw = db.execute('select cid,name,balance from orders where stats = 0').fetchall()
	return raw

def settle(cid):
	db.execute(f'update orders set balance = 0,stats = 1 where cid = {cid}')
	dbconn.commit()

def getAll():
	return db.execute('select * from orders').fetchall()
	
def moneyStats():
	return db.execute('select total,balance from orders').fetchall()

#createOrder(1,'Sachin','1!2!1!2',500)	
