from sys import argv
from os import path
from pytube import YouTube
import argparse
import numpy as np
import cv2
import json

def download_video(url, dest):
  yt = YouTube(url)
  video = yt.filter('mp4')[0]
  filename = yt.filename
  if not path.isdir(dest):
    head, tail = path.split(dest)
    filename = tail.split(".")[0]
    dest = head
  yt.set_filename("".join([filename, ".", yt.video_id]))
  video.download(dest)
  print("Video saved to:", "".join([dest, "/", yt.filename, ".mp4"]))

def generate_animation(vid, dest):
  emotions = {
    "idle": "idle",
    "think": "io11/think",
    "look": "io2/look",
    "distress": "io5/distress",
    "fear": "io1/fear",
  }
  emote = "idle"
  head, tail = path.split(vid)
  vid_json = { "videoID": tail.split(".")[-2], "triggers": {} }

  cap = cv2.VideoCapture(vid)

  # Check if camera opened successfully
  if (cap.isOpened()== False):
    print("Error opening video stream or file")

  # Read until video is completed
  while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
      blackness = 1 - detect_color(frame)
      time, emote = handle_blackness(blackness, cap.get(cv2.CAP_PROP_POS_MSEC), emote)
      if time:
        vid_json["triggers"][time] = {
          "emotion": emote,
          "gesture": emotions[emote],
        }
        print(time, emote, blackness)

      # Press Q on keyboard to  exit
      if cv2.waitKey(25) & 0xFF == ord('q'):
        break

    else:
      break

  # When everything done, release the video capture object
  cap.release()

  # Closes all the frames
  cv2.destroyAllWindows()

  if path.isdir(dest):
    dest = "".join([dest, "/", tail.split(".")[0], ".json"])
  with open(dest, 'w+') as dest_file:
    json.dump(vid_json, dest_file, sort_keys=True, indent=4, separators=(',', ': '))

def handle_blackness(blackness, time, prev_emote):
  if blackness < .15:
    emote = "idle"
  elif blackness < .25:
    emote = "think"
  elif blackness < .35:
    emote = "look"
  elif blackness < .5:
    emote = "distress"
  elif blackness < .9:
    emote = "fear"
  else:
    emote = "idle"
  return [time, emote] if emote != prev_emote else [None, emote]

def detect_color(img):
  color_ranges = [
  	([200, 200, 200], [255, 255, 255]),
  	# ([50, 100, 0], [255, 255, 100]),
  ]
  masks = []
  for (lower, upper) in color_ranges:
    lower = np.array(lower)
    upper = np.array(upper)

    masks.append(cv2.inRange(img, lower, upper))
  cv2.imshow('colors', np.hstack([img] + [cv2.bitwise_and(img, img, mask=mask) for mask in masks]))
  white_mask = masks[0]
  return cv2.countNonZero(white_mask) / white_mask.size


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Download and process Youtube videos.')
  parser.add_argument("-v", "--video", type=str, nargs=1, help="A Youtube video url to download")
  parser.add_argument("-d", "--destination", type=str, nargs=1, help="The destination dir of any outputs.")
  parser.add_argument("-p", "--process", type=str, nargs=1, help="Path to a locally stored video to process")

  args = parser.parse_args()

  dest = args.destination or ["."]
  if args.video:
    download_video(args.video[0], dest[0])
  elif args.process:
    generate_animation(args.process[0], dest[0])
  else:
    print("Type -h or --help for help.")
