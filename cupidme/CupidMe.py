from json import dumps, loads
from re import sub, DOTALL
from time import sleep

from robobrowser import RoboBrowser

from .CupidFilter import CupidFilter
from .CupidUtil import string_between, CupidException


class CupidMe:   
    #Initialization optionally allows log-in
    def __init__(self, username = None, password = None):
        self.total_users = 0
        self.user_list = []
        self._logged_in = False
        
        self.browser = RoboBrowser(parser = "html.parser", user_agent = "Python-Bot")
        self.filter = CupidFilter(self.browser)
        if username is not None and password is not None:
            self.login(username, password)

    #Perform a search and save the number of matching users. Optionally, save a list of users that match the search.
    def search(self, list_users = False):
        self.browser.open('https://www.okcupid.com/1/apitun/match/search', method='post', data=dumps(self.filter.current_filter))
        if self.browser.response.status_code != 200:
            raise CupidException('Search Error')

        #OKCupid may return malformed JSON depending on photo data
        #This removes the data before loading it
        data = loads(sub(', \"thumbs.*?\}\]','',str(self.browser.parsed), flags = DOTALL))
        self.total_users = 0
        self.user_list.clear()
        
        if self._logged_in and self.filter.match_cutoff > 0:
            for user in data["data"]:
                if user["percentages"]["match"] < self.filter.match_cutoff:
                    break
                self.total_users += 1
                if list_users:
                    self.user_list.append(user["username"])         
        else:
            self.total_users = data["total_matches"]
            if list_users:
                for user in data["data"]:
                    self.user_list.append(user["username"])

    def contact(self, username, message = None, reply = False, like = False):
        if not self._logged_in:
            raise CupidException('Authentication Error')
        self.browser.open('https://www.okcupid.com/profile/' + username)
        if self.browser.response.status_code != 200:        
            raise CupidException('Invalid profile')
        
        page_info = loads(string_between(str(self.browser.find_all('script')[-4]),"ProfilePromo.params = ",";\n"))
        userid = page_info['jsParams']['userid']
        contact = page_info["lastContact"]
        
        if like:
            self.browser.open('https://www.okcupid.com/1/apitun/profile/' + userid + '/like', method='post', data={})
        
        if message is not None:
            if reply is False and contact != 0:
                return
            
            elif contact == 0:
                existing_convo = False
            
            else:
                existing_convo = True
                
            payload = {"receiverid":userid,"body":message,"source":"desktop_global","service":"profile","reply":existing_convo}
            self.browser.open('https://www.okcupid.com/1/apitun/messages/send', method='post', data=dumps(payload))
                
    #messages all users in user_list with the string msg. Be responsible.
    def flood(self, message = None, like = False):
        for user in self.user_list:
            self.contact(user, message = message, like = like)
            sleep(2)
    
    def login(self, usr, pwd):
        if self._logged_in: self.logout()
        auth = {'username': usr, 'password': pwd, 'okc_api': 1}
        self.browser.open('https://www.okcupid.com/login', method = 'post', data = auth)
        if self.browser.response.status_code != 200 or loads(str(self.browser.parsed))['screenname'] == 'None':        
            raise CupidException('Authentication Error')
        else:          
            self.browser.session.headers["Authorization"] = "Bearer " + loads(str(self.browser.parsed))["oauth_accesstoken"]
            self._saved_filters()
            self._logged_in = True

    def logout(self):
        self.browser.open('https://www.okcupid.com/logout')
        self.browser.session.headers["Authorization"] = ''
        self._logged_in = False
            
    #set current filter equal to your last search (as saved by the site)
    def _saved_filters(self):
        self.browser.open('https://www.okcupid.com/match')
        self.filter.clear()
        self.filter.copy(loads(string_between(str(self.browser.find_all('script')[-4]), "params\" : [", "]}"))["filters"])