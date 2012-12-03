from flask import render_template
from app import app
import markdown
from flask import Markup
from lib.git import GitHandler
import json

with open("config.conf", "r") as j:
    t = json.loads(j.read())
s = GitHandler(t["Github"], t["Repo"], t["client_id"], t["client_secret"])
s.fetch_posts()
print "lol"


@app.route('/')
@app.route('/index')
@app.route('/blog')
def index():
    content = s.return_posts()
    return render_template("index.html", posts=content)


@app.route('/blog/<name>')
def blog_view(name):
    content = s.return_posts()
    print content
    for i in range(0, len(content)):
        if name == content[i]["rel_name"]:
            content_view = content[i]["content"]
            break
    content_view = Markup(markdown.markdown(content_view))
    return render_template("blog.html", content=content_view)
