class BaseAdapter(object):
	url = ''
	api_key = ''
	username = ''
	password = ''
	connection = None
	errors = []
	adapter_name = 'Base'
	max_batchsize = None

	### COMMON METHODS FOR ALL ADAPTERS ###

	def sync(self, options={}):
		models_to_sync = options.get(
			'models',
			['person', 'list']
		)

		if 'person' in models_to_sync:
			person_batchsize = options.get('people_batchsize', 100)
			self.sync_people(
				start_at=options.get('people_startat', 0),
				batch_size=person_batchsize
			)

		if 'list' in models_to_sync:
			list_batchsize = options.get('list_batchsize', 100)
			self.sync_lists(
				batch_size = list_batchsize
			)

	def sync_lists(self, batch_size=100):
		if self.max_batchsize and batch_size > self.max_batchsize:
			raise ImproperlyConfigured("{0} has a max batch size of {1}".format(self.adapter_name, self.max_batchsize))

		for list_data in self.get_lists():
			self.sync_list(list_data, batch_size=batch_size)

	def sync_list(self, list_data, start_at=0, batch_size=100):
		list_object = self.create_list(list_data)

		index = start_at

		while index < self.get_list_item_count(list_data):
			for list_item in self.get_list_items(list_data, index, batch_size):
				self.create_list_item(list_item, list_object)

			index += batch_size
			print "Imported {0} list records...".format(index)

	def sync_donations(self, start_at=0, batch_size=100):
		if self.max_batchsize and batch_size > self.max_batchsize:
			raise ImproperlyConfigured("{0} has a max batch size of {1}".format(self.adapter_name, self.max_batchsize))

		index = start_at

		while index < self.get_donations_count():
			for donation in self.get_donations(index, batch_size):
				self.create_donation(donation)

			index += batch_size
			print "Imported {0} donation records...".format(index)

	def sync_forms(self, start_at=0, batch_size=100):
		if self.max_batchsize and batch_size > self.max_batchsize:
			raise ImproperlyConfigured("{0} has a max batch size of {1}".format(self.adapter_name, self.max_batchsize))

		index = start_at

		while index < self.get_forms_count():
			for form in self.get_forms(index, batch_size):
				self.create_form(form)

			index += batch_size
			print "Imported {0} form records...".format(index)		

	def sync_people(self, start_at=0, batch_size=100):
		if self.max_batchsize and batch_size > self.max_batchsize:
			raise ImproperlyConfigured("{0} has a max batch size of {1}".format(self.adapter_name, self.max_batchsize))

		index = start_at

		while index < self.get_people_count():
			for person in self.get_people(index, batch_size):
				self.create_person(person)
			index += batch_size
			print "Imported {0} person records...".format(index)

	### METHODS FOR OVERRIDING ###

	def connect(self, rl, username, password):
		"""
		Override this method to set self.connection
		to an object representing your API interface.
		"""
		pass

	def get_people_count(self):
		"""
		Override this method to return a total count of the
		number of people in the database.
		"""
		pass

	def get_people(self, index, batch_size):
		"""
		Override this method to return a subset of the people in
		the remote database who fall within the range of index..batch_size.
		"""
		pass

	def create_person(self, person_data):
		"""
		Override this method to take a dictionary of person_data formatted
		according to your API and produce a Person object.
		"""
		pass

	def create_list_item(self, list_item_data, list_object):
		"""
		Override this method to take a dictionary of list_item_data formatted
		according to your API and produce a Person object.
		"""
		pass

	def create_list(self, list_data):
		"""
		Override this method to take in a dictionary of list_data
		and generate at List object from it, according to the API
		you are using.
		"""
		return None

	def get_donations_count(self):
		"""
		Override to return the number of donations in the system
		"""
		pass

	def get_donations(self, index, batch_size):
		"""
		Override to return a list of donations
		"""
		pass

	def create_donation(self, donation_data):
		"""
		Override to translate donation_data to a donation object.
		"""
		pass

	def get_forms_count(self):
		"""
		Override to return the number of donations in the system
		"""
		pass

	def get_forms(self, index, batch_size):
		"""
		Override to return a list of donations
		"""
		pass

	def create_form(self, donation_data):
		"""
		Override to translate donation_data to a donation object.
		"""
		pass