# -*- coding:utf-8 -*-
import requests
import json

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


# url = "http://ib.snssdk.com/api/2/wap/search_content/?from=search_tab&keyword=vivo%20x20&plugin_enable=3&followbtn_template=%7B%2522color_style%2522%3A%2522red%2522%7D&iid=15456210477&device_id=39490187575&ac=wifi&channel=baidu&aid=13&app_name=news_article&version_code=636&version_name=6.3.6&device_platform=android&ab_version=173477%252C179885%252C159913%252C177252%252C179332%252C181412%252C172664%252C172658%252C171194%252C180360%252C181466%252C170354%252C180929%252C178898%252C181479%252C179981%252C171602%252C169430%252C179196%252C178242%252C174396%252C178732%252C180777%252C181197%252C181230%252C180699%252C177166%252C152027%252C176590%252C181531%252C177009%252C178532%252C180705%252C180718%252C181217%252C170713%252C179372%252C176739%252C156262%252C145585%252C179382%252C174430%252C181819%252C177257%252C181223%252C176457%252C162572%252C181181%252C176601%252C176609%252C179624%252C169176%252C175631%252C179898%252C176617%252C164943%252C170988%252C180928%252C181000%252C178902%252C176596%252C176653%252C177702%252C176615%252C180150%252C180117&ab_client=a1%252Cc4%252Ce1%252Cf2%252Cg2%252Cf7&ab_feature=94563%252C102749&abflag=3&device_type=SM-N900P&device_brand=samsung&language=zh&os_api=19&os_version=4.4.2&uuid=864394010762047&openudid=4ccc6af075ab2956&manifest_version_code=636&resolution=1280*720&dpi=240&update_version_code=6368&_rticket=1506395883474&plugin=2431&search_sug=1&forum=1&latitude=30.001249999999995&longitude=110.56358166666665&no_outsite_res=0&as=A1E579FCD93C6EC&cp=59C9DC263EFC9E1&count=10&cur_tab=1&format=json&offset=10&search_text=vivo%20x20&keyword_type=&action_type=input_keyword_search&search_id=20170928095845172016006165414302"

def search(offset):
    searchtext = 'vivo%20x20'
    search_id = "20170928095845172016006165414302"
    url = "http://ib.snssdk.com/api/2/wap/search_content/?from=search_tab&keyword={}&plugin_enable=3&followbtn_template=%7B%2522color_style%2522%3A%2522red%2522%7D&iid=15456210477&device_id=39490187575&ac=wifi&channel=baidu&aid=13&app_name=news_article&version_code=636&version_name=6.3.6&device_platform=android&ab_version=173477%252C179885%252C159913%252C177252%252C179332%252C181412%252C172664%252C172658%252C171194%252C180360%252C181466%252C170354%252C180929%252C178898%252C181479%252C179981%252C171602%252C169430%252C179196%252C178242%252C174396%252C178732%252C180777%252C181197%252C181230%252C180699%252C177166%252C152027%252C176590%252C181531%252C177009%252C178532%252C180705%252C180718%252C181217%252C170713%252C179372%252C176739%252C156262%252C145585%252C179382%252C174430%252C181819%252C177257%252C181223%252C176457%252C162572%252C181181%252C176601%252C176609%252C179624%252C169176%252C175631%252C179898%252C176617%252C164943%252C170988%252C180928%252C181000%252C178902%252C176596%252C176653%252C177702%252C176615%252C180150%252C180117&ab_client=a1%252Cc4%252Ce1%252Cf2%252Cg2%252Cf7&ab_feature=94563%252C102749&abflag=3&device_type=SM-N900P&device_brand=samsung&language=zh&os_api=19&os_version=4.4.2&uuid=864394010762047&openudid=4ccc6af075ab2956&manifest_version_code=636&resolution=1280*720&dpi=240&update_version_code=6368&_rticket=1506395883474&plugin=2431&search_sug=1&forum=1&latitude=30.001249999999995&longitude=110.56358166666665&no_outsite_res=0&as=A1E579FCD93C6EC&cp=59C9DC263EFC9E1&count=10&cur_tab=1&format=json&offset={}&search_text={}&keyword_type=&action_type=input_keyword_search&search_id={}". \
        format(searchtext, offset, searchtext, search_id)
    result = requests.get(url).text
    data = json.loads(result)['data']
    print len(data)
    with open('titles.txt', 'a')as f:
        for item in data:
            try:
                title = item['title']
                f.write(title + '\n')
            except:
                continue
                pass


def test():
    for i in range(10):
        search(i * 10)


def count():
    temp = []
    with open('titles.txt', 'r') as f:
        data = f.readlines()
        print len(data)
        for item in data:
            temp.append(item)
    print len(set(temp))


pass

if __name__ == '__main__':
    test()
    # count()
