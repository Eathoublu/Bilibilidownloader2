import requests
from tqdm import tqdm
import time
import os
from utils.logger import logger
from utils.add_database import DBProxy  # insert_table_author, insert_table_dynamics, insert_table_collections, insert_table_follow, insert_table_video
# https://api.bilibili.com/x/space/acc/info?mid=297344797&jsonp=jsonp 用户个人信息


def evalable(text):
    return str(text).replace('false', 'False').replace('true', 'True').replace('null', 'None')

def sqlable(text):
    return text.replace('"', '·').replace('|', '、')

def pathable(text):
    return text.replace('/', '-').replace('(', '[').replace(')', ']').replace('\\', '-')


def get_profile(mid):
    url = 'https://api.bilibili.com/x/space/acc/info?mid={}&jsonp=jsonp'.format(mid)
    headers = {
        'access-control-allow-credentials': 'true',
        'access-control-allow-headers': 'Origin,No-Cache,X-Requested-With,If-Modified-Since,Pragma,Last-Modified,Cache-Control,Expires,Content-Type,Access-Control-Allow-Credentials,DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Cache-Webcdn,x-bilibili-key-real-ip,x-backend-bili-real-ip',
        'access-control-allow-methods': 'GET,POST',
        'access-control-allow-origin': 'https://space.bilibili.com',
        'bili-status-code': '0',
        # 'bili-trace-id': '1f031b45c60ffd5',
        'content-encoding': 'br',
        'content-type': 'application/json; charset=utf-8',
        'date': 'Tue, 27 Jul 2021 09:43:01 GMT',
        'vary': 'Origin',
        # 'x-cache-webcdn': 'BYPASS from blzone09'
    }
    req = requests.get(url, headers=headers)
    # print(req.text)
    return eval(req.text.replace('null', 'None').replace('false', 'False').replace('true', 'True'))

def get_raw_single_page(mid, page):
    url = 'https://api.bilibili.com/x/space/arc/search?mid={}&ps=30&tid=0&pn={}&keyword=&order=pubdate&jsonp=jsonp'.format(mid, page)
    headers = {
    'access-control-allow-credentials': 'true',
    'access-control-allow-headers': 'Origin,No-Cache,X-Requested-With,If-Modified-Since,Pragma,Last-Modified,Cache-Control,Expires,Content-Type,Access-Control-Allow-Credentials,DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Cache-Webcdn,x-bilibili-key-real-ip,x-backend-bili-real-ip',
    'access-control-allow-methods': 'GET,POST',
    'access-control-allow-origin': 'https://space.bilibili.com',
    'bili-status-code': '0',
    # 'bili-trace-id': '1f031b45c60ffd5',
    'content-encoding': 'br',
    'content-type': 'application/json; charset=utf-8',
    'date': 'Tue, 27 Jul 2021 09:43:01 GMT',
    'vary': 'Origin',
    # 'x-cache-webcdn': 'BYPASS from blzone09'
    }

    req = requests.get(url, headers=headers)
    # print(req.text)
    content = req.text.replace('null', 'None').replace('false', 'False').replace('true', 'True')
    return eval(content)

def get_author(mid):
    page = 1
    raw_content = []
    info_1 = {}
    while True:
        content = get_raw_single_page(mid, page)
        if content['data']['list']['tlist'] is not None:
            raw_content.append(content)
            if page == 1:
                info_1 = content['data']['list']['tlist']
            page += 1
        else:
            break
    return raw_content, info_1

def parse_content(content):
    # content = fake_content()
    # print(len(content))
    video_list = []
    try:
        basic_info_1 = content[0]['data']['list']['tlist']
    except:
        basic_info_1 = {}
    for pg in content:
        for v in pg['data']['list']['vlist']:
            # if v['mid'] == author_mid:
            video_list.append(
                {
                    'author':v['author'],
                    'mid':v['mid'],
                    'title':v['title'],
                    'comment':v['review'],
                    'pic':v['pic'],
                    'play':v['play'],
                    'created':v['created'],
                    'description': v['description'],
                    'length': v['length'],
                    'bvid':v['bvid'],
                    'aid':v['aid']
                }
            )
    # print(len(video_list))
    return video_list, basic_info_1

