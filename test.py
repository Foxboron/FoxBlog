#!/usr/bin/env python

def fix_name(title):
    base = title[:-3].split("#")
    print base
    date = base[0].replace("-", "/")
    link = "/blog/%s" % base[2]
    ntitle = base[2].replace("_", " ").title()
    time = base[1].replace("-", ":")
    return (base[2], date, time, ntitle, link)


def main():
    var = "2012-12-02#07-12#Hello_World.md"
    print fix_name(var)

if __name__ == '__main__':
    main()