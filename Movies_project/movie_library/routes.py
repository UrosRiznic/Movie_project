import functools
import uuid
import datetime
import json
import requests
import pymongo
from dataclasses import asdict

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    session,
    url_for,
    request,
)
from movie_library.forms import LoginForm, RegisterForm, MovieForm, ExtendedMovieForm, QuizForm
from movie_library.models import User, Movie
from passlib.hash import pbkdf2_sha256


pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)

req = requests.get('https://opentdb.com/api.php?amount=11&category=11&type=boolean')
data = json.loads(req.content)
q1 = QuizForm(1, data["results"][0]["question"].replace("&#039;", "\'").replace("&quot;","\""), 1, data["results"][0]["correct_answer"] , data["results"][0]["incorrect_answers"][0])
q2 = QuizForm(2, data["results"][1]["question"].replace("&#039;", "\'").replace("&quot;","\""), 1, data["results"][0]["correct_answer"] , data["results"][0]["incorrect_answers"][0])
q3 = QuizForm(3, data["results"][2]["question"].replace("&#039;", "\'").replace("&quot;","\""), 1, data["results"][0]["correct_answer"] , data["results"][0]["incorrect_answers"][0])
q4 = QuizForm(4, data["results"][3]["question"].replace("&#039;", "\'").replace("&quot;","\""), 1, data["results"][0]["correct_answer"] , data["results"][0]["incorrect_answers"][0])
q5 = QuizForm(5, data["results"][4]["question"].replace("&#039;", "\'").replace("&quot;","\""), 1, data["results"][0]["correct_answer"] , data["results"][0]["incorrect_answers"][0])
q6 = QuizForm(6, data["results"][5]["question"].replace("&#039;", "\'").replace("&quot;","\""), 1, data["results"][0]["correct_answer"] , data["results"][0]["incorrect_answers"][0])
q7 = QuizForm(7, data["results"][6]["question"].replace("&#039;", "\'").replace("&quot;","\""), 1, data["results"][0]["correct_answer"] , data["results"][0]["incorrect_answers"][0])
q8 = QuizForm(8, data["results"][7]["question"].replace("&#039;", "\'").replace("&quot;","\""), 1, data["results"][0]["correct_answer"] , data["results"][0]["incorrect_answers"][0])
q9 = QuizForm(9, data["results"][8]["question"].replace("&#039;", "\'").replace("&quot;","\""), 1, data["results"][0]["correct_answer"] , data["results"][0]["incorrect_answers"][0])
q10 = QuizForm(10, data["results"][9]["question"].replace("&#039;", "\'").replace("&quot;","\""), 1, data["results"][0]["correct_answer"] , data["results"][0]["incorrect_answers"][0])
q11 = QuizForm(11, data["results"][10]["question"].replace("&#039;", "\'").replace("&quot;","\""), 1, data["results"][0]["correct_answer"] , data["results"][0]["incorrect_answers"][0])

question_list_easy = [q1, q2, q3]
question_list_medium = [q1, q2, q3, q4, q5]
question_list_hard = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]

def login_required(route):
    @functools.wraps(route)
    def route_wrapper(*args, **kwargs):
        if session.get("email") is None:
            return redirect(url_for(".login"))

        return route(*args, **kwargs)

    return route_wrapper


@pages.route("/")
@login_required
def index():
    user_data = current_app.db.user.find_one({"email": session["email"]})
    user = User(**user_data)

    movie_data = current_app.db.movie.find({"_id": {"$in": user.movies}})
    movies = [Movie(**movie) for movie in movie_data]

    return render_template(
        "index.html",
        title="Movies Watchlist",
        movies_data=movies,
    )


@pages.route("/register", methods=["POST", "GET"])
def register():
    if session.get("email"):
        return redirect(url_for(".index"))

    form = RegisterForm()

    if form.validate_on_submit():
        user = User(
            _id=uuid.uuid4().hex,
            email=form.email.data,
            password=pbkdf2_sha256.hash(form.password.data),
            resaults_easy=[1,2],
            resaults_medium=[1,2],
            resaults_hard=[1,2],
        )

        current_app.db.user.insert_one(asdict(user))

        flash("User registered successfully", "success")

        return redirect(url_for(".login"))

    return render_template(
        "register.html", title="Movies Watchlist - Register", form=form
    )

@pages.route("/quiz", methods=["GET","POST"])
def quiz():
    return render_template("quiz.html")

@pages.route("/yourscore", methods=["GET","POST"])
def yourscore():
    return render_template("yourscore.html")


@pages.route("/easy/", methods=["GET", "POST"])
def easy():
    session['score_easy'] = 0
    session['score_medium'] = 0
    session['score_hard'] = 0
    return render_template("easy.html")


@pages.route("/easy_quiz_test/<int:page>", methods=["GET", "POST"])
def easy_quiz_test(page):
    if request.method == "POST":
        if page+1 >= 3:
            selected_option = request.form.get('test1')
            if request.form.get('test1') != None:
                session['score_easy'] += 1
            flash(f"You have answered on {session['score_easy']} easy questions correctly!", category="success")
            return redirect(url_for("pages.yourscore"))
        else:
            selected_option = request.form.get('test1')
            if request.form.get('test1') != None:
                session['score_easy'] += 1
            page += 1
    return render_template("easy_quiz.html", question_list_easy=question_list_easy, page=page)
    
