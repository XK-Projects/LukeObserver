# roundplay_info_fetcher

Scripts for fetching roundplay information of Bilibili Live.

## Collect roundplay list

```bash
# Collect the video in roundplay now, every 60 seconds. Should be kept running in background.
python roundplay_info_fetcher.py <room_id> --save_dir results --sleep_sec 60
```

## Get video information, including duration

```bash
# Run this when new videos are found in the roundplay list. Should be executed in a relatively low freq (e.g. every day/week)
python gen_roundplay_video_list.py --fetch_folder results/<room_id> --sleep_sec 2
```

## Predict the video in roundplay at desired time

```bash
# A demo for prediction, using Beijing time by default
python predict_roundplay_video.py <room_id> <%Y-%m-%d-%H-%M> --fetch_folder results/<room_id>
```
