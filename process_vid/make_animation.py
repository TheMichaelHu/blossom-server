from os import path
from pytube import YouTube
import argparse
import numpy as np
import cv2
import json
from sklearn.cluster import KMeans
from scipy.spatial.distance import cosine


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
    "look": "io2/look",
    "think": "io11/think",
    "look": "io2/look",
    "distress": "io5/distress",
    "fear": "io1/fear",
    "calm": "io8/calm",
    "sad": "io7/sad",
  }
  emote = ""
  head, tail = path.split(vid)
  vid_json = {"videoId": tail.split(".")[-2], "triggers": []}

  cap = cv2.VideoCapture(vid)

  # Check if camera opened successfully
  if not cap.isOpened():
    print("Error opening video stream or file")

  # Read until video is completed
  while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
      color = detect_color(frame)
      time, emote = handle_color(color, cap.get(cv2.CAP_PROP_POS_MSEC), emote)
      if time:
        vid_json["triggers"].append({
          "time": time,
          "emotion": emote,
          "gesture": emotions[emote],
        })
        print(time, emote)

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
  with open("./demo/gestures.es6", 'w+') as dest_file:
    dest_file.write("var emotions =\n")
    json.dump(vid_json, dest_file, sort_keys=True, indent=4, separators=(',', ': '))


def handle_color(color, time, prev_emote):
  cen_color = color - np.mean(color)
  colors = {
    "red": cosine(cen_color, np.array([[0, 0, 1]])),
    "yellow": cosine(cen_color, np.array([[0, 1, 1]])),
    "green": cosine(cen_color, np.array([[0, 1, 0]])),
    "blue": cosine(cen_color, np.array([[1, 0, 0]])),
    "purple": cosine(cen_color, np.array([[2, 0, 1]])),
    "pink": cosine(cen_color, np.array([[1, 0, 1]])),
    "gray": cosine(cen_color, np.array([[1, 1, 1]])),
  }
  best_color = min(colors, key=colors.get)

  if best_color == "red":
    emote = "fear"
  elif best_color == "yellow":
    emote = "calm"
  elif best_color == "green":
    emote = "look"
  elif best_color == "blue":
    emote = "sad"
  elif best_color == "purple":
    emote = "distress"
  elif best_color == "pink":
    emote = "think"
  else:
    emote = "think"

  if emote != prev_emote:
    print(best_color)

  return [time, emote] if emote != prev_emote else [None, emote]


def detect_color(img):
  image = img.reshape((img.shape[0] * img.shape[1], 3))
  kmeans = KMeans(n_clusters=2, max_iter=20, n_init=1)
  kmeans.fit(image)

  counts = np.bincount(kmeans.labels_).tolist()
  center = kmeans.cluster_centers_[counts.index(max(counts))]

  lower, upper = center - 60, center + 60
  cv2.imshow('colors', np.hstack([img, cv2.bitwise_and(img, img, mask=cv2.inRange(img, lower, upper))]))

  return center


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
