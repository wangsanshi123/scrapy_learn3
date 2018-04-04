import json


def test1():
    with open('missedArticles.json', 'r+') as f:
        data = json.load(f)
        for item in data:
            try:
                print item['title']
            except:
                print "title is null"
                pass
    pass


if __name__ == '__main__':
    test1()
