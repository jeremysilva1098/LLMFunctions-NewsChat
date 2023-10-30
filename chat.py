import openai
from dotenv import load_dotenv
import os
from functions import functions
import helper_funcs as hfuncs
import json
import requests
from datetime import datetime, date
from typing import Optional

load_dotenv()


class ChatSession:
    def __init__(self, system_message) -> None:
        self.key = os.getenv("OPENAI_API_KEY")
        # set the key
        openai.api_key = self.key
        self.news_key = os.getenv("NEWS_API_KEY")
        self.model_name = "gpt-3.5-turbo-16k"
        self.max_context = 16000
        # initialize the message history with the system message
        self.messages = [{'role': 'system', 'content': system_message}]
        # store citations
        self.citations = {}
        # news
        self.news_url_everything = "https://newsapi.org/v2/everything"
        self.news_url_headlines = "https://newsapi.org/v2/top-headlines"
        self.news_key = os.getenv("NEWS_API_KEY")
        # get the date to use for the news funcs
        self.week_ago = date.today().replace(day=date.today().day-7).strftime("%Y-%m-%d")

    
    def trim_messages(self) -> None:
        # check if we are near the max context
        while len(str(self.messages)) > self.max_context * 0.8:
            # remove the second oldest message
            self.messages.pop(1)


    def news_keyword_func(self, keyword: str, limit: int = 15) -> str:
        params = {
            'q': keyword,
            'apiKey': self.news_key,
            'sortBy': 'relevancy',
            'from': self.week_ago,
            'pageSize': limit
        }
        res = requests.get(self.news_url_everything, params=params)
        res = res.json()
        # grab the url content from each
        articles = hfuncs.add_url_content_to_news_res(res['articles'])
        articlesText = ""
        citations = {}
        # add articles untill 4000 tokens is reached
        for article in articles:
            if len(articlesText.split()) > (self.max_context * .33):
                break
            articlesText += article['content']
            citations[article['title']] = {'url': article['url'], 'source': article['source']['name']}
        return articlesText, citations
    

    def news_topic_func(self, topic: str, limit: int = 15) -> str:
        params = {
            'apiKey': self.news_key,
            'country': 'us',
            'category': topic,
            'sortBy': 'relevancy',
            'from': self.week_ago,
            'pageSize': limit
        }
        res = requests.get(self.news_url_headlines, params=params)
        res = res.json()
        # grab the url content from each
        articles = hfuncs.add_url_content_to_news_res(res['articles'])
        articlesText = ""
        citations = {}
        # add articles untill 4000 tokens is reached
        for article in articles:
            if len(articlesText.split()) > (self.max_context * .33):
                break
            articlesText += article['content']
            citations[article['title']] = {'url': article['url'], 'source': article['source']['name']}
        return articlesText, citations
        

    def execute_function(self, function_call) -> str:
        funcName = function_call['name']
        args = json.loads(function_call['arguments'])
        if funcName == 'get_news_by_keyword':
            keyword = args['keywords']
            print("Calling get_news_by_keyword with keyword: ", keyword)
            # call the function
            resText, citations = self.news_keyword_func(keyword)
        elif funcName == 'get_top_headlines_by_topic':
            topic = args['topic']
            print("Calling get_top_headlines_by_topic with topic: ", topic)
            resText, citations = self.news_topic_func(topic)
        return resText, citations
        
    
    def answer_query(self, query: str, functions: Optional[list] = functions) -> str:
        # check if this is not the first query
        if len(self.messages) > 1:
            # trim the messages as needed
            self.trim_messages()

        # add the query to the message history
        self.messages.append({'role': 'user', 'content': query})
        completionArgs = {
            "model": self.model_name,
            "messages": self.messages
        }
        if functions is not None:
            completionArgs['functions'] = functions
        chat_completion = openai.ChatCompletion.create(**completionArgs)
        #print(json.dumps(chat_completion, indent=4))
        # get the response
        ansDict = chat_completion.choices[0].message
        # add the response to the message history
        self.messages.append(ansDict)
        if 'function_call' in ansDict:
            # if the response is a function call, execute the function
            funcResText, funcCitations = self.execute_function(ansDict.function_call)
            # add the function results to the user query
            queryEnhanced = query + "\n---\n Here is some information that may be useful in answering the question: \n" + funcResText
            # call the chatbot again with the enhanced query and no functions
            ans =  self.answer_query(queryEnhanced, functions=None)
            # add the citations to the citations dict
            self.citations[ans] = funcCitations
            return ans
        # return the response
        return ansDict['content']
    

    def __repr__(self) -> str:
        return "Chat Session Instantiated!"

