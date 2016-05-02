#!/usr/bin/env python2

from flask import Flask, render_template, g, url_for, redirect, make_response

from pymongo import *
from bson.objectid import ObjectId
import urllib

app = Flask(__name__)
#app.config.from_object(__name__)


def connect_mongo():
    clt = MongoClient()
    return clt.scrapy


@app.before_request
def before_request():
    g.db = connect_mongo()

@app.teardown_request
def teardown_request(exception):
    pass



@app.route("/")
def hello():
    return redirect(url_for('articles'))


@app.route("/articles/")
def articles():
    cur = g.db.article.find({})
    articles = list(cur)
    return render_template('articles.html', objects=articles)


@app.route("/article/<gid>")
def article(gid):
    article = g.db.article.find_one(ObjectId(gid))
    article['pages'] = list(g.db.page.find(
        {
            'article_id':ObjectId(gid)
        }, 
        sort=[('idx',ASCENDING)]))
    article['pages_done'] = list(g.db.page.find({
        'article_id':ObjectId(gid),
        'image_path': { '$ne' : None }
    }, {'idx':1}))
    return render_template('article.html', object=article)

@app.route("/article/<gid>/delete", methods=["POST"])
def delete_article(gid):
    g.db.page.remove({'article_id': ObjectId(gid)})
    g.db.article.remove({ '_id': ObjectId(gid)})
    return redirect(url_for('articles'))

@app.route("/article/<gid>/scrape", methods=["POST"])
def scrape_article(gid):
    obj = g.db.article.find_one({ '_id': ObjectId(gid)})
    data = ""
    if obj:
        url = obj['url']
        form_data = { 
            'project': 'default', 
            'spider': 'ehinfo',
            'url': url
        }
        f = urllib.urlopen('http://localhost:6800/schedule.json', urlencode(form_data))
        data  = f.read()
    resp = make_response(data)
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route("/article/<gid>/scrape_image", methods=["POST"])
def scrape_article_image(gid):
    obj = g.db.article.find_one({ '_id': ObjectId(gid)})
    data = ""
    if obj:
        url = obj['url']
        form_data = { 
            'project': 'default', 
            'spider': 'ehinfo',
            'url': url
        }
        f = urllib.urlopen('http://localhost:6800/schedule.json', urlencode(form_data))
        data  = f.read()
    resp = make_response(data)
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route("/article/<gid>/check")
def check_article(gid):
    obj = g.db.article.find_one({ '_id': ObjectId(gid)})
    return render_template('article.html', object=obj)


@app.route("/image/<path:path>")
def image(path):
    data = None
    with open('/home/roadt/Pictures/scrapy/'+path, mode='rb') as f:
        data = f.read()
    resp = make_response(data)
#    resp.headers['Content-Type'] = 'image/jpg'
    return resp

    



    
if __name__ == '__main__':
        app.run(debug=True,host='0.0.0.0', port=5001)