def micro_dm(bvid, mid):
    headers = {
    'accept': '*/*',
'accept-encoding': 'deflate',
'ccept-language': 'zh-CN,zh;q=0.9',
'cache-control': 'no-cache',
'pragma': 'no-cache',
'referer': 'https://space.bilibili.com/{}'.format(mid),
'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
'sec-ch-ua-mobile': '?0',
'sec-fetch-dest': 'script',
'sec-fetch-mode': 'no-cors',
'sec-fetch-site': 'same-site',
'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'}
    url = 'https://api.bilibili.com/x/v2/dm/ajax?aid={}'.format(bvid)
    req = requests.get(url, headers=headers)
    return eval(req.text.replace('null', 'None').replace('false', 'False').replace('true', 'True'))['data']

def fans_stat(mid):
    url = 'https://api.bilibili.com/x/relation/stat?vmid={}'.format(mid)
    headers = {
        'access-control-allow-credentials': 'true',
        'access-control-allow-headers': 'Origin,No-Cache,X-Requested-With,If-Modified-Since,Pragma,Last-Modified,Cache-Control,Expires,Content-Type,Access-Control-Allow-Credentials,DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Cache-Webcdn,x-bilibili-key-real-ip,x-backend-bili-real-ip',
        'access-control-allow-methods': 'GET,POST',
        'access-control-allow-origin': 'https://space.bilibili.com',
        'bili-status-code': '0',
        # 'bili-trace-id': '1f031b45c60ffd5',
        'content-encoding': 'br',
        'content-type': 'application/json; charset=utf-8',
        'date': 'Tue, 27 Jul 2021 09:43:01 GMT',
        'vary': 'Origin',
        # 'x-cache-webcdn': 'BYPASS from blzone09'
    }
    req = requests.get(url, headers=headers)
    return eval(req.text.replace('null', 'None').replace('false', 'False').replace('true', 'True'))

def parse_profile_info(info_1, info_2, info_3):
    """

    :param info_1: from 视频目录
    :param info_2: from 个人profile
    :param info_3: from fans stat
    :return:
    """
    info_2 = info_2['data']
    curr = time.time()
    return {'follower':info_3['data']['follower'],
            'following':info_3['data']['following'],
            'mid': info_3['data']['mid'],
            'key_words': [info_1[k]['name'] for k in info_1],
            'name': info_2['name'],
            'sex': info_2['sex'],
            'face': info_2['face'],
            'sign': info_2['sign'],
            'rank': info_2['rank'],
            'level': info_2['level'],
            'jointime': info_2['jointime'],
            'birthday': info_2['birthday'],
            'official': info_2['official']['title'],
            'vip_type': info_2['vip']['type'],
            'vip_status': info_2['vip']['status'],
            'vip_due': info_2['vip']['due_date'],
            'vip_pay_type': info_2['vip']['vip_pay_type'],
            'live_info': info_2['live_room']['url'],
            'live_title': info_2['live_room']['title'],
            'live_cover': info_2['live_room']['cover'],
            'spider_time': curr
            }
    pass

def save_imgs(info_d):
    face = requests.get(info_d['face'])
    if info_d['live_cover'] == 'NULL':
        return face.content, None
    else:
        cover = requests.get(info_d['live_cover'])
        return face.content, cover.content

def get_cover(url):
    cover = requests.get(url)
    return cover.content

