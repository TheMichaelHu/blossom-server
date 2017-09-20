from flask import Flask, render_template, request, jsonify
from models import Animation

app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello, World!'

@app.route('/animate/<url>')
def get_animation(url=None):
  if url:
    return jsonify({ "url": url })
  else:
    return "Please provide a url"

@app.route('/animate', methods=['GET', 'POST'])
def animate():
  if request.method == 'POST':
    if request.form:
      return submit_url(request.form['url'])
    return submit_url(request.url)
  else:
    return render_template('animate_form.html')

def submit_url(url):
  process_video(url)
  return render_template("animate_form_submitted.html", url=url)

# this is gonna be async probably...depends on how processing takes
def process_video(url):
  animation = Animation(url=url, data="test")
  animation_key = animation.put()
