import requests
#from urllib.parse import urlencode
#
#

class FakeService():

	def getFakeEmployee():
		url = 'http://dummy.restapiexample.com/api/v1/employees'
		try:
			response = requests.get(url)
			if response.status_code == 200:
				return response.json()
		except requests.ConnectionError:
			return None