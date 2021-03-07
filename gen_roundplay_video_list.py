'''
Generate the list of roundplay videos from fetched roundplay info, including the duration of each video.
'''

import os
import shutil
import gzip
import json
from argparse import ArgumentParser
import time
from collections import OrderedDict
from datetime import datetime

import requests
from tqdm import tqdm

from roundplay_info_fetcher import fetch_roundplay_info


def fetch_video_info(bvid):
    request_url = 'https://api.bilibili.com/x/web-interface/view'
    r = requests.get(request_url, params={'bvid': bvid})
    try:
        r_text = r.text
    except:
        r_text = ''
    return r_text


def main(args):
    # load fetched roundplay info
    fetch_folder = args.fetch_folder
    gzfiles = sorted([x for x in os.listdir(fetch_folder) if x.endswith('.txt.gz')])
    tdpairs = []
    for gzfile in gzfiles:
        with gzip.open(os.path.join(fetch_folder, gzfile), 'rt') as f:
            for line in f:
                timestamp, jsonstr = line.split(',', 1)
                data = json.loads(jsonstr)['data']
                if data:
                    tdpairs.append((timestamp, data))
    seq_dict = {}
    for _, data in tdpairs:    
        idx = data['sequence']
        bvid = data['bvid']
        pid = data['pid']
        title = data['title']
        seq_dict[idx] = (bvid, pid, title)
    seq_dict = OrderedDict(sorted(seq_dict.items())) # sequence -> (bvid, pid, title)

    # load saved video_info
    video_list = []
    saved_video_info = os.path.join(fetch_folder, 'video_info.txt')
    if os.path.exists(saved_video_info):
        shutil.copy(saved_video_info, saved_video_info + '.bk')
        with open(saved_video_info, 'r') as f:
            for line in f:
                line = line.rstrip('\r\n')
                eles = line.split(',', 1)
                video_list.append((eles[0], eles[1]))
    video_dict = OrderedDict(sorted(video_list))

    # add new videos if necessary
    new_bvids = []
    for _, v in seq_dict.items():
        if v[0] not in video_dict:
            new_bvids.append(v[0])
    new_bvids = sorted(list(set(new_bvids)))
    print('Found {} new videos. Fetching information...'.format(len(new_bvids)))
    for bvid in tqdm(new_bvids):
        video_info = fetch_video_info(bvid)
        video_dict[bvid] = video_info
        time.sleep(args.sleep_sec)
    video_dict = OrderedDict(sorted(video_dict.items()))
    with open(saved_video_info, 'w') as f:
        for x in video_dict.items():
            f.write(','.join(x) + '\n')

    # save roundplay seq with durations
    seq_dict_with_du = {}
    for k, (bvid, pid, title) in seq_dict.items():
        video_info = json.loads(video_dict[bvid])
        duration = video_info['data']['pages'][pid - 1]['duration']
        video_url = 'https://www.bilibili.com/video/{}?p={}'.format(bvid, pid)
        seq_dict_with_du[k] = {
            'bvid': bvid, 'pid': pid, 'duration': duration,
            'video_url': video_url, 'title': title
        }
    # save fetch result for static query
    curr_info = json.loads(fetch_roundplay_info(args.room_id))
    sequence, play_time = curr_info['data']['sequence'], curr_info['data']['play_time']
    curr_time = datetime.now()
    curr_time = curr_time.replace(tzinfo=curr_time.astimezone().tzinfo)
    curr_play = {
        'time': curr_time.isoformat(),
        'sequence': sequence,
        'play_time': play_time
    }

    to_save_dict = {
        'roundplay_seq': seq_dict_with_du,
        'curr_play': curr_play
    }

    with open(os.path.join(args.fetch_folder, 'roundplay_seq.json'), 'w') as f:
        json.dump(to_save_dict, f)
    if not os.path.exists(args.site_folder):
        os.makedirs(args.site_folder, exist_ok=True)
    with open(os.path.join(args.site_folder, 'roundplay_seq.json'), 'w') as f:
        json.dump(to_save_dict, f)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('room_id', type=int, default=21602686)
    parser.add_argument('--fetch_folder', default='.')
    parser.add_argument('--site_folder', default='.')
    parser.add_argument('--sleep_sec', type=int, default=2)
    
    args = parser.parse_args()
    
    args.fetch_folder = os.path.join('results', str(args.room_id))
    args.site_folder = os.path.join('site', 'assets', 'rplist', str(args.room_id))
    
    main(args)
