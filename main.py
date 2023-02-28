from flet import *
import json

# LOGIN PAGE
class MyLogin(UserControl):
	def __init__(self):
		super(MyLogin, self).__init__()
		self.username = TextField(label="username")
		self.password = TextField(label="password")

	def build(self):
		return Container(
			bgcolor="yellow200",
			padding=10,
			content=Column([
				Text("Login Account",size=30),
				self.username,
				self.password,
				ElevatedButton("Login Now",
					bgcolor="blue",color="white",
					on_click=self.loginbtn
					),
				# AND CREATE REGISTER BUTTON FOR REDIRECT YOU
				# GO TO PAGE REGISTER IF YOU NOT REGISTER
				TextButton("i No Have Account",
					on_click=self.registerbtn
					),
				# AND NOW I CREATE BUTTON TO PRIVATE PAGE
				# WITHOUT LOGIN 
				ElevatedButton("Go to Private Page Without login",
					bgcolor="red",color="white",
					on_click=self.nologinbtn
					),

				])

			)

	def nologinbtn(self,e):
		self.page.go("/privatepage")
		self.page.update()


	def registerbtn(self,e):
		# GO TO REGISTER PAGE
		self.page.go("/register")
		self.page.update()



	def loginbtn(self,e):
		# WRITE YOU INPUT USERNAME AND PASSWORD TO Login.json
		# this is read sorry 
		# if username and password in file login.json
		# not valid 
		# then show error message


		with open("login.json","r") as f:
			data = json.load(f)
		username = self.username.value
		password = self.password.value

		# CHECK YOU LOGIN
		for user in data["users"]:
			if user["username"] == username and user["password"] == password :
				print("you success login !!!!")

				# AND IF YOU SUCESS LOGIN THEN CREATE SESSIONS
				# THIS SESSION IS KEY IF YOU GO TO PRIVATE PAGE
				# IF YOU DONT HAVE THIS SESSION YOU AUTOMATiCALY
				# REDIRECT TO LOGIN PAGE AGAIN

				datalogin = {
					# THIS CUSTOM FOR DATA
					# EXAMPLE I WANT SAVE VALUE AND USERNAME
					"value":True,
					"username":self.username.value
				}	

				# NOW CREATE SESSIONS
				self.page.session.set("loginme",datalogin)
				# AND REDIRECT TO PRIVATE PAGE IF YOU HAVE THIS 
				# sessions
				self.page.go("/privatepage")
				self.page.update()
			else:
				# AND IF YOU WRONG USERNAME PASSWORD THEN SHOW
				# SNACKBAR MESSAGE 
				print("you wrong login")
				self.page.snack_bar = SnackBar(
					Text("YOu Wrong login",size=30),
					bgcolor="red"
					)
				self.page.snack_bar.open = True
				self.page.update()



# NOW CREATE PRIVATE PAGE 
class PrivatePage(UserControl):
	def __init__(self):
		super(PrivatePage, self).__init__()

	def build(self):
		return Container(
			bgcolor="blue200",
			content=Column([
				Text("Welcome to YOu Page Again",size=30),
				# AND CREATE LOGOUT BUTTON 
				# THE LOGOUT BUTTON WILL REMOVE SESSION LOGIN
				ElevatedButton("logout now",
					bgcolor="red",color="white",
					on_click=self.logoutnow
					)

				])
			)
	def logoutnow(self,e):
		# CLEAR THE NAME OF SESSION loginme
		self.page.session.clear()
		# AND THEN YOU DONT AGAIN SESSION
		# YOU WILL REDIRECT TO LOGIN PAGE AGAIN
		self.page.go("/")
		self.page.update()


# AND FINALY CREATE REGISTER PAGE FOR REGISTER USERNAME
# AND PASSWORD
class MyRegister(UserControl):
	def __init__(self):
		super(MyRegister, self).__init__()
		self.username = TextField(label="username")		
		self.password = TextField(label="password")		

	# AND NOW CREATE PAGE 
	def build(self):
		return Container(
			bgcolor="green200",
			padding=10,
			content=Column([
				Text("Register You Account",size=30),
				self.username,
				self.password,
				ElevatedButton("Register Now",
					on_click=self.registerprocess
					)

				])

			)
	def registerprocess(self,e):
		new_user = {
			"username":self.username.value,
			"password":self.password.value,
		}
		data = {"users":[]}

		# AND WRITE YOU USERNAME AND PASSWORD TO login.json FIle
		data["users"].append(new_user)
		with open("login.json","w") as f:
			json_string = json.dumps(data)
			# AND WRITE
			f.write(json_string)

		# AND IF SUCCESS WRITE USER PASSWORD TO FILE login.json
		# THEN YOU REDIRECT TO LOGIN PAGE AUTOMATICALLY
		self.page.go("/")
		self.page.update()





def main(page:Page):

	# AND NOW CREATE ROUTE FOR EACH PAGE YOU CREATE BEFORE
	mylogin = MyLogin()
	privatepage = PrivatePage()
	registerpage = MyRegister()

	# AND NOW DEFINE ROUTE
	def myroute(route):
		# CLEAR ALL PAGES 
		page.views.clear()
		# AND APPEND ROUTE AND PAGE 
		page.views.append(
				View(
					"/",[
						# AND YOU PAGE HERE!!!!
						mylogin 
						]
					)
			)
		# AND CREATE SECOND PAGE
		# THIS IS PRIVATE PAGE
		if page.route == "/privatepage":
			print(page.session.get("loginme"))
			if page.session.get("loginme") == None:
				page.go("/")
			else:
				page.views.append(
				View(
					"/privatepage",
					[
					privatepage
					]

					)

				)
		# and last create REGISTER URL PAGE
		elif page.route == "/register":
			page.views.append(
				View(
					"/register",
					[
					registerpage
					]

					)

				)
		page.update()

	# AND NO USE PAGE.add() AGAIN
	# REMOVE page.add()

	# AND NOW DEFINE YOU ROUTE TO PAGE
	page.on_route_change = myroute
	page.go(page.route)

flet.app(target=main)
