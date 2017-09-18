# blossom-server
Flask server for producing commands for blossom

# setup
- Set up Google App Engine, first few steps of (this)[https://cloud.google.com/appengine/docs/standard/python/getting-started/python-standard-env#test_the_application]
- Make sure running `python --version` gets 2.7.x, not 3.6 or something
- Install dependencies with `pip install -t lib -r requirements.txt`
- Start the server locally with `dev_appserver.py app.yaml`

# deploy to google app engine
Just run `gcloud app deploy`

# layout
So far there is a form `/animate` that takes a url and submits to the same url but as a POST. Once the video is processed, it'll be made available at `/animate/[url]`
