"https://api.github.com/repos/foxboron/foxblog/git/trees/master"
import urllib2
import json
import base64


class GitHandler(object):
    def __init__(self, username, repo, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.url = self.api_retv("https://api.github.com/repos/%s/%s/git/trees/master" % (username, repo))

    def api_retv(self, url):
        v = urllib2.urlopen(url + "?client_id=%s&client_secret=%s" % (self.client_id, self.client_secret)).read()
        js = json.loads(v)
        return js

    def fix_name(self, title):
        date = title[:10].replace("-", ".")
        link = "/blog/%s" % title[11:-3]
        ntitle = title[11:-3].replace("_", " ").title()
        return (title[11:-3], date, ntitle, link)

    def fetch_posts(self):
        j = self.url
        posts = j["tree"]
        for i in range(0, len(posts)):
            if posts[i]["path"] == "posts":
                self.posts_dir = posts[i]["url"]
                break
        posts_dir = self.api_retv(self.posts_dir)
        self.posts_content = []
        for i in range(0, len(posts_dir["tree"])):
            if posts_dir["tree"][i]["path"] != ".gitignore":
                post = {}
                post["rel_name"], post["date"], post["title"], post["link"] = self.fix_name(posts_dir["tree"][i]["path"])
                con = self.api_retv(posts_dir["tree"][i]["url"])
                post["content"] = base64.b64decode(con["content"])
                self.posts_content.append(post)

    def return_posts(self):
        return self.posts_content[::-1]

    def fetch_sites(self):
        j = self.url
        posts = j["tree"]
        for i in range(0, len(posts)):
            if posts[i]["path"] == "sites":
                self.sites_dir = posts[i]["url"]
                break
        sites_dir = self.api_retv(self.sites_dir)
        self.sites_content = {}
        for i in range(0, len(sites_dir["tree"])):
            if sites_dir["tree"][i]["path"] != ".gitignore":
                site = {}
                row, name, link = self.sites_title(sites_dir["tree"][i]["path"])
                site["name"] = name
                site["link"] = link
                con = self.api_retv(sites_dir["tree"][i]["url"])
                site["content"] = base64.b64decode(con["content"])
                self.sites_content[row] = site
        
    def return_sites(self):
        return self.sites_content
    
    def sites_title(self, title):
        title = title[:-3].split("-")
        link = "/site/" + title[1]
        return (int(title[0]), title[1], link)