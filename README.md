# 录萪观察者 (LukeObserver)

收集Bilibili直播间的轮播列表并预测未来给定时间录播播放的视频。

## 收集轮播列表

目前没找到B站直接获取轮播列表的API，暂时采用定时获取当前轮播视频的方式累积轮播列表的信息。

```bash
# 每60s获取一次当前轮播视频，应保持后台运行
python roundplay_info_fetcher.py <room_id> --save_dir results --sleep_sec 60
```

## 获取轮播视频信息

```bash
# 获取收集到的轮播列表中所有视频的信息（包括视频时长）
python gen_roundplay_video_list.py --fetch_folder results/<room_id> --sleep_sec 2
```

## 示例CLI程序：读取轮播列表和视频信息，预测未来给定时间的轮播视频

```bash
# 默认输入时间为北京时间
python predict_roundplay_video.py <room_id> <%Y-%m-%d-%H-%M> --fetch_folder results/<room_id>
```
