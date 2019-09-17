import os, json, requests, re
from elasticsearch import Elasticsearch

NEWS_API_KEY = "YOUR_NEWS_KEY"
TXT_WERK_KEY = "YOUR_TXTWERK_KEY"
es_index = 'news_articles'
## regex to remove remaining character counts ([+950 chars]) at the end of news article responses
regex_chars = re.compile(r'\[\+[0-9]* chars\]')

def txt_werk_request(text, services = 'categories,entities,tags'):
   headers = {'X-API-Key': TXT_WERK_KEY}
   url = "https://api.neofonie.de/rest/txt/analyzer"
   data = {'text':text.encode('utf-8') , 'services': services}
   resp = requests.post(url, data=data, headers=headers).json()
   if not 'entities' in resp and not 'tags' in resp:
      print(resp)
   return resp

def get_article_text(article):
   text = '. '.join([article[field] for field in ['title','description','content'] if article[field]])
   ## remove remaining character counts in responses
   return regex_chars.sub("", text)

def get_tags(metadata):
   return list(set(
      [x['surface'] for x in metadata['entities'] if x['surface'] is not None] \
      + [x['label'] for x in metadata['entities'] if x['label'] is not None] \
      + [x['term'] for x in metadata['tags'] if x['term'] is not None]
      ))

def index_news(sources):
   es = Elasticsearch(['localhost'])
   url = "https://newsapi.org/v2/top-headlines?sources={}&apiKey={}&pageSize=100"
   headlines = requests.get(url.format(sources,NEWS_API_KEY)).json()
   if not 'articles' in headlines:
      print(headlines)
   for article in headlines['articles']:
      text = get_article_text(article)
      metadata = txt_werk_request(text)
      doc = {
         'title': article['title'],
         'description': article['description'],
         'content': article['content'],
         'url': article['url'],
         'tags': get_tags(metadata),
         'category': metadata['categories'][0]['label'].capitalize()
         }
      print(doc['title'], doc['tags'], sep='\n')
      ## url as _id to avoid duplicates
      resp = es.index(es_index, doc_type='_doc', body=doc, id=doc['url'])

if __name__ == "__main__":
   sources = "spiegel-online,bild,focus,die-zeit,wired-de,der-tagesspiegel,t3n,handelsblatt"
   index_news(sources)