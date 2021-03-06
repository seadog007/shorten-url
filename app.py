from flask import Flask, render_template, request
from flask_cors import CORS
from os import system, popen
from flask_recaptcha import ReCaptcha
from models import *
from string import ascii_letters, digits


app = Flask(__name__)
CORS(app)

public_key = "6Lc7UMUUAAAAAEVWlNxm5SNF7kaiixUZAVBoyNVc"
private_key = "6Lc7UMUUAAAAALl0APCC9dCjzKKOz0Cgys1K91q1"
app.config.update(dict(
    RECAPTCHA_ENABLED = True,
    RECAPTCHA_SITE_KEY = public_key,
    RECAPTCHA_SECRET_KEY = private_key,
))

recaptcha = ReCaptcha()
recaptcha.init_app(app)

allow = ascii_letters + digits + '_-\\'


@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', path = '')
    elif request.method == 'POST':
        if recaptcha.verify():
            url = request.form.get('url')
            new_url = request.form.get('new-url')

            if not (all(ch in allow for ch in new_url) and new_url != ""):
                return render_template("char-forbidden.html")
            if new_url in ["new", "old", "who", "id"]:
                return render_template("string-forbidden.html")

            trans(request.remote_addr, url, new_url)

            return "<script>alert('https://cnmc.tw/%s')</script>"%new_url
        else:
            return render_template("verify-error.html")


@app.errorhandler(404)
def redirect(e):
    try:
        page = get_page(request.path)
    except:
        return render_template("404.html")
    else:
        model = "window.location.replace('url')"
        out = model.replace('url', page)
        out = "<script>%s</script>"%out
        return out


if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 8080, debug = True)
