from sys import argv
from pytube import YouTube
import argparse
import numpy as np
import cv2

def download_video(url, dest):
  yt = YouTube(url)
  video = yt.filter('mp4')[0]
  video.download(dest)

def generate_animation(vid, dest):
  cap = cv2.VideoCapture(vid)

  while(cap.isOpened()):
      ret, frame = cap.read()

      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      print(gray)

      cv2.imshow('frame',gray)
      if cv2.waitKey(1) & 0xFF == ord('q'):
          break

  cap.release()
  cv2.destroyAllWindows()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Download and process Youtube videos.')
  parser.add_argument("-v", "--video", type=str, nargs=1, help="A Youtube video url to download")
  parser.add_argument("-d", "--destination", type=str, nargs=1, help="The destination path of any outputs.")
  parser.add_argument("-p", "--process", type=str, nargs=1, help="Path to a locally stored video to process")

  args = parser.parse_args()

  dest = args.destination or ["."]
  if args.video:
    download_video(args.video[0], dest[0])
  elif args.process:
    generate_animation(args.process[0], dest[0])
  else:
    print("Type -h or --help for help.")
