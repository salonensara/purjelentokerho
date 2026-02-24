import sqlite3
import secrets
import markupsafe
from datetime import datetime

from flask import Flask
from flask import Response
from flask import flash, abort, redirect, render_template, request, session

import config
import items
import users

app = Flask(__name__)
app.secret_key = config.secret_key

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/")
def index():
    all_items = items.get_items()
    return render_template("index.html", items=all_items)

@app.route("/create_reservation", methods=["POST"])
def create_reservation():
    require_login()
    check_csrf()

    user_id = session["user_id"]
    item_id = request.form["item_id"]
    if not item_id:
        abort(403)
    info = request.form["info"]
    if not info or len(info) > 1000:
        abort(403)
    begin_date = request.form.get("begin_date")
    begin_date = datetime.strptime(begin_date, "%Y-%m-%d").date()
    begin_date = begin_date.strftime("%d.%m.%Y")
    end_date = request.form.get("end_date")
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    end_date = end_date.strftime("%d.%m.%Y")
    print(f"testi: {begin_date} ja {type(begin_date)}")
    items.add_reservation(item_id, begin_date, end_date, info, user_id)

    return redirect("/item/"+str(item_id))

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    items = users.get_items(user_id)
    return render_template("show_user.html", user=user, items=items)

@app.route("/search_item")
def search_item():
    query = request.args.get("query")
    if query:
        results = items.search_items(query)
    else:
        query = ""
        results = []
    return render_template("search_item.html", query=query, results=results)

@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    reservations = items.get_reservations(item_id)
    return render_template("show_item.html", item=item, reservations=reservations)

@app.route("/image/<int:item_id>")
def show_image(item_id):
    item = items.get_item(item_id)
    if item and item["image"]:
        return Response(item["image"], mimetype="image")
    abort(404)

@app.route("/new_item")
def new_item():
    require_login()
    return render_template("new_item.html")

@app.route("/create_item", methods=["POST"])
def create_item():
    require_login()
    check_csrf()

    glider_type = request.form["glider_type"]
    if not glider_type or len(glider_type) > 20:
        abort(403)
    callsign = request.form["callsign"]
    if not callsign or len(callsign) > 10:
        abort(403)
    compsign = request.form["compsign"]
    if not compsign or len(compsign) > 5:
        abort(403)
    glider_class = request.form["glider_class"]
    options = request.form["options"]
    user_id = session["user_id"]
    image = None
    file = request.files["image"]
    if file:
        if not file.filename.endswith((".jpg", ".png")):
            return "VIRHE: väärä tiedostomuoto"

        image = file.read()
        if len(image) > 100*1024:
            return "VIRHE: liian suuri kuva"
        
    items.add_item(glider_type, callsign, compsign, glider_class, options, image, user_id)

    return redirect("/")

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()

    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_item.html", item=item)

@app.route("/update_item", methods=["POST"])
def update_item():
    check_csrf()
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    glider_type = request.form["glider_type"]
    if not glider_type or len(glider_type) > 50:
        abort(403)
    callsign = request.form["callsign"]
    if not callsign or len(callsign) > 10:
        abort(403)
    compsign = request.form["compsign"]
    if len(compsign) > 5:
        abort(403)
    glider_class = request.form["glider_class"]
    options = request.form["options"]
    file = request.files["image"]
    if file:
        if not file.filename.endswith((".jpg", ".png")):
            return "VIRHE: väärä tiedostomuoto"

        image = file.read()
        if len(image) > 100*1024:
            return "VIRHE: liian suuri kuva"
    else:
        image = items.get_item(item_id)["image"]

    items.update_item(item_id, glider_type, callsign, compsign, glider_class, options, image)

    return redirect("/item/" + str(item_id))

@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    require_login()

    item = items.get_item(item_id)
    if not item:
        abort(404)

    if item["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_item.html", item=item)

    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        return redirect("/item/" + str(item_id))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    if not username or len(username) > 10:
        abort(403)
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        flash("VIRHE: Salasanat eivät täsmää!", "error")
        return render_template("register.html")
    if not password1 or len(password1) > 20:
        abort(403)
    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("VIRHE: Tunnus on jo varattu!", "error")
        return render_template("register.html")

    flash("JIPPII! Tunnus luotu onnistuneesti!", "success")
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])

def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")

        flash("VIRHE: Väärä tunnus tai salasana!", "error")
        return render_template("login.html")

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")
