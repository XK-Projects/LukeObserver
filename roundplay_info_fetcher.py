'''
https://api.live.bilibili.com/live/getRoundPlayVideo?room_id=<room_id>


Response example:
{'code': 0,
 'msg': 'ok',
 'message': 'ok',
 'data': {'cid': 185849088,
  'play_time': 588,
  'sequence': 57,
  'aid': 838101812,
  'title': 'BV12g4y1q7Hf-【2020.05.01录播】劳动最光荣！-P1',
  'pid': 1,
  'bvid_url': 'https://www.bilibili.com/video/BV12g4y1q7Hf',
  'bvid': 'BV12g4y1q7Hf',
  'play_url': 'https://interface.bilibili.com/v2/playurl?appkey=fb06a25c6338edbc&buvid=&cid=185849088&otype=json&platform=live&qn=64&type=mp4&sign=5c8c147852cf7729ffced20209cccaee'}}

'''


import os
import sys
import json
import gzip
from argparse import ArgumentParser
from datetime import datetime
import time

import requests


def fetch_roundplay_info(room_id):
    request_url = 'https://api.live.bilibili.com/live/getRoundPlayVideo'
    r = requests.get(request_url, params={'room_id': room_id})
    try:
        r_text = r.text
    except:
        r_text = ''
    return r_text


def main(args):
    room_id = args.room_id
    save_dir = os.path.join(args.save_dir, str(room_id))
    sleep_sec = args.sleep_sec
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, '{}.txt.gz'.format(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')))

    while True:
        timestamp = datetime.timestamp(datetime.now())
        rpinfo_text = fetch_roundplay_info(room_id)
        line = '{:f},{}'.format(timestamp, rpinfo_text)
        print(line)
        with gzip.open(save_path, 'at') as f:
            f.write(line + '\n')
        time.sleep(sleep_sec)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('room_id', type=int, default=21602686)
    parser.add_argument('--save_dir', type=str, default='results')
    parser.add_argument('--sleep_sec', type=int, default=60)
    args = parser.parse_args()
    main(args)
