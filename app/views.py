from flask import render_template
from app import app
import markdown
from flask import Markup
from lib.git import GitHandler
import json
import time
import hashlib

global profile_link

with open("config.conf", "r") as j:
    n = json.loads(j.read())
    profile_link = hashlib.md5(n["mail"]).hexdigest()
profile_link = "http://www.gravatar.com/avatar/%s?s=250" % profile_link
global s
global t
s = GitHandler(n["Github"], n["Repo"], n["client_id"], n["client_secret"])
s.fetch_posts()
s.fetch_sites()
t = time.time()


def refresh():
    global t
    a = time.time() - t
    if a > 300:
        s.fetch_posts()
        s.fetch_sites()
        t = time.time()


@app.route('/')
@app.route('/index')
@app.route('/blog')
def index():
    print profile_link
    refresh()
    content = s.return_posts()
    sites = s.return_sites()
    return render_template("index.html", picture = profile_link, posts=content, sites=sites.itervalues())


@app.route('/blog/<name>')
def blog_view(name):
    refresh()
    content = s.return_posts()
    sites = s.return_sites()
    for i in range(0, len(content)):
        if name == content[i]["rel_name"]:
            content_view = content[i]["content"]
            con_title = content[i]["title"]
            break
    content_view = Markup(markdown.markdown(content_view, ['fenced_code', 'codehilite']))
    return render_template("blog.html", picture = profile_link, head=con_title, content=content_view, sites=sites.itervalues())


@app.route('/site/<name>')
def site_view(name):
    refresh()
    content = s.return_sites()
    for i in range(1, len(content.keys())+1):
        if name == content[i]["name"]:
            content_view = content[i]["content"]
            sit_title = content[i]["name"]
            break
    content_view = Markup(markdown.markdown(content_view))
    return render_template("blog.html", picture = profile_link, head=sit_title, content=content_view, sites=content.itervalues())
