import threading
import FormalSignUP
import datetime

class SignUpToFormal():
	def __init__(self, db, formal_id):
		self.db = db #pointer to the database object.
		self.complete_signuplist = list()
		self.formal_id = formal_id
		self.GetFormalDate()
		self.SetInitialTimer()

		print 'Set Timer'

	def GetFormalDate(self):
		formal = self.db(self.db.formal.id==self.formal_id).select().first()
		self.formal_signup_time = formal.formal_signup

	def GetServerTime(self):
		signup = FormalSignUP.FormalSignUp()
		self.server_time_difference = signup.GetServerTimeDifference()
		del signup
		return self.server_time_difference + datetime.datetime.now()

	def GetTimeToFormal(self):
		time_to_formal = self.formal_signup_time - self.GetServerTime() # time to formal using the server time 
		time_in_seconds = (time_to_formal.days * 24 * 60 *60) + time_to_formal.seconds #put it in seconds
		time_in_seconds_ohb = time_in_seconds - (20*60) # time in seconds 20 mins before we need to signup
		return time_in_seconds_ohb, time_in_seconds

	def SetInitialTimer(self):
		ttf, tttb = self.GetTimeToFormal()# time for formal, time to twenty before [formal]
		self.timer = threading.Timer(tttb, self.PrepForFormalSignUp_TwentyMinsBefore)
		self.timer.start() # stat the timer ....
		print 'Started Initial Timer'

	def SetFinalTimer(self):
		ttf, tttb = self.GetTimeToFormal()# time for formal, time to twenty before [formal]
		self.timer = threading.Timer(ttf, self.SignUpEveryone)
		self.timer.start()
		print 'Started Final Timer'

	def PrepForFormalSignUp_TwentyMinsBefore(self):
		signup = FormalSignUP.FormalSignUp()
		self.formal_number = signup.GetFormalNumber() #gets first formal number on the page ...
		self.LoginSignUpList()
		self.SetFinalTimer()

	def LoginSignUpList(self):
		#self.GetFormalSignUpList_Now()
		self.complete_signuplist = []
		z= self.db(self.db.signup_list.formal_id==self.formal_id).select()
    		for person in z:
    			temp_u = self.db(self.db.user.id==person[user_id]).select().first()
    			self.complete_signuplist.append([temp_u.email,temp_u.password])
		
		self.logged_in_users_list = []
		
		for person in self.complete_signuplist:
			username = person[0]
			password = person[1]
			sign_obj =  FormalSignUP.FormalSignUp(username,password,self.formal_number)
			if sign_obj.Login() == True:
				self.logged_in_users_list.append(sign_obj)

	def SignUpEveryone(self):
		for obj in self.logged_in_users_list:
			chk = obj.SignUpFormal()
			if chk == True:
				print 'Successfully Signed People Up!'
				obj.LogOut()
			else:
				print 'Could Not Sign Up!'

	def CancelSignUp(self):
		self.timer.cancel()



