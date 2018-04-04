import requests


def test():
    # url = "https://www.zhihu.com/search?type=content&q=vivo+x20"
    # url = "https://www.zhihu.com/r/search?q=vivo+x20&correction=1&type=content&offset=10"
    time = 0
    offset = 0
    runFlag = True
    keyword = 'vivo+x20'
    while runFlag:
        if time > 0:
            break
        url = "https://www.zhihu.com/r/search?q={}&correction=1&type=content&offset={}".format(keyword, offset)
        print url
        user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0"
        headers = {"User-Agent": user_agent}
        result = requests.get(url, headers=headers)
        print result.text


        time += 1
        offset += 10


if __name__ == '__main__':
    test()
