
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

"""
TODO
        new file:   output/book/chapter_09_docker.html
        new file:   output/book/chapter_10_production_readiness.html
        new file:   output/book/chapter_11_ansible.html
        renamed:    content/book/chapter_organising_test_files.html -> output/book/chapter_12_organising_test_files.html
        renamed:    content/book/chapter_database_layer_validation.html -> output/book/chapter_13_database_layer_validation.html
        renamed:    output/book/chapter_simple_form.html -> output/book/chapter_14_simple_form.html
        modified:   output/book/chapter_CI.html
        modified:   output/book/chapter_advanced_forms.html
        deleted:    output/book/chapter_automate_deployment_with_fabric.html
        deleted:    output/book/chapter_database_layer_validation.html
        modified:   output/book/chapter_deploying_validation.html
        modified:   output/book/chapter_fixtures_and_wait_decorator.html
        modified:   output/book/chapter_hot_lava.html
        modified:   output/book/chapter_javascript.html
        deleted:    output/book/chapter_making_deployment_production_ready.html
        deleted:    output/book/chapter_manual_deployment.html
        modified:   output/book/chapter_mocking.html
        deleted:    output/book/chapter_organising_test_files.html
"""