def get_his_following(mid, db_proxy):
    """

    :param mid: up
    :return: <mid list>
    """
    headers = {
        'accept': '*/*',
'accept-encoding': 'deflate',
'accept-language': 'zh-CN,zh;q=0.9',
'cache-control': 'no-cache',
# 'cookie': "buvid3=2CD0AEF0-B134-3D0E-2811-B8761ABC5C6439485infoc; _uuid=45F1ECFC-CF41-5057-7B0F-A98059E33DF741329infoc; sid=jmqvgyjb; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(u))lJm~J)u0J'uYk~JYu)mm; fingerprint=633bee25f908ecc914be5cb23d475c7e; buvid_fp=2CD0AEF0-B134-3D0E-2811-B8761ABC5C6439485infoc; buvid_fp_plain=2CD0AEF0-B134-3D0E-2811-B8761ABC5C6439485infoc; PVID=1; bfe_id=1bad38f44e358ca77469025e0405c4a6",
'pragma': 'no-cache',
'referer': 'https://space.bilibili.com/{}/fans/follow'.format(mid),
'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
'sec-ch-ua-mobile': '?0',
'sec-fetch-dest': 'script',
'sec-fetch-mode': 'no-cors',
'sec-fetch-site': 'same-site',
'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
    }
    basic_url = 'https://api.bilibili.com/x/relation/followings?vmid={}&pn={}&ps=20&order=desc&jsonp=jsonp'
    pn = 1
    following = []
    while True:

        req = requests.get(url=basic_url.format(mid, pn), headers=headers)
        content = eval(evalable(req.text))
        for u in content['data']['list']:
            following.append({mid:u['mid']})
        pn += 1
        if pn > 5:
            break

    # print(following)
    # print(len(following))
    logger('Inserting followers...')
    for p in tqdm(following):
        db_proxy.insert_table_follow(mid, p[mid])

    return following

def get_his_follower(mid, db_proxy):
    """

    :param mid:up
    :return: <mid list>
    """
    """

        :param mid: up
        :return: <mid list>
        """
    headers = {
        'accept': '*/*',
        'accept-encoding': 'deflate',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        # 'cookie': "buvid3=2CD0AEF0-B134-3D0E-2811-B8761ABC5C6439485infoc; _uuid=45F1ECFC-CF41-5057-7B0F-A98059E33DF741329infoc; sid=jmqvgyjb; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(u))lJm~J)u0J'uYk~JYu)mm; fingerprint=633bee25f908ecc914be5cb23d475c7e; buvid_fp=2CD0AEF0-B134-3D0E-2811-B8761ABC5C6439485infoc; buvid_fp_plain=2CD0AEF0-B134-3D0E-2811-B8761ABC5C6439485infoc; PVID=1; bfe_id=1bad38f44e358ca77469025e0405c4a6",
        'pragma': 'no-cache',
        'referer': 'https://space.bilibili.com/{}/fans/follow'.format(mid),
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
    }
    basic_url = 'https://api.bilibili.com/x/relation/followers?vmid={}&pn={}&ps=20&order=desc&jsonp=jsonp'
    pn = 1
    follower = []
    while True:

        req = requests.get(url=basic_url.format(mid, pn), headers=headers)
        content = eval(evalable(req.text))
        for u in content['data']['list']:
            follower.append({mid: u['mid']})
        pn += 1
        if pn > 5:
            break

    # print(follower)
    # print(len(follower))
    logger('Inserting followers 2...')
    for p in tqdm(follower):
        db_proxy.insert_table_follow(p[mid], mid)
    #
    return follower

    pass

def get_his_updates(mid, db_proxy, down_pics=False, down_loc='temp/ups'):
    url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?visitor_uid=0&host_uid={}&offset_dynamic_id=0&need_top=1&platform=web'.format(mid)
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'accept-encoding': 'deflate',
'accept-language': 'zh-CN,zh;q=0.9',
'cache-control': 'no-cache',
 # 'cookie': "l=v; buvid3=2CD0AEF0-B134-3D0E-2811-B8761ABC5C6439485infoc; _uuid=45F1ECFC-CF41-5057-7B0F-A98059E33DF741329infoc; sid=jmqvgyjb; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(u))lJm~J)u0J'uYk~JYu)mm; fingerprint=633bee25f908ecc914be5cb23d475c7e; buvid_fp=2CD0AEF0-B134-3D0E-2811-B8761ABC5C6439485infoc; buvid_fp_plain=2CD0AEF0-B134-3D0E-2811-B8761ABC5C6439485infoc; PVID=1",
