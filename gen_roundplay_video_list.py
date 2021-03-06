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

import requests
from tqdm import tqdm


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
    seq_dict_with_du = OrderedDict()
    for k, (bvid, pid, title) in seq_dict.items():
        video_info = json.loads(video_dict[bvid])
        duration = video_info['data']['pages'][pid - 1]['duration']
        video_url = 'https://www.bilibili.com/video/{}?p={}'.format(bvid, pid)
        seq_dict_with_du[k] = (bvid, pid, duration, video_url, title)
    with open(os.path.join(args.fetch_folder, 'roundplay_seq.txt'), 'w') as f:
        for k, v in seq_dict_with_du.items():
            line = [str(k)] + list(map(str, v))
            f.write(','.join(line) + '\n')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--fetch_folder', default='.')
    parser.add_argument('--sleep_sec', type=int, default=2)
    
    args = parser.parse_args()
    main(args)
