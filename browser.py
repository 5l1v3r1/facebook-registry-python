import mechanize
import cookielib
import socks
import socket
import os
import time
from random import randrange
from stem import Signal
from stem.control import Controller



def create_connection(address, timeout=None, source_address=None):
	sock = socks.socksocket()
	print(address)
	sock.connect(address)
	return sock
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150)
# patch the socket module
socket.socket = socks.socksocket
socket.create_connection = create_connection


User_Info = {
	"ho": ["Nguyen","Hoang","Phan","Pham", "Ho","Le","Truong","Dinh", "Bui", "Tran", "Do", "Vo", "Luong"],
	"dem": ["Thi","Hoang","Thuy","Tuyet","Thu","Kim","Thanh","Ngoc","Kieu","Anh","Phuong", "Tuong"],
	"ten": ["Duong","Linh","Thuy","Thu","Tuyet","Tien","Hue","Hanh","Uyen",
			"Duyen","Chau","Huyen","Huong","Trinh","Truc","Trang","Hong","Mai",
			"Luong", 'Huong', "Nhung", "Linh", "Ngan","Thanh","Nguyet","Quynh",
			"Thao","Bich","Lien","Tram","Anh","Kieu","Diem","Phuong","Dung","Nhu",
			"Anh","Hang","Bich"]
}

class Registor(object):
	"""docstring for Registor"""
	def __init__(self):
		# Browser
		self.br = mechanize.Browser()

		# Cookie Jar
		self.cj = cookielib.LWPCookieJar()
		self.br.set_cookiejar(self.cj)
		# Browser options
		self.br.set_handle_equiv(True)
		self.br.set_handle_gzip(True)
		self.br.set_handle_redirect(True)
		self.br.set_handle_referer(True)
		self.br.set_handle_robots(False)
		# Follows refresh 0 but not hangs on refresh > 0
		self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
		# Want debugging messages?
		#br.set_debug_http(True)
		#br.set_debug_redirects(True)
		#br.set_debug_responses(True)

		# User-Agent (this is cheating, ok?)
		self.br.addheaders = [
			('User-agent', 'Mozilla/5.0 (Linux; U; Android 2.2; en-us; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1')
			# ('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36')
			# ('User-Agent', 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.136 Mobile Safari/537.36')
		]
		# br.set_proxies({"socks5": "127.0.0.1:9050"})

	def gen_acc(self):
		self.user = {
			"ho": User_Info["ho"][randrange(0, len(User_Info["ho"]))],
			"dem": User_Info["dem"][randrange(0, len(User_Info["dem"]))],
			"ten": User_Info["ten"][randrange(0, len(User_Info["ten"]))],
		}
		self.birthday = {
			"day": str(randrange(1, 29+1)),
			"month": str(randrange(1, 12+1)),
			"year": str(randrange(1990, 1997+1)),
			"salt": str(randrange(1, 999999+1))
		}
		self.user['user'] = ("%s%s%s" % (self.user['ho'], self.user['dem'], self.user['ten'])).lower()
		self.user['email'] = ("%s%s%s%s%s@outlook.com" % (
						self.user['user'],
						self.birthday['month'], self.birthday['day'],self.birthday['year'][-2:], self.birthday['salt']
					)).lower()
		self.user['pass'] = '%s:">..' % self.user['user']
		print(self.user)
		print(self.birthday)

	def reg(self):
		self.gen_acc()
		# try:
		self.br.open('https://facebook.com')
		self.br.select_form(nr=1)
		self.br.form['lastname'] = "%s %s" % (self.user['ho'], self.user['dem'])
		self.br.form['firstname'] = self.user['ten']
		self.br.form['reg_email__'] = self.user['email']
		self.br.form['reg_email_confirmation__'] = self.user['email']
		self.br.form['birthday_day'] = [self.birthday['day']]
		self.br.form['birthday_month'] = [self.birthday['month']]
		self.br.form['birthday_year'] = [self.birthday['year']]
		self.br.form['reg_passwd__'] = self.user['pass']
		self.br.form['sex'] = ["1"]
		self.br.submit()
		response = self.br.response().read()
		print(response)
		if not 'action="/login/checkpoint/' in response:
			print("#"*70)
			print("face: " + self.user['email'])
			print("pass: " + self.user['pass'])
			print("#"*70)
			# for link in self.br.links(url_regex='/changeemail'):
			# 	print link
			# 	self.br.click_link(link)
			# 	response = self.br.response().read()
			# 	break
			return True
		# except Exception, e:
		# 	print(e)
		return False

if __name__ == '__main__':
	
	while True:
		reg = Registor()
		if reg.reg():
			r = raw_input("Next >>")
		# reg.gen_socks()
		os.system("python tor.py")
		time.sleep(2)
