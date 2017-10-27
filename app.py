# -*- coding: utf-8 -*-
"""

"""

from flask import Flask, render_template, request
from elasticsearch import Elasticsearch

app = Flask(__name__)
HOST = 'http://localhost:9200/'
es = Elasticsearch(hosts=[HOST])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index/results', methods=['GET', 'POST'])
def search_simple():
    query = request.form["input"]
    res = es.search(index="reuters", size = 20,
                    body = {
                            "query": {
                                    "multi_match": {
                                            "query": query,
                                            "fields": [
                                                    "title",
                                                    "date",
                                                    "topics",
                                                    "places",
                                                    "people",
                                                    "exchanges",
                                                    "companies",
                                                    "orgs"
                                                    ]
                                            }
                                    }
                            }
                    )
    return render_template('results.html', res=res)

@app.route('/index/document/<int:id>', methods=['GET', 'POST'])
def show_doc(id):
    res = es.search(index="reuters", 
                    body = {
                          "query": {
                                  "match": {
                                          "id": id}
                                  }  
                                 }
                    )
    return render_template('document.html', res=res)

if __name__ == '__main__':
    app.secret_key ='mysecret'
    app.run()