
from flask import Flask, redirect

app = Flask(__name__)


@app.route('/')
def hello_world():
    return (
        "If you're seeing this, I'm probably rebuilding the site. "
        "It should be back within seconds... "
    )



@app.route("/book/chapter_unit_test_first_view.html")
def redirect_1():
    return redirect("/book/chapter_03_unit_test_first_view.html", code=301)

@app.route("/book/chapter_philosophy_and_refactoring.html")
def redirect_2():
    return redirect("/book/chapter_04_philosophy_and_refactoring.html", code=301)

@app.route("/book/chapter_post_and_database.html")
def redirect_3():
    return redirect("/book/chapter_05_post_and_database.html", code=301)

@app.route("/book/chapter_explicit_waits_1.html")
def redirect_4():
    return redirect("/book/chapter_06_explicit_waits_1.html", code=301)

@app.route("/book/chapter_working_incrementally.html")
def redirect_5():
    return redirect("/book/chapter_07_working_incrementally.html", code=301)

@app.route("/book/chapter_prettification.html")
def redirect_6():
    return redirect("/book/chapter_08_prettification.html", code=301)
