import requests

ACCESS_TOKEN = '1/85f844fa5d9552ac3b3e66b1c03238a0'
YANDEX_KEY = 'trnsl.1.1.20141224T152311Z.dce9988e1ba0ccfb.c199c447a63cbe20a9cf2b0a5082c66c4fda15bf'


def get_profiles():
	url = 'https://api.bufferapp.com/1/profiles.json?access_token=%s' % ACCESS_TOKEN
	r = requests.get(url)

	results = r.json()

	for result in results:
		print result['id'], result['service']

def translate(text, lang):
	url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=%s&lang=en-%s&text=%s' % (YANDEX_KEY, lang, text)
	r = requests.get(url)

	print r.json()['text']

def get_updates(choice):
	url = 'https://api.bufferapp.com/1/profiles/%s/updates/pending.json?access_token=%s' % (choice, ACCESS_TOKEN)
	r = requests.get(url)

	results = r.json()
	lang = raw_input('Enter language to translate to: ')

	for result in results['updates']:
		print result['profile_service'], result['_id'], result['text']
		text = result['text']
		translate(text, lang)

get_profiles()

choice = raw_input('Enter desired profile: ')

get_updates(choice)