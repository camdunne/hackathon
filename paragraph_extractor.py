import requests
from bs4 import BeautifulSoup
import json
import pickle
from collections import defaultdict

THRESH = 20

env_vars = json.load(open('env_vars.json'))
api_key = env_vars['api_key']


# def make_request(url, json_data=None, method="post", headers=None):
#     if (headers is None):
        

#     try:
#         func = getattr(requests, method)
#         if (json_data):
#             response = func(url, json=json_data, headers=headers)
#         else:
#             response = func(url, headers=headers)

#         if (response.content):
#             return json.loads(response.content)
#     except Exception as e:
#         app.ext_logger.exception(e)
#         return None


def dd():
    return defaultdict(dict)



if __name__ == "__main__":
	
	urls = ["https://www.nytimes.com/2018/04/07/health/antidepressants-withdrawal-prozac-cymbalta.html?hp&action=click&pgtype=Homepage&clickSource=story-heading&module=first-column-region&region=top-news&WT.nav=top-news"] # "https://www.nytimes.com/2017/08/22/health/417-million-awarded-in-suit-tying-johnsons-baby-powder-to-cancer.html"

	url_2_cats = defaultdict(dd)

	for url_str in urls:
		# get paragraphs
		page = requests.get(url_str) # http://dataquestio.github.io/web-scraping-pages/simple.html
		soup = BeautifulSoup(page.content, 'html.parser')
		all_paras = soup.find_all('p')
		all_text = []
		for para in all_paras:
			all_text.append(para.get_text())

		# Create a string of text from the paragraphs
		l = len(all_text)
		
		s = 0
		m = int(l/2)
		e = l
		if l > 9600:
			texts_list = [ ' '.join(all_text[s:m]), ' '.join(all_text[m:e]) ]
		else:
			texts_list = [ ' '.join(all_text[s:e])]
		url_2_cats[url_str] = None

		for i in range(len(texts_list)):
			all_text = texts_list[i]
			print(len(all_text), type(all_text))

			# prepare to send post req to API
			data = [
					  ('text', all_text),
					  ('api_key', api_key),
					]
			headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
			res = requests.post('https://apis.paralleldots.com/v3/taxonomy', headers=headers, data=data)
			# print("res", res) # reponse [200]
			# print("res type:", type(res)) # <class 'requests.models.Response'>
			# print('response from server:', res.text) # {"Error": "An Error Occured."}
			dictFromServer = res.json()
			# print("dictFromServer", dictFromServer)
			# print("dictFromServer type:", type(dictFromServer))
			if "taxonomy" in dictFromServer:
				for d in dictFromServer['taxonomy']:
					if url_2_cats[url_str] is None:
						url_2_cats[url_str] = {}
					if d['tag'] in url_2_cats[url_str].keys():
						pass # TODO take avg, not pass
					else:
						url_2_cats[url_str][d['tag']] = d['confidence_score']
			else:
				print("Faced some error with url = ", url_str) 
				break
					
		# exit(0)
		# print(all_text)
	# save the processed dict
	with open('urls_category_cache.pkl', 'wb') as f:
		pickle.dump(url_2_cats, f)
	
	# with open('urls_category_cache.pkl', 'rb') as f:
	# 	dicctt = pickle.load(f)



