import os, json, requests, re
from elasticsearch import Elasticsearch

NEWS_API_KEY = "YOUR_NEWS_KEY"
TXT_WERK_KEY = "YOUR_TXTWERK_KEY"
es_index = 'news_articles'
regex_chars = re.compile(r'\[\+[0-9]* chars\]')

def txt_werk_request(text, services = 'categories,entities,tags'):
   headers = {'X-API-Key': TXT_WERK_KEY}
   url = "https://api.neofonie.de/rest/txt/analyzer"
   data = {'text':text.encode('utf-8') , 'services': services}
   res = requests.post(url, data=data, headers=headers)
   return res.json()

def index_news(sources):
   headlines = requests.get("https://newsapi.org/v2/top-headlines?sources={}&apiKey={}&pageSize=100".format(sources,NEWS_API_KEY)).json()

   es = Elasticsearch(['localhost'])

   for article in headlines['articles']:
      text = '. '.join([article[field] for field in ['title','description','content'] if article[field]])
      text = regex_chars.sub("", text)
      metadata = txt_werk_request(text)
      doc = {
         'title': article['title'],
         'description': article['description'],
         'content': article['content'],
         'url': article['url'],
         'tags': list(set([x['surface'] for x in metadata['entities']] + [x['label'] for x in metadata['entities']] + [x['term'] for x in metadata['tags']])),
         'category': metadata['categories'][0]['label'].capitalize()
         }
      print(doc['title'])
      print(doc['url'])
      print(doc['tags'])
      res = es.index(index=es_index, doc_type='_doc', body=doc)

if __name__ == "__main__":
   sources = "spiegel-online,bild,focus,die-zeit,wired-de,der-tagesspiegel,t3n,handelsblatt"
   index_news(sources)