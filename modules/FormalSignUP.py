#######################################################################################
##################################### Formal Signup ###################################
############################# Shezad Khan & Yew Choon Tay #############################
#######################################################################################
#######################################################################################
'''
Module Containing the class FormalSignUp. See Below for more information.
'''
import urllib
import urllib2
import cookielib
import re
import formalnumberfinder
import datetime
import time


class FormalSignUp():
    '''
    This Class handles all communication with the castle JCR Website.
    It can be created with none or all attributes for a varitey of tasks.
    Spoofs User Agent to look like Mozilla Firefox.
    '''
    def __init__(self,username=None, password=None, formal_num=None, veg=False, guest_places='0'):
        '''
        Run on creation of the object, it creates the cookie jar, and adds it along with headers to the
        url opener class.
        '''
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        self.opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11')]
        self.username = username
        self.password= password
        self.formal_number = formal_num
        self.veg = veg
        self.guest_places = guest_places
        
    def Login(self):
        '''
        It logs into the JCR website, by posting directly to the authentication link.
        It returns True if there was a successful login, False if there was not and
        None if somthing went wrong (shouldn't happen)
        '''
        self.login_data = urllib.urlencode({'username' :self.username, 'password' :self.password})
        reply = self.opener.open('http://castlejcr.com/sessions/authenticate', self.login_data)
        headers_dic = dict(re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n", str(reply.info())))
        check = headers_dic['Refresh']
        if check == r'0;url=http://castlejcr.com/home':
            return True
        elif check == r'0;url=http://castlejcr.com/login_help':
            return False
        else:
            return None

    def GetServerTimeDifference(self):
        '''
        This methods polls the castle jcr website for server time using time.php. Returns the
        time difference between the server and local computer time.
        '''
        
        s_time = self.opener.open('http://castlejcr.com/')
        local_time = datetime.datetime.now()

        headers_dic = dict(re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n", str(s_time.info())))
        time_format = '%a, %d %b %Y %H:%M:%S GMT'
        date_time = headers_dic['Date']
        server_time = datetime.datetime.fromtimestamp(time.mktime(time.strptime(date_time, time_format)))

        print server_time

        dif_time = server_time - local_time

        return dif_time

    def GetFormalNumber(self):
        '''
        Calls formal find number module in order to get the formal number
        of the first formal on the jcr page. This method calls a function
        which parses HTML and is slow. You should try to only call it once.
        '''
        formal_page = self.opener.open('http://castlejcr.com/formals')
        return formalnumberfinder.FormalNumber(formal_page.read())

    def CheckLoggedIn(self):
        '''
        This function is Deprecated and probably/definitly should not be used....
        You Have Been Warned.
        '''
        check_login = self.opener.open('http://castlejcr.com/index.php/formals/view/227')
        check = re.search('<li class="pos">Attending &amp; Paid<br /></li>',check_login.read())
        if check:
            return True
        else:
            return False

    def SignUpFormal(self):
        '''
        This Methods signs up the user to formal by posting to the commit booking page.
        retunrs true if the signup was successful, or false if it wasn't.
        '''
        self.formal_data = urllib.urlencode({'veg' : self.veg, 'guest_num' :self.guest_places })
        #ret = self.opener.open("http://castlejcr.com/formals/commit_booking/%d" %int(self.formal_number)) # real line...
        ret = self.opener.open("http://castlejcr.com/formals/commit_booking/227") # Line for testing ....
        check = re.search('<li class="pos">Attending &amp; Paid<br /></li>',ret.read())
        if check:
            return True
        else:
            return False

    def LogOut(self):
        '''
        Logs out of the current session.
        '''
        self.opener.open('http://castlejcr.com/sessions/logout')

