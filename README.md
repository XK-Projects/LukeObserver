# 录萪观测者 (LukeObserver)

收集Bilibili直播间的轮播列表并预测未来给定时间录播播放的视频。

## 配置环境

- python >= 3.6
- requests
- tqdm
- pytz

## 收集轮播列表

目前没找到B站直接获取轮播列表的API，暂时采用定时获取当前轮播视频的方式累积轮播列表的信息。

```bash
# 每60s获取一次当前轮播视频，应保持后台运行
python roundplay_info_fetcher.py <room_id>
```

## 获取轮播视频信息

```bash
# 获取收集到的轮播列表中所有视频的信息（包括视频时长）
python gen_roundplay_video_list.py <room_id>
```

## 文件说明

录播列表存储在`results/<room_id>`下，包括：

- `<datetime>.txt.gz`: 累积的当前录播视频查询结果
- `video_info.txt`: 累积的录播视频信息
- `roundplay_seq.json`: 录播列表，包括`[在录播列表内的序号(从1开始), BV号, 分P序号, 视频时长(秒), URL, 视频标题]`

## 示例CLI程序：读取轮播列表和视频信息，预测未来给定时间的轮播视频

```bash
# 默认输入时间为北京时间，格式<yyyy-mm-dd-HH-MM>，必须晚于当前时间
python predict_roundplay_video.py <room_id> <%Y-%m-%d-%H-%M>
```

输入输出示例:

```bash
python predict_roundplay_video.py 21602686 "2021-03-08-19-00"
--------------------------------------------------------------------------------------------------------------
bvid: BV1zg4y1q7mc
pid: 1
title: BV1zg4y1q7mc-【2020.06.12录播】夏日大作战-P1
time: 63:5
url: https://www.bilibili.com/video/BV1zg4y1q7mc?p=1&t=3785
```
