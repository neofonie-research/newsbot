# -*- coding: utf-8 -*-
from rasa_core_sdk import Action
from elasticsearch import Elasticsearch

def get_elastic_matches(query_text, index="news_articles"):
   es = Elasticsearch(['localhost'])
   res = es.search(index=index, body={"query": {"match": {"tags": query_text}}})
   if not res or res['hits']['total']==0:
      return None

   return res['hits']['hits']

class ActionDefaultFallback(Action):
   def name(self):
      # type: () -> Text
      return "action_default_fallback"

   def run(self, dispatcher, tracker, domain):
      # type: (CollectingDispatcher, Tracker, Dict[Text, Any]) -> List[Dict[Text, Any]]

      ##### TXT-Werk request
      hits = None
      try:
         hits = get_elastic_matches(query_text=tracker.latest_message['text'], index="news_articles")
      except Exception as e:
         print('No Elasticsearch results. {}'.format(str(e)))

      ## Nothing found in elastic index
      if not hits:
         dispatcher.utter_message("Tut mir leid, dazu habe ich nichts gefunden.")
      else:
         dispatcher.utter_message("Ich habe folgende Artikel gefunden:")
         for hit in hits[:3]:
            dispatcher.utter_message("[{}]({})".format(hit['_source']['title'],hit['_source']['url']))
      return []
