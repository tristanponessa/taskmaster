#!/usr/bin/env python
# encoding: UTF-8

import sys
import yaml
import atexit
import os
import readline
import rlcompleter
import cmd
import time
import threading
from threading import Thread
import subprocess
import commands
import copy
import signal

def cmp_success(ret, success):
	for i in success:
		if i == ret:
			return True
	return False

umask = os.umask(0)
os.umask(umask)
opened = open(sys.argv[1])
global var1
var1 = yaml.load(opened)
opened.close()
sys.argv[1] = os.getcwd() + "/" + sys.argv[1]

def signal_handler(signal, frame):
		global var1
		to_open = sys.argv[1]
		if os.path.isfile(to_open):
			opened = open(to_open)
			del var1
			var1 = yaml.load(opened)
			opened.close()
			print "\n" + to_open + ": Successfully load"
			sys.stdout.write("\033[36m$> \033[37m")
			sys.stdout.flush()
		else:
			print "\n\033[31mError:\033[37m " + to_open + " is not a file that can be open"
signal.signal(signal.SIGHUP, signal_handler)

if 'directory' in var1:
	if os.path.exists(var1['directory']):
		os.chdir(var1['directory'])
	else:
		os.mkdir(var1['directory'])
		os.chdir(var1['directory'])

from cmd import Cmd
import subprocess

if 'logfile' in var1:
	if os.path.isfile(var1['logfile']):
		lobj = open(var1['logfile'], 'r+a+w+')
		file = lobj.read()
	else:
		lobj = open(var1['logfile'], 'w+')
else:
	print "\033[31mError:\033[37m logfile missing in configuration file"
	exit()

if not 'prog' in var1:
	print "\033[31mError:\033[37m prog missing in configuration file"
	exit()

lobj.write("[" + time.strftime("%c") + "] Started\n")

class MyThread(Thread):
	process = None
	name = 'None'
	test = None
	launch = None
	pid = None
	time = None

	def __init__(self, test):
		Thread.__init__(self)
		if test != None:
			self.test = test.copy()

	def run(self):
		if 'stdout' in self.test:
			foutput = open(self.test['stdout'], 'w')
		else:
			foutput = 1
		if 'stderr' in self.test:
			ferrput = open(self.test['stderr'], 'w')
		else:
			ferrput = 2
		if 'stdin' in self.test:
			finput = open(self.test['stdin'], 'r')
		else:
			finput = -1
		self.name = self.test['name']
		prompt.current_log = prompt.current_log + "[" + time.strftime("%c") + "] \033[33mStarted:\033[37m " + self.name + "\n"
		lobj.write("[" + time.strftime("%c") + "] Started : " + self.name + "\n")
		self.launch = time.strftime("%c")
		my_env = os.environ.copy()
		if 'env' in self.test:
			for var in self.test['env']:
				my_env[var] = self.test['env'][var]
		if 'umask' in self.test:
			os.umask(self.test['umask'])
		self.process = subprocess.Popen(self.test['command'], stdout=foutput, stderr=ferrput, stdin=finput, shell=True, env=my_env)
		self.pid = self.process.pid
		self.time = time.time()
		self.process.communicate()
		lobj.write("[" + time.strftime("%c") + "] " + self.name + " stopped \n")
		if not cmp_success(self.process.returncode, self.test['success']):
			lobj.write("[" + time.strftime("%c") + "] " + "Error: " + self.name + " returncode: " + str(self.process.returncode) + "\n")
			prompt.current_log = prompt.current_log + "[" +  time.strftime("%c") + "] \033[31mError:\033[37m " + self.name + " returncode: " + str(self.process.returncode) + "\n"
			print "\033[31mError:\033[37m " + self.name + " didn't exit correctly returncode=" + str(self.process.returncode)
			if self.test['failed'] > 0:
				self.test['failed'] = self.test['failed'] - 1
				self.run()
				self.name = 'None'
				return
		prompt.current_log = prompt.current_log + "[" +  time.strftime("%c") + "] \033[33mStopped:\033[37m " + self.name + "\n"
		self.name = 'None'

