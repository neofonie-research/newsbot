# TXTWerk Newsbot

Example of a chatbot that can answer questions it never heard before, by searching for matching keywords in a knowledge base. Keywords are found with [Neofonie](https://www.neofonie.de/)'s text analysis framework [TXTWerk](https://www.txtwerk.de/).

## Preparation
* **download or clone repository**
   ```
   git clone https://github.com/neofonie-research/newsbot.git
   ```
* **TXTWerk-API-Key**
   To get an API-key for TXTWerk register [here](https://services.neofonie.de/ws/account/register).
* **NewsAPI-Key**
   Newsarticles for the Chatbot are gathered from [newsapi.org](newsapi.org). Register for an API-key [here](newsapi.org/account).
* **RASA Installation**
   The newsbot uses [RASA](https://rasa.com/) as a Chatbot-Framework because it is both highly adjustable and achieves good results with a standard configuration. Installation should be simple and is described [here](https://rasa.com/docs/rasa/user-guide/installation/).
* **Elasticsearch-Installation**
  Elasticsearch is used as the search index for the newsbot. Its installation is described [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html)