'pragma': 'no-cache',
'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
'sec-ch-ua-mobile': '?0',
'sec-fetch-dest': 'document',
'sec-fetch-mode': 'navigate',
'sec-fetch-site': 'none',
'sec-fetch-user': '?1',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
    }
    dynamics = []
    name = None
    logger('Now downloading dynamics...')
    while True:
        print('##', end='')
        req = requests.get(url, headers=headers)
        dy_content = eval(evalable(req.text))
        # print(dy_content)
        # quit()
        dynamics.append(dy_content)
        if dy_content['data']['next_offset']:
            url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?visitor_uid=0&host_uid={}&offset_dynamic_id={}&need_top=1&platform=web'.format(mid, dy_content['data']['next_offset'])
        else:
            break
    # print(len(dynamics))
    # quit()
    dy_lst = []
    # print(len(dynamics))
    for item in dynamics:
        try:
            # print('cards', len(item['data']['cards']))
            for d in item['data']['cards']:
                try:
                    d_content = eval(evalable(d['card'].replace('\/', '/')))
                    try:
                        if not name:name = d_content['user']['uname']
                    except:
                        pass
                    # print(d_content)
                    if 'origin' not in d_content:
                        # try:
                            say = sqlable(d_content['item']['description'])
                        # except:
                        #     say = 'NULL'
                        # try:
                            pics = [i['img_src'] for i in d_content['item']['pictures']]
                        # except:
                        #     pics = []
                        # try:
                            reply = d_content['item']['reply']
                        # except:
                        #     reply = 0
                        # try:
                            upload_time = d_content['item']['upload_time']
                        # except:
                        #     upload_time = 'NULL'
                            dy_lst.append({'from':None, 'origin_say':None , 'say': say, 'pics':pics, 'reply':reply, 'upload_time': upload_time})
                    else:
                            d_content = eval(evalable(d['card'].replace('\/', '/')))
                        # print(d_content.keys())
                        # print(d_content['origin'])
                        # quit()
                            origin_parse = eval(evalable(d_content['origin'].replace('\/', '/')))

                        # try:
                            _from =  origin_parse['owner']['mid']
                        # except:
                        #     _from = 'unknown'
                        # try:
                            origin_say = sqlable(origin_parse['dynamic'])
                        # except:
                        #     origin_say = 'unknown'

                        # try:
                            say = sqlable(d_content['item']['content'])
                        # except:
                        #     say = 'NULL'

                        # try:
                            pics = [i['img_src'] for i in origin_parse['pic']] if type(origin_parse['pic']) == list else [origin_parse['pic'], ]
                        # except:
                        #     pics = []

                        # try:
                            reply = d_content['item']['reply']
                        # except:
                        #     reply = 0

                        # try:
                            upload_time = d_content['item']['timestamp']
                        # except:
                        #     upload_time = 'NULL'


                            dy_lst.append({'from': _from,
                                       'origin_say': origin_say,
                                       'say': say,
                                       'pics': pics,
                                       'reply': reply,
                                       'upload_time': upload_time})
                except:
                    pass

        except:
            pass
    # print(len(dy_lst))
    # print(dy_lst)
    # quit()
    logger('Inserting dynamics...')
    for d in tqdm(dy_lst):
        db_proxy.insert_table_dynamics(d, mid)
    if down_pics:
        if not os.path.exists('{}/{}'.format(down_loc, name)):
            os.mkdir('{}/{}'.format(down_loc, name))
        logger('Downloading dy-pics...')
        for d in tqdm(dy_lst):
            idx = 0
            for p in d['pics']:
                try:
                    idx += 1
                    if os.path.exists('{}/{}/{}_{}.jpg'.format(down_loc, pathable(name), pathable(d['say'][:30]), idx)):
                        continue
                    content = requests.get(p, headers=headers)
                    try:
                        with open('{}/{}/{}_{}.jpg'.format(down_loc, pathable(name), pathable(d['say'][:30]), idx), 'wb') as f:
                            f.write(content.content)
                            f.close()
                    except:
                        with open('{}/{}/{}.jpg'.format(down_loc, pathable(name), str(int(time.time()))), 'wb') as f:
                            f.write(content.content)
                            f.close()
                except:
                    pass


    return dy_lst

