# blossom-server
Flask server for producing commands for blossom

# video to json script
The server and script are currently separated (script is in `./process_vid/`). The script uses a python library to download a video from youtube, and opencv to go through the video frame by frame.

## downloading a video
To download a video off youtube, run
```
python process_vid/make_animation.py -v [video url] -d [destination]
```
The destination is optional and defaults to your current directory

## processing a video
To process a video that's been downloaded into a json file, run
```
python process_vid/make_animation.py -p [video] -d [destination]
```
The destination is optional and defaults to your current directory

# server setup (*Note, just ignore the server stuff for how.*)
- Set up Google App Engine, first few steps of [this](https://cloud.google.com/appengine/docs/standard/python/getting-started/python-standard-env#test_the_application)
- Make sure running `python --version` gets 2.7.x, not 3.6 or something
- Install dependencies with `pip install -t lib -r requirements.txt`
- Start the server locally with `dev_appserver.py app.yaml`

# deploy to google app engine
Just run `gcloud app deploy`

# layout
So far there is a form `/animate` that takes a url and submits to the same url but as a POST. Once the video is processed, it'll be made available at `/animate/[url]`
