class BaseAdapter(object):
	url = ''
	api_key = ''
	username = ''
	password = ''
	connection = None

	def connect(self, rl, username, password):
		pass

	def sync(self, models_list=[]):
		pass