@pages.route("/medium/", methods=["GET", "POST"])
def medium():
    #session['score_medium'] = 0
    return render_template("medium.html")

@pages.route("/medium_quiz/<int:page>", methods=["GET", "POST"])
def medium_quiz(page):
    if request.method == "POST":
        if page+1 >= 5:
            selected_option = request.form.get('test1')
            if request.form.get('test1') != None:
                session['score_medium'] += 1
            flash(f"You have answered on {session['score_medium']} easy questions correctly!", category="success")
            return redirect(url_for("pages.yourscore"))
        else:
            selected_option = request.form.get('test1')
            if request.form.get('test1') != None:
                session['score_medium'] += 1
            page += 1
    return render_template("medium_quiz.html", question_list_medium=question_list_medium, page=page)

@pages.route("/hard/", methods=["GET", "POST"])
def hard():
    #session['score_hard'] = 0
    return render_template("hard.html")

@pages.route("/hard_quiz/<int:page>", methods=["GET", "POST"])
def hard_quiz(page):
    if request.method == "POST":
        if page+1 >= 10:
            question_id = question_list_hard[page].q_id
            selected_option = request.form.get('test1')
            if request.form.get('test1') != None:
                session['score_hard'] += 1
            flash(f"You have answered on {session['score_hard']} easy questions correctly!", category="success")
            return redirect(url_for("pages.yourscore"))
        else:
            question_id = question_list_hard[page].q_id
            selected_option = request.form.get('test1')
            if request.form.get('test1') != None:
                session['score_hard'] += 1
            page += 1
    return render_template("hard_quiz.html", question_list_hard=question_list_hard, page=page)


@pages.route("/login", methods=["GET", "POST"])
def login():
    if session.get("email"):
        return redirect(url_for(".index"))

    form = LoginForm()

    if form.validate_on_submit():
        user_data = current_app.db.user.find_one({"email": form.email.data})
        if not user_data:
            flash("Login credentials not correct", category="danger")
            return redirect(url_for(".login"))
        user = User(**user_data)

        if user and pbkdf2_sha256.verify(form.password.data, user.password):
            session["user_id"] = user._id
            session["email"] = user.email

            return redirect(url_for(".index"))

        flash("Login credentials not correct", category="danger")

    return render_template("login.html", title="Movies Watchlist - Login", form=form)

@pages.route("/logout")
def logout():
    current_theme = session.get("theme")
    session.clear()
    session["theme"] = current_theme
    return redirect(url_for(".login"))

@pages.route("/add", methods=["GET", "POST"])
@login_required
def add_movie():
    form = MovieForm()

    if form.validate_on_submit():
        movie = Movie(
            _id=uuid.uuid4().hex,
            title=form.title.data,
            director=form.director.data,
            year=form.year.data,
        )

        current_app.db.movie.insert_one(asdict(movie))

        current_app.db.user.update_one(
            {"_id": session["user_id"]}, {"$push": {"movies": movie._id}}
        )

        return redirect(url_for(".movie", _id=movie._id))

    return render_template(
        "new_movie.html", title="Movies Watchlist - Add Movie", form=form
    )


@pages.get("/movie/<string:_id>")
def movie(_id: str):
    movie = Movie(**current_app.db.movie.find_one({"_id": _id}))
    return render_template("movie_details.html", movie=movie)


@pages.route("/edit/<string:_id>", methods=["GET", "POST"])
@login_required
def edit_movie(_id: str):
    movie = Movie(**current_app.db.movie.find_one({"_id": _id}))
    form = ExtendedMovieForm(obj=movie)
    if form.validate_on_submit():
        movie.title = form.title.data
        movie.director = form.director.data
        movie.year = form.year.data
        movie.cast = form.cast.data
        movie.series = form.series.data
        movie.tags = form.tags.data
        movie.description = form.description.data
        movie.video_link = form.video_link.data

        current_app.db.movie.update_one({"_id": movie._id}, {"$set": asdict(movie)})
        return redirect(url_for(".movie", _id=movie._id))
    return render_template("movie_form.html", movie=movie, form=form)


@pages.get("/movie/<string:_id>/watch")
@login_required
def watch_today(_id):
    current_app.db.movie.update_one(
        {"_id": _id}, {"$set": {"last_watched": datetime.datetime.today()}}
    )

    return redirect(url_for(".movie", _id=_id))


@pages.get("/movie/<string:_id>/rate")
@login_required
def rate_movie(_id):
    rating = int(request.args.get("rating"))
    current_app.db.movie.update_one({"_id": _id}, {"$set": {"rating": rating}})

    return redirect(url_for(".movie", _id=_id))


@pages.get("/toggle-theme")
def toggle_theme():
    current_theme = session.get("theme")
    if current_theme == "dark":
        session["theme"] = "light"
    else:
        session["theme"] = "dark"

    return redirect(request.args.get("current_page"))
