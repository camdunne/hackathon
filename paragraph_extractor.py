import requests
from bs4 import BeautifulSoup
import json
import pickle
from collections import defaultdict


env_vars = json.load(open('env_vars.json'))
api_key = env_vars['api_key']

def dd():
    return defaultdict(dict)

def create_and_save_pickle(urls):
	url_2_cats = defaultdict(dd)

	for i,url_str in enumerate(urls):
		if(i%10==0):
			print("--------",i,"--------")
		# get paragraphs
		try:
			page = requests.get(url_str)
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
			x = ' '.join(all_text[s:e])
			if len(x) > 9600:
				texts_list = [ ' '.join(all_text[s:m]), ' '.join(all_text[m:e]) ]
			else:
				texts_list = [ x ]
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
				try:
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
				except:
					print(" :( ")
					break
		except:
			print(':| Beautiful soup issue')
					
		# exit(0)
		# print(all_text)
	# save the processed dict
	print("Saving...")
	with open('cam_urls_category_cache.pkl', 'wb') as f:
		pickle.dump(url_2_cats, f)
	print("Saving done...")

if __name__ == "__main__":
	TRAIN = False

	# urls = ["https://www.nytimes.com/2018/04/07/health/antidepressants-withdrawal-prozac-cymbalta.html?hp&action=click&pgtype=Homepage&clickSource=story-heading&module=first-column-region&region=top-news&WT.nav=top-news", "https://www.nytimes.com/2017/08/22/health/417-million-awarded-in-suit-tying-johnsons-baby-powder-to-cancer.html", "http://dataquestio.github.io/web-scraping-pages/simple.html"] # 
	# urls = ["https://www.savoirflair.com/beauty/341969/chanel-spring-summer-2018-makeup-look",
	# 		"https://www.nytimes.com/2018/01/12/business/personal-finance-dont-have-a-clue.html",
	# 		"https://www.nytimes.com/2018/04/06/us/politics/farenthold-harassment-case-resigns.html",
	# 		"https://www.nytimes.com/2018/04/07/us/politics/trump-trade-china-politics-heartland.html"]
	urls = ["https://developer.chrome.com/extensions/history#method-getVisits", "http://localhost:8000/", "https://stackoverflow.com/questions/28518454/visualizing-a-chart-using-c3", "https://www.google.com/search?q=c3+is+not+defined&…e.0.0j69i57j0l4.1875j0j1&sourceid=chrome&ie=UTF-8", "http://c3js.org/samples/chart_pie.html", "http://c3js.org/examples.html", "https://cdnjs.com/libraries/c3", "https://glitch.com/edit/#!/windy-tractor?path=views/index.html:38:1", "http://windy-tractor.glitch.me/", "https://glitch.com/edit/#!/windy-tractor?path=views/index.html:70:9", "https://glitch.com/edit/#!/windy-tractor?path=views/index.html:31:75", "https://cdnjs.com/libraries/d3/4.12.0", "https://cdnjs.com/libraries/d3", "https://github.com/c3js/c3/blob/master/bower.json", "https://github.com/c3js/c3", "http://c3js.org/gettingstarted.html", "https://www.google.com/search?q=d3+and+c3+versions…s=chrome..69i57.4867j0j4&sourceid=chrome&ie=UTF-8", "https://github.com/c3js/c3/releases/tag/v0.5.2", "http://c3js.org/gettingstarted.html#setup", "https://glitch.com/edit/#!/windy-tractor?path=views/index.html:45:9", "https://glitch.com/edit/#!/windy-tractor?path=public/client.js:1:0", "https://glitch.com/edit/#!/windy-tractor?path=views/index.html:26:28", "https://glitch.com/edit/#!/windy-tractor?path=views/index.html:40:76", "https://cdnjs.com/libraries/d3/3.5.12", "https://www.google.com/search?q=d3+cdn&oq=d3&aqs=c…0j69i59j69i60l3.2516j0j4&sourceid=chrome&ie=UTF-8", "https://glitch.com/edit/#!/windy-tractor?path=views/index.html:13:94", "https://glitch.com/edit/#!/windy-tractor?path=views/index.html:40:75", "https://www.google.com/search?q=c3+cdn&oq=c3+cdn&a…69i59j69i60j0l3.2433j0j4&sourceid=chrome&ie=UTF-8", "https://glitch.com/edit/#!/windy-tractor?path=views/index.html:16:0", "https://glitch.com/edit/#!/windy-tractor", "https://glitch.com/edit/#!/", "https://glitch.com/edit/#!/exclusive-hydrogen?path=app/app.jsx:1:0", "http://exclusive-hydrogen.glitch.me/", "https://www.google.com/search?ei=SVXJWuPOHI_1zgL21…33i160k1j0i67k1j0i131k1j0i131i67k1.77.-CEiXcML90c", "https://glitch.com/edit/#!/exclusive-hydrogen", "https://glitch.com/edit/#!/remix/starter-react", "https://glitch.com/~starter-react", "https://glitch.com/react", "https://glitch.com/search?q=react", "https://glitch.com/", "https://glitch.com/~c3-ex", "https://glitch.com/edit/#!/c3-ex", "https://glitch.com/search?q=c3", "https://glitch.com/search?q=chart", "https://glitch.com/search?q=d3", "https://glitch.com/~react-example", "https://glitch.com/edit/#!/react-example", "https://glitch.com/edit/#!/starter-react", "https://glitch.com/search?q=c3.js", "https://www.google.com/search?q=make+a+chrome+exte…s=chrome..69i57.9125j0j9&sourceid=chrome&ie=UTF-8", "https://www.google.com/search?ei=KE3JWvbzE8qTzwKiq…0....0...1c.1.64.psy-ab..2.1.213....0.RfaNmLaibsY", "https://www.scirra.com/forum/c3-clipboard-chrome-extension_t190677", "https://stackoverflow.com/questions/15348868/google-chart-in-chrome-extension-popup", "https://github.com/d3/d3/issues/1698", "https://www.google.com/search?q=chrome+extension+c…hrome..69i57j0.10610j0j1&sourceid=chrome&ie=UTF-8", "https://raw.githubusercontent.com/c3js/c3/v0.5.2/c3.min.js", "https://github.com/c3js/c3/blob/v0.5.2/c3.min.js", "https://github.com/c3js/c3/tree/v0.5.2", "https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.17/d3.min.js", "https://cdnjs.com/libraries/d3/3.5.17", "https://www.google.com/search?q=cdn+d3+v3&oq=cdn+d…s=chrome..69i57.3155j0j1&sourceid=chrome&ie=UTF-8", "https://stackoverflow.com/questions/41178111/d3js-d3-scale-category10-not-working", "https://www.google.com/search?ei=nkzJWpSeNMb0zgLsz…i131k1j0i46i67k1j46i67k1j0i20i263k1.0.tdprpw4Ktv8", "https://www.google.com/search?q=chrome+extension+c…s=chrome..69i57.4478j0j1&sourceid=chrome&ie=UTF-8", "https://codepen.io/vladaboiko/pen/EWgmrL", "https://www.w3schools.com/jsref/prop_text_value.asp", "https://github.com/rempkay/SpoiledHack", "http://flawlesshacks.com/", "https://www.google.com/search?ei=yAjJWurfG4jz5gLlu…1.64.psy-ab..0.3.251...0j0i20i263k1.0.D99Nbc5MECQ", "https://newsapi.org/s/buzzfeed-api", "https://glitch.com/edit/#!/discreet-beach", "https://chrome.google.com/webstore/detail/stylish-…themes-for/fjnbnpbmkenffdnngjfgmeleoegfcffe?hl=en", "https://glitch.com/edit/#!/discreet-beach?path=bubbles.js:5:9", "http://discreet-beach.glitch.me/", "http://glamgirlcodes.com/", "https://aframe.io/docs/0.8.0/introduction/javascript-events-dom-apis.html", "https://cdnjs.cloudflare.com/ajax/libs/d3/4.13.0/d3.min.js", "https://www.google.com/search?q=d3+cdn&oq=d3+cdn&a…rome..69i57j0l5.1446j0j4&sourceid=chrome&ie=UTF-8", "https://www.google.com/search?q=c3+cdn+link&oq=c3+…ome.1.69i57j0l5.6684j1j4&sourceid=chrome&ie=UTF-8", "http://c3js.org/samples/data_url.html", "https://www.oldies.com/artist-songs/Beyonce.html", "https://www.google.com/search?q=beyonce+song+title…rome..69i57j0l5.4861j0j1&sourceid=chrome&ie=UTF-8", "http://c3js.org/", "https://www.google.com/search?ei=0UnJWrP9OsTs5gL3w…k1j0i30k1j0i13k1j0i13i30k1j0i8i30k1.0.pVHBzDYQiOw", "https://www.google.com/search?q=c3&oq=c3&aqs=chrome..69i57j0l5.14420j0j1&sourceid=chrome&ie=UTF-8", "https://www.google.com/search?q=form+validation+va…ome.0.0j69i57j0.5011j0j1&sourceid=chrome&ie=UTF-8", "https://gomakethings.com/vanilla-javascript-form-validation/", "https://www.google.com/search?q=input+value+js&oq=…rome..69i57j0l5.2757j0j1&sourceid=chrome&ie=UTF-8", "https://github.com/vanilla-calendar/vanilla-calendar/blob/master/gulpfile.js", "https://github.com/vanilla-calendar/vanilla-calendar", "https://github.com/vanilla-calendar/vanilla-calendar/tree/master/dist", "https://github.com/vanilla-calendar/vanilla-calendar/blob/master/dist/vanillaCalendar.js", "https://raw.githubusercontent.com/vanilla-calendar/vanilla-calendar/master/dist/vanillaCalendar.js", "https://www.cssscript.com/minimal-inline-calendar-date-picker-vanilla-javascript/", "https://www.google.com/search?q=vanilla%20js%20dat…Ck6naAhXOwVkKHXTtA0YQsKwBCDAoADAA&biw=720&bih=803", "https://www.npmjs.com/package/vanilla-datepicker", "https://github.com/dbushell/Pikaday", "https://developer.chrome.com/extensions/history", "https://www.npmjs.com/package/js-datepicker", "https://unpkg.com/js-datepicker@2.3.1/datepicker.min.js"]
	if TRAIN:
		print("Training on",len(urls),"urls...")
		# create_and_save_pickle(urls)
	else:
		main_dict_count = defaultdict(int)
		print("Printing Stats...")
		with open('cam_urls_category_cache.pkl', 'rb') as f:
			url_2_cats_loaded = pickle.load(f)
    		
		print("Showing data for",len(url_2_cats_loaded),"urls.")
		for k,v in url_2_cats_loaded.items():
			print("Url:",k)
			print("Tags:",v,"\n")
			if v is not None:
				for tag_str,score in v.items():
					main_cat = tag_str.split('/')[0]
					# sub_cat = tag_str.split('/')[1]
					
					main_dict_count[main_cat] += 1
					# main_dict_count[sub_cat] += 1
		den_for_percent = 0
		for k,v in main_dict_count.items():
			den_for_percent += v
		print(den_for_percent)
		for k,v in main_dict_count.items():
			main_dict_count[k] /= den_for_percent
		print(main_dict_count)
		print("Saving stats...")
		with open('cam_stats_cache.pkl', 'wb') as f:
			pickle.dump(main_dict_count, f)
		print("Saving stats done...")
	
	# with open('urls_category_cache.pkl', 'rb') as f:
	# 	dicctt = pickle.load(f)



