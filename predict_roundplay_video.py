import os
import json
from argparse import ArgumentParser
from datetime import datetime
import pytz
from collections import OrderedDict

from roundplay_info_fetcher import fetch_roundplay_info


def load_roundplay_list(roundplay_seq_path):
    roundplay_seq = OrderedDict()
    with open(roundplay_seq_path, 'r') as f:
        for line in f:
            eles = line.rstrip('\r\n').split(',', 5)
            seq, bvid, pid, duration, url, title = int(eles[0]), eles[1], int(eles[2]), int(eles[3]), eles[4], eles[5]
            roundplay_seq[seq] = (bvid, pid, duration, url, title)
    return roundplay_seq


def predict_roundplay_video(room_id, dt, seq_dict):
    curr_info = json.loads(fetch_roundplay_info(room_id))
    sequence, play_time = curr_info['data']['sequence'], curr_info['data']['play_time']

    x = datetime.now()
    x = x.replace(tzinfo=x.astimezone().tzinfo)
    assert (dt >= x), 'Time to predict should be later than the current time!\nCurrent time: {}\nTime to predict: {}'.format(x, dt)
    after_time = int((dt - x).total_seconds())

    sum_play_time = after_time + play_time
    seq_i = sequence
    summed_play_time = 0

    while True:
        while seq_i not in seq_dict:
            seq_i += 1
            if seq_i > max(seq_dict.keys()):
                seq_i = 1
        summed_play_time += seq_dict[seq_i][2]
        if summed_play_time > sum_play_time:
            break
        seq_i += 1
        if seq_i > max(seq_dict.keys()):
            seq_i = 1

    if seq_i not in seq_dict:
        return None
    else:
        will_play = seq_i
        bvid, pid, duration, url, title = seq_dict[will_play]
        will_play_time = duration - (summed_play_time - sum_play_time)
        url += '&t={}'.format(int(will_play_time))
        return (bvid, pid, will_play_time, url, title)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('room_id', type=int, default=21602686)
    parser.add_argument('datetime', type=str, help='format: %Y-%m-%d-%H-%M')
    parser.add_argument('--timezone', default='Asia/Shanghai')
    parser.add_argument('--fetch_folder', default='.')
    args = parser.parse_args()

    seq_dict = load_roundplay_list(os.path.join(args.fetch_folder, 'roundplay_seq.txt'))
    room_id = args.room_id
    dt = datetime.strptime(args.datetime, '%Y-%m-%d-%H-%M')
    dt = pytz.timezone(args.timezone).localize(dt)
    prediction = predict_roundplay_video(room_id, dt, seq_dict)
    print('bvid:', prediction[0])
    print('pid:', prediction[1])
    print('title:', prediction[4])
    print('time: {}:{}'.format(prediction[2] // 60, prediction[2] % 60))
    print('url:', prediction[3])
