from prettytable import PrettyTable as table
import database as db
import os

def orderList():
	allTable = table(['Cot Number','Name','Order','Total','Balance'])
	raw = db.getAll()
	for item in raw:
		allTable.add_row([item[0],item[1],db.parseOrder(item[2])[1],item[3],item[4]])
	print(allTable)

def newOrder():
	cid = input('Cot Number: ')
	name = input('Name: ')
	order = ""
	done = False
	while not done:
		orderIn = input("Order Id: ") + '!'
		if orderIn == 'n!':
			done = True
		else:
			order += orderIn
	total = db.parseOrder(order)[0]
	credits = input(f'Total amount: {total}\nEnter amount paid: ')
	db.createOrder(cid,name,order,credits)
	print('Done')

def showOrder():
	cid = input("Enter Cot Number: ")
	data = db.getOrder(cid)
	if data == []:
		print('No order found')
		return 500
	else:
		order = data[0]
		orderList = db.parseOrder(order[2])[1]
		print(f"\nName: {order[1]} \nOrder: \n\n{orderList}\nTotal: {order[3]}\nBalance: {order[4]}")
	return cid

def deleteOrder():
	cid = showOrder()
	if cid == 500:
		return
	choice = input('Do you want to delete this order? [y/n]: ')
	if choice == "y":
		db.deleteOrder(cid)
	else:
		return
def stats():
	data = db.moneyStats()
	total = 0
	bal = 0
	for item in data:
		total += item[0]
		bal += item[1]
	print(f'\nTotal to bill: {total}\nBalance to give: {bal}')

def settle():
	cid = showOrder()
	choice = input("Do you want to settle this order? [y/n]: ")
	if choice == 'y':
		db.settle(cid)
		print('Done\n')
	else:
		return

def balanceList():
	data = db.balanceList()
	balTable = table(["Cot Number",'Name','Balance'])
	for item in data:
		balTable.add_row([item[0],item[1],item[2]])
	print(balTable)

while True:
	try:
		opt = input('\nJhonny"s Kitchen >>> ')
		if opt == "help":
			print('''
			new : Create a new order
			rem : Delete a order
			ls  : List all orders
			get : Get a specific order
			sta : View money stats
			bal : View balance list
			set : Settle a order
			clear : Clears the terminal
			''')
		elif opt == "new":
			newOrder()
		elif opt == 'rem':
			deleteOrder()
		elif opt == 'ls':
			orderList()
		elif opt == 'get':
			showOrder()
		elif opt == 'sta':
			stats()
		elif opt == "bal":
			balanceList()
		elif opt == "set":
			settle()
		elif opt == 'clear':
			os.system('clear')
		else:
			print("Unknown command try again or use help")
	except Exception as e:
		print('An error occuered:\n' + str(e))