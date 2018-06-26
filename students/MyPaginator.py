
class EmptyPage(Exception):
	def __init__(self, message):
		super().__init__(message)


class MyPaginator():
	def __init__(self, objects, entries_per_page):
		self.objects = objects
		if entries_per_page == 0:
			self.entries_per_page = 3
		self.entries_per_page = entries_per_page

	class Page():
		def __init__(self, index, paginatorObj):
			self.index = index
			self.paginatorObj = paginatorObj

		def __str__(self):
			return 'Page {} of {}'.format(self.index, self.paginatorObj.num_pages)

		def __repr__(self):
			return 'Page {} of {}'.format(self.index, self.paginatorObj.num_pages)

		@property
		def object_list(self):
			entries_per_page = self.paginatorObj.entries_per_page
			start_index = (self.index-1)*entries_per_page
			end_index = min(self.index*entries_per_page, self.paginatorObj.count)

			return self.paginatorObj.objects[start_index:end_index]

		def has_next(self):
			return self.index + 1 <= self.paginatorObj.num_pages

		def has_previous(self):
			return self.index - 1 > 0

		def has_other_pages(self):
			return self.index == self.paginatorObj.num_pages

		def next_page_number(self):
			if self.index == self.paginatorObj.num_pages:
				raise EmptyPage('No next page available')
			else:
				return self.index + 1

		def previous_page_number(self):
			if self.index == 1:
				raise EmptyPage('No previous page available')
			else:
				return self.index - 1

		def start_index(self):
			entries_per_page = self.paginatorObj.entries_per_page
			return (self.index-1)*entries_per_page

		def end_index(self):
			entries_per_page = self.paginatorObj.entries_per_page

			return min(self.index*entries_per_page, self.paginatorObj.count) - 1

	@property
	def count(self):
		return len(self.objects)

	@property
	def num_pages(self):
		count = 0
		if len(self.objects) % self.entries_per_page == 0:
			count = len(self.objects) // self.entries_per_page
		else:
			count = len(self.objects) // self.entries_per_page + 1

		return count

	@property
	def page_range(self):
		return range(1, self.num_pages + 1)

	def page(self, index):
		if index == 0:
			raise EmptyPage('No page with 0 index')
		elif index > self.num_pages:
			raise EmptyPage('No pages with this index')

		return MyPaginator.Page(index, self)
	
	
	

