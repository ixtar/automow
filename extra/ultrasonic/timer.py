import time

class Timer():
	def __init__(self):
		self.start_time = None
		self.end_time = None
		self.last_difference = None
	
	def start(self):
		self.start_time = time.time()
	
	def get_difference(self):
		self.last_difference = time.time() - self.start_time
		return self.last_difference
	
	def sleep(time_to_sleep):
		time.sleep(time_to_sleep)

	def delay(self, time_uS):
		self.start()
		while True:
			if (self.get_difference()*1000000) >= time_uS:
				return self.last_difference

# def test_timer ():
# 	myTimer = Timer()
# 	myTimer.start()
# 	while True:
# 		if (myTimer.get_difference()*1000000) >= 10:
# 			print(str(myTimer.last_difference*1000000) + " uS")
# 			return myTimer.last_difference
	
# test_timer()
