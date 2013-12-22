from pyquery import PyQuery as pq

class Tpb:
	def __init__(self):
		pass

	def first_by_keyword(self, keyword):
		d = pq(url='http://thepiratebay.se/search/'+keyword+'/0/7/0')
		return d('img[src="/static/img/icon-magnet.gif"]').parent().eq(0).attr('href')