def get_collects(mid, db_proxy):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'deflate',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        # 'cookie': "l=v; buvid3=2CD0AEF0-B134-3D0E-2811-B8761ABC5C6439485infoc; _uuid=45F1ECFC-CF41-5057-7B0F-A98059E33DF741329infoc; sid=jmqvgyjb; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(u))lJm~J)u0J'uYk~JYu)mm; fingerprint=633bee25f908ecc914be5cb23d475c7e; buvid_fp=2CD0AEF0-B134-3D0E-2811-B8761ABC5C6439485infoc; buvid_fp_plain=2CD0AEF0-B134-3D0E-2811-B8761ABC5C6439485infoc; PVID=1",
        'pragma': 'no-cache',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
    }
    url = 'https://api.bilibili.com/x/v3/fav/folder/created/list?pn=1&ps=10&up_mid={}&jsonp=jsonp'.format(mid)
    pn = 1
    coll_lst = []
    while True:
        content = requests.get(url, headers=headers)
        coll_menu = eval(evalable(content.text))
        # print(coll_menu)
        try:
            coll_lst += coll_menu['data']['list']
        except:
            logger('He didnt public his collections.')
            break
        if not coll_menu['data']['has_more']:
            break
        else:
            pn += 1
            url = 'https://api.bilibili.com/x/v3/fav/folder/created/list?pn={}&ps=10&up_mid={}&jsonp=jsonp'.format(pn, mid)
    # print(coll_lst)
    # print(len(coll_lst))

    url_2 = 'https://api.bilibili.com/x/v3/fav/resource/list?media_id={}&pn={}&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp'

    vids = {}

    for coll in coll_lst:
        vids[coll['title']] = {'all_bv':None, 'count':coll['media_count']}
        media_id = coll['id']
        pn = 1
        vid_in_coll = []
        while True:
            _url = url_2.format(media_id, pn)
            content = requests.get(_url, headers=headers)
            vid_content = eval(evalable(content.text))
            vid_in_coll += [{'bv':v['bvid'], 'title':v['title']} for v in vid_content['data']['medias']]
            if pn >= 5 or not vid_content['data']['has_more']:
                break
            else:
                pn += 1
        vids[coll['title']]['all_bv'] = vid_in_coll

    # print(vids)
    logger('Inserting collections...')
    for c in tqdm(vids):
        db_proxy.insert_table_collections({'mid':mid, 'videos':sqlable(str(vids[c]['all_bv'])), 'count':vids[c]['count'], 'title':sqlable(c)})






        # a = {'code': 0, 'message': '0', 'ttl': 1, 'data': {'count': 5, 'list': [{'id': 54038702, 'fid': 540387, 'mid': 42784402, 'attr': 0, 'title': '默认收藏夹', 'cover': 'http://i1.hdslb.com/bfs/archive/9675334a5bc93b878b1227a6d330eadb28acf5d8.jpg', 'upper': {'mid': 42784402, 'name': '', 'face': ''}, 'cover_type': 2, 'intro': '', 'ctime': 1474071821, 'mtime': 1583141921, 'state': 0, 'fav_state': 0, 'media_count': 1231, 'view_count': 0, 'type': 0, 'link': ''}, {'id': 702632802, 'fid': 7026328, 'mid': 42784402, 'attr': 22, 'title': 'ARRRRRRT', 'cover': 'http://i1.hdslb.com/bfs/archive/bf23ce6668c006844b0db17afed21855e5b45105.png', 'upper': {'mid': 42784402, 'name': '', 'face': ''}, 'cover_type': 2, 'intro': '', 'ctime': 1564984171, 'mtime': 1584847285, 'state': 0, 'fav_state': 0, 'media_count': 55, 'view_count': 0, 'type': 0, 'link': ''}, {'id': 846158702, 'fid': 8461587, 'mid': 42784402, 'attr': 22, 'title': '日常健身', 'cover': 'http://i2.hdslb.com/bfs/archive/64a46fcd19aeb36e08ccf9ef2f544f624dc83a7d.jpg', 'upper': {'mid': 42784402, 'name': '', 'face': ''}, 'cover_type': 2, 'intro': '', 'ctime': 1582552245, 'mtime': 1582552245, 'state': 0, 'fav_state': 0, 'media_count': 15, 'view_count': 0, 'type': 0, 'link': ''}, {'id': 422796602, 'fid': 4227966, 'mid': 42784402, 'attr': 22, 'title': '失眠福音', 'cover': 'http://i2.hdslb.com/bfs/archive/e44d129e9d20936a76a9f50a071c6e9da0f9ac75.jpg', 'upper': {'mid': 42784402, 'name': '', 'face': ''}, 'cover_type': 2, 'intro': '', 'ctime': 1555101870, 'mtime': 1556657480, 'state': 0, 'fav_state': 0, 'media_count': 13, 'view_count': 0, 'type': 0, 'link': ''}, {'id': 192468202, 'fid': 1924682, 'mid': 42784402, 'attr': 2, 'title': '学习', 'cover': 'http://i0.hdslb.com/bfs/archive/219731dbe48f2886cde76475e919c156c48d66bf.jpg', 'upper': {'mid': 42784402, 'name': '', 'face': ''}, 'cover_type': 2, 'intro': '', 'ctime': 1530062080, 'mtime': 1557818801, 'state': 0, 'fav_state': 0, 'media_count': 32, 'view_count': 0, 'type': 0, 'link': ''}], 'has_more': False}}

