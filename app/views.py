from flask import render_template
from app import app
import markdown
from flask import Markup, request
from lib.git import GitHandler
import json
import time
import hashlib
from lib.database import databaselayer


global profile_link
global s
global t
global vc
global viewcount


def init():
    global profile_link
    global s
    global t
    global vc
    global viewcount
    with open("config.conf", "r") as j:
        n = json.loads(j.read())
        profile_link = hashlib.md5(n["mail"]).hexdigest()
    profile_link = "http://www.gravatar.com/avatar/%s?s=250" % profile_link
    s = GitHandler(n["Github"], n["Repo"], n["client_id"], n["client_secret"])
    s.fetch_posts()
    s.fetch_sites()
    t = time.time()
    viewcount = {}

init()

def refresh():
    global t
    global viewcount
    a = time.time() - t
    if a > 300:
        s.fetch_posts()
        s.fetch_sites()
        t = time.time()
        viewcount = {}


@app.route('/')
@app.route('/index')
@app.route('/blog')
def index():
    global viewcount
    if not viewcount.get('index'):
        viewcount['index'] = []
    if request.remote_addr not in viewcount.get('index'):
        viewcount['index'].append(request.remote_addr)
        databaselayer.inc("index")
    refresh()
    content = s.return_posts()
    sites = s.return_sites()
    return render_template("index.html", picture=profile_link, **locals())


@app.route('/blog/<name>')
def blog_view(name):
    refresh()
    content, sites = s.return_posts(), s.return_sites()
    for i in range(0, len(content)):
        if name == content[i]["rel_name"]:
            content_view = content[i]["content"]
            con_title = content[i]["title"]
            con_date = content[i]["date"]
            con_time = content[i]["time"]
            db_id = content[i]["key"]
            break
    content_view = Markup(markdown.markdown(content_view, ['fenced_code', 'codehilite']))
    global viewcount
    if not viewcount.get(db_id):
        viewcount[db_id] = []
    if request.remote_addr not in viewcount.get(db_id):
        viewcount[db_id].append(request.remote_addr)
        databaselayer.inc(db_id)
    return render_template("blog.html", picture=profile_link, **locals())




@app.route('/site/<name>')
def site_view(name):
    refresh()
    content, sites = s.return_posts(), s.return_sites()
    for i in range(1, len(sites.keys()) + 1):
        print sites[i]
        if name == sites[i]["con_tit"]:
            print "lool"
            print sites[i]["content"]
            content_view = sites[i]["content"]
            con_title = sites[i]["name"]
            break
    content_view = Markup(markdown.markdown(content_view))
    global viewcount
    if not viewcount.get(con_title):
        viewcount[con_title] = []
    if request.remote_addr not in viewcount.get(con_title):
        viewcount[con_title].append(request.remote_addr)
        databaselayer.inc(name)
    return render_template("blog.html", picture=profile_link, **locals())


@app.route("/views")
def view_counts():
    l = databaselayer.fetch()
    content, sites = s.return_posts(), s.return_sites()
    site_list, blog_list = {}, {}
    for i in sites.itervalues():
        for n in l: 
            if i["name"] == n[0]:
                site_list[i["name"]] = n[1]
            if n[0] == "index":
                site_list["index"] = n[1]
    for i in content:
        for n in l:
            if i["key"] == n[0]:
                blog_list[i["title"]] = n[1]
    return render_template("views.html", picture=profile_link, **locals())