class MyPrompt(Cmd):
	current_log = "Log: \n"
	threads = {0 : {"None" : MyThread(None)}}


	def do_load(self, args):
		global var1
		if args:
			to_open = args
		else:
			to_open = sys.argv[1]
		if os.path.isfile(to_open):
			opened = open(to_open)
			del var1
			var1 = yaml.load(opened)
			opened.close()
			print to_open + ": Successfully load"
		else:
			print "\033[31mError:\033[37m " + to_open + " is not a file that can be open"

	def emptyline(self):
		print ""

	def default(self, args):
		self.do_help(args)

	def do_help(self, args):
		print "\nDefault commands: \n\033[33mstart stop restart status load quit help\nmail add coucou pause continue\033[37m\n"

	def do_add(self, args):
		if not args:
			print "\033[31mError:\033[37m use: add program key value"
			return
		args = args.split(' ')
		if len(args) != 3:
			print "\033[31mError:\033[37m use: add program key value"
			return
		prog = args[0]
		key = args[1]
		val = args[2]
		flag = 0
		for value in var1['prog']:
			if value['name'] == prog:
				flag = 1
				if key != 'env' and key != 'success':
					if val.isdigit() == True:
						value[key] = int(val)
					else:
						value[key] = val
				elif key == 'success':
					if val.isdigit() == True:
						value[key].append(int(val))
				else:
					print "Sorry, you can't modify the env while running the main programm"
					return
		if not flag:
			print prog + ": Invalid program name"

	def do_coucou(self, args):
		print "Tu veux voir ma bite ?"
		var = raw_input("Yes, No, Maybe : ")
		if var == "I don't know":
			var = raw_input('Can you repeat the question ? ')
			if var == "YOU'RE NOT THE BOSS OF ME NOW":
				subprocess.call("open http://manganim.free.fr/Malcolm/Fichiers/Malcolm%20-%20Opening.MP3", shell=True)
			else:
				print "YOU failed ..."
		else:
			print "Noob"
			subprocess.call("open https://www.youtube.com/watch?v=M6KOEMJKdEI", shell=True)

	def do_pause(self, name):
		flag = 0
		for key in self.threads:
			if name in self.threads[key]:
				if self.threads[key][name] != None and self.threads[key][name].name != 'None':
					self.threads[key][name].process.send_signal(17)
					flag = 1
		if flag == 0:
			print name + ": \033[31mNo such process\033[37m"

	def do_continue(self, name):
		flag = 0
		for key in self.threads:
			if name in self.threads[key]:
				if self.threads[key][name] != None and self.threads[key][name].name != 'None':
					self.threads[key][name].process.send_signal(19)
					flag = 1
		if flag == 0:
			print name + ": \033[31mNo such process\033[37m"


	def do_EOF(self, args):
		print ""
		for key in self.threads:
			for to_kill in self.threads[key]:
				if self.threads[key][to_kill] != None and self.threads[key][to_kill].name != 'None':
					self.threads[key][to_kill].process.send_signal(self.threads[key][to_kill].test['stop_signal'])
					if 'kill_wait' in self.threads[key][to_kill].test:
						time.sleep(self.threads[key][to_kill].test['kill_wait'])
					else:
						time.sleep(1)
					if self.threads[key][to_kill].process.returncode == None:
						self.threads[key][to_kill].process.send_signal(9)
						self.threads[key][to_kill].process.wait()
		lobj.write("[" + time.strftime("%c") +"] quit\n")
		exit()

	def do_status(self, args):
		flag = 0
		if not args:
			for prog in var1['prog']:
				flag = 0
				for key in self.threads:
					if prog['name'] in self.threads[key] and self.threads[key][prog['name']] != None and self.threads[key][prog['name']].name != 'None':
						print "\033[32m" + prog['name'] + " is running with pid : " + str(self.threads[key][prog['name']].pid) + \
							" since : " + "{:.3f}".format(time.time() - self.threads[key][prog['name']].time) + " seconds\033[37m"
						flag = 1
				if flag == 0:
					print "\033[33m" + prog['name'] + " is not running\033[37m"
		else:
			for key in self.threads:
				if args in self.threads[key]:
					if  self.threads[key][args] != None and self.threads[key][args].name != 'None':
						print "\033[32m" + args + " is running with pid : " + str(self.threads[key][args].pid) + \
							" since : " + "{:.3f}".format(time.time() - self.threads[key][args].time) + " seconds\n" + \
							"\tIt was launch on : " + self.threads[key][args].launch + "\033[37m"
						flag = 1
			if flag == 0:
				print "\033[33m" + args + " is not running\033[37m"


	def do_stop(self, name):
		flag = 0
		for key in self.threads:
			if name in self.threads[key]:
				if self.threads[key][name] != None and self.threads[key][name].name != 'None':
					self.threads[key][name].process.send_signal(self.threads[key][name].test['stop_signal'])
					if 'kill_wait' in self.threads[key][name].test:
						time.sleep(self.threads[key][name].test['kill_wait'])
					else:
						time.sleep(1)
					if self.threads[key][name].process.returncode == None:
						self.threads[key][name].process.send_signal(9)
						self.threads[key][name].process.wait()
					flag = 1
				del self.threads[key][name]
		if flag == 0:
			print name + ": \033[31mNo such process\033[37m"

	def do_quit(self, args):
		for key in self.threads:
			for to_kill in self.threads[key]:
				if self.threads[key][to_kill] != None and self.threads[key][to_kill].name != 'None':
					self.threads[key][to_kill].process.send_signal(self.threads[key][to_kill].test['stop_signal'])
					if 'kill_wait' in self.threads[key][to_kill].test:
						time.sleep(self.threads[key][to_kill].test['kill_wait'])
					else:
						time.sleep(1)
					if self.threads[key][to_kill].process.returncode == None:
						self.threads[key][to_kill].process.send_signal(9)
						self.threads[key][to_kill].process.wait()
		lobj.write("[" + time.strftime("%c") +"] quit\n")
		exit()

	def do_mail(self, args):
		if args:
			subprocess.call("cat " + var1['logfile'] +  " | mail -s Log " + args, shell=True)
		elif 'MAIL' in os.environ:
			subprocess.call("cat " + var1['logfile'] +  " | mail -s Log " + os.environ['MAIL'], shell=True)
		else:
			print "\033[31mError:\033[37m No mail given run with \"mail email@email\""

	def do_restart(self, name):
		if name in self.threads[0] and self.threads[0][name].name != 'None':
				prompt.do_stop(name)
				prompt.do_start(name)
		else:
			print "\033[33m%s is not already launch\033[37m" % name
			return
		self.current_log = self.current_log + "[" + time.strftime("%c") + "] \033[33mRestarted: \033[37m" + name + "\n"
		lobj.write("[" + time.strftime("%c") + "] Restarted : " + name + "\n")

	def do_start(self, args):
		if not args :
			print "\033[33mA program name is needed in argument\033[37m"
			return;
		test = None
		for tmp in var1['prog']:
			if tmp['name'] == args:
				test = tmp
		if test == None:
			print args + ": \033[33mUnknow program\033[37m"
			return
		for key in self.threads:
			if args in self.threads[key] and self.threads[key][args].name != 'None':
				print "\033[33mWarning:\033[37m %s is already launch" % test['name']
				return
		if 'numproc' in test:
			nbprocess = test['numproc']
		else:
			nbprocess = 1
		i = 0
		while i < nbprocess:
			p =  -1
			fail = test['failed']
			if not i in self.threads:
				self.threads[i] = {"None" : None}
			while fail > 0 and p == -1:
				self.threads[i][test['name']] = MyThread(test)
				self.threads[i][test['name']].start()
				os.umask(umask)
				time.sleep(test['wait'])
				if self.threads[i][test['name']].process != None:
					p = self.threads[i][test['name']].process.returncode
				else:
					p = -1
				fail = fail - 1
			i = i + 1

		if fail <= 0 and p != None and not cmp_success(p, test['success']):
			print "\033[31mError:\033[37m could not launch " + test['name'] + "\n"
			lobj.write("[" + time.strftime("%c") + "] Error: could not launch " + test['name'] + "\n")
			self.current_log = self.current_log + "[" + time.strftime("%c") + "] \033[31mError:\033[37m could not launch " + test['name'] + "\n"
		else:
			self.current_log = self.current_log + "[" + time.strftime("%c") + "] \033[32mSuccess:\033[37m launching " + test['name'] + "\n"
			lobj.write("[" + time.strftime("%c") + "] Success launching " + test['name'] + "\n")

	def do_log(self, args):
		print self.current_log

if __name__ == '__main__':
    prompt = MyPrompt()
    for test in var1['prog']:
    	if test['autostart'] == 1:
			prompt.do_start(test['name'])

    prompt.prompt = '\033[36m$> \033[37m'
    prompt.cmdloop('\033[35mStarting prompt\033[33m.\033[31m.\033[32m.\033[37m')