def act_find_author(mid, db_proxy):
    raw_content, info_1 = get_author(mid)
    video_lst, _ = parse_content(raw_content)
    info_2 = get_profile(mid)
    info_3 = fans_stat(mid)
    info_d = parse_profile_info(info_1, info_2, info_3)
    # print(info_d)
    for k in info_d:
        if info_d[k] == '' or info_d[k] is None:
            info_d[k] = 'NULL'
    face, live_cover = save_imgs(info_d)
    info_d['face_img'] = face
    info_d['cover_img'] = live_cover
    for k in info_d:
        if info_d[k] == '' or info_d[k] is None:
            info_d[k] = 'NULL'
    # with open('test.jpg', 'wb') as f:
    #     f.write(face)

    db_proxy.insert_table_author(info_d)

    # print(video_lst)
    # quit()
    # return
    logger('Inserting videos...')
    for v in tqdm(video_lst):
        dm = micro_dm(v['bvid'], mid)
        # print(dm)
        # quit()
        v['dm'] = dm
        cover_img = get_cover(v['pic'])
        v['cover'] = cover_img
        db_proxy.insert_table_video(v)


    return {'video_lst': video_lst,
            'profile': info_d,
           'face': face,
           'live_cover': live_cover,
            'follower': None,
            'follwing': None,
            'video_dm': None
            }

def run(mid, down_pics, down_loc, db_path):
    dbproxy = DBProxy(db_path)
    act_find_author(mid, dbproxy)
    get_collects(mid, dbproxy)
    get_his_following(mid, dbproxy)
    get_his_follower(mid, dbproxy)
    get_his_updates(mid, down_pics=down_pics, down_loc=down_loc, db_proxy=dbproxy)

    pass

if __name__ == '__main__':

    pass

    # run(285478186, down_pics=True, down_loc='temp2', db_path='test2.db')

    # print(pathable('/只要太阳出来，就会有好心情☀️\U0001fab4🐈_1.jpg'))
    # print(os.path.isfile(pathable('a.txt')))
    # quit()


    # print(get_raw_single_page('297344797', 1))
    # raw_content, info_1 = get_author('297344797')
    # print(info_1)
    # print(parse_content())
    # micro_dm('297344797')
    # print(get_profile('297344797'))
    # print(fans_stat('297344797'))
    # act_find_author('297344797')
    # act_find_author('12473905')
    # act_find_author('480404755')
    # get_his_updates('42784402', down_pics=True)
    # get_his_updates('480404755', down_pics=True)
    # get_collects('23064683')
    # get_collects('42784402')
    # get_his_following('42784402')
    # get_his_follower('42784402')

    dbproxy = DBProxy('test2.db')
    get_his_updates(297344797, dbproxy, down_loc='temp2', down_pics=True)
