from flask import Flask, redirect

app = Flask(__name__)


@app.route("/")
def hello_world():
    return (
        "If you're seeing this, I'm probably rebuilding the site. "
        "It should be back within seconds... "
    )


@app.route("/book/chapter_unit_test_first_view.html")
def redirect_03():
    return redirect("/book/chapter_03_unit_test_first_view.html", code=301)


@app.route("/book/chapter_philosophy_and_refactoring.html")
def redirect_04():
    return redirect("/book/chapter_04_philosophy_and_refactoring.html", code=301)


@app.route("/book/chapter_post_and_database.html")
def redirect_05():
    return redirect("/book/chapter_05_post_and_database.html", code=301)


@app.route("/book/chapter_explicit_waits_1.html")
def redirect_06():
    return redirect("/book/chapter_06_explicit_waits_1.html", code=301)


@app.route("/book/chapter_working_incrementally.html")
def redirect_07():
    return redirect("/book/chapter_07_working_incrementally.html", code=301)


@app.route("/book/chapter_prettification.html")
def redirect_08():
    return redirect("/book/chapter_08_prettification.html", code=301)


@app.route("/book/chapter_organising_test_files.html")
def redirect_12():
    return redirect("/book/chapter_12_organising_test_files.html", code=301)


@app.route("/book/chapter_database_layer_validation.html")
def redirect_13():
    return redirect("/book/chapter_13_database_layer_validation.html", code=301)


@app.route("/book/chapter_simple_form.html")
def redirect_14():
    return redirect("/book/chapter_14_simple_form.html", code=301)

@app.route("/book/chapter_advanced_forms.html")
def redirect_15():
    return redirect("/book/chapter_15_advanced_forms.html", code=301)

@app.route("/book/chapter_javascript.html")
def redirect_16():
    return redirect("/book/chapter_16_javascript.html", code=301)

@app.route("/book/chapter_deploying_validation.html")
def redirect_17():
    return redirect("/book/chapter_17_second_deploy.html", code=301)

@app.route("/book/chapter_spiking_custom_auth.html")
def redirect_18():
    return redirect("/book/chapter_18_spiking_custom_auth.html", code=301)

@app.route("/book/chapter_mocking.html")
def redirect_19():
    return redirect("/book/chapter_19_mocking.html", code=301)

"""
TODO?

chapter_CI.html
chapter_fixtures_and_wait_decorator.html
chapter_hot_lava.html
chapter_outside_in.html
chapter_page_pattern.html
chapter_prettification.html
chapter_purist_unit_tests.html
chapter_server_side_debugging.html
"""
