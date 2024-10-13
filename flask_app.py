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


@app.route("/book/chapter_fixtures_and_wait_decorator.html")
def redirect_20():
    return redirect("/book/chapter_20_fixtures_and_wait_decorator.html", code=301)


@app.route("/book/chapter_server_side_debugging.html")
def redirect_21():
    return redirect("/book/chapter_21_server_side_debugging.html", code=301)


@app.route("/book/chapter_outside_in.html")
def redirect_22():
    return redirect("/book/chapter_22_outside_in.html", code=301)


@app.route("/book/chapter_CI.html")
def redirect_23():
    return redirect("/book/chapter_23_CI.html", code=301)


@app.route("/book/chapter_page_pattern.html")
def redirect_24():
    return redirect("/book/chapter_24_page_pattern.html", code=301)


@app.route("/book/chapter_purist_unit_tests.html")
def redirect_25():
    return redirect("/book/appendix_purist_unit_tests.html", code=301)


# 2 big chapter splits 2024-10-13
@app.route("/book/chapter_11_ansible.html")
def redirect26():
    return redirect("/book/chapter_12_ansible.html", code=301)


@app.route("/book/chapter_12_organising_test_files.html")
def redirect27():
    return redirect("/book/chapter_13_organising_test_files.html", code=301)


@app.route("/book/chapter_13_database_layer_validation.html")
def redirect28():
    return redirect("/book/chapter_14_database_layer_validation.html", code=301)


@app.route("/book/chapter_14_simple_form.html")
def redirect29():
    return redirect("/book/chapter_15_simple_form.html", code=301)


@app.route("/book/chapter_15_advanced_forms.html")
def redirect30():
    return redirect("/book/chapter_16_advanced_forms.html", code=301)


@app.route("/book/chapter_16_javascript.html")
def redirect31():
    return redirect("/book/chapter_17_javascript.html", code=301)


@app.route("/book/chapter_17_second_deploy.html")
def redirect32():
    return redirect("/book/chapter_18_second_deploy.html", code=301)


@app.route("/book/chapter_18_spiking_custom_auth.html")
def redirect33():
    return redirect("/book/chapter_19_spiking_custom_auth.html", code=301)


@app.route("/book/chapter_19_mocking.html")
def redirect34():
    return redirect("/book/chapter_20_mocking_1.html", code=301)


@app.route("/book/chapter_20_fixtures_and_wait_decorator.html")
def redirect36():
    return redirect("/book/chapter_22_fixtures_and_wait_decorator.html", code=301)


@app.route("/book/chapter_21_server_side_debugging.html")
def redirect37():
    return redirect("/book/chapter_23_debugging_prod.html", code=301)


@app.route("/book/chapter_22_outside_in.html")
def redirect38():
    return redirect("/book/chapter_24_outside_in.html", code=301)


@app.route("/book/chapter_23_CI.html")
def redirect39():
    return redirect("/book/chapter_25_CI.html", code=301)


@app.route("/book/chapter_24_page_pattern.html")
def redirect40():
    return redirect("/book/chapter_26_page_pattern.html", code=301)


@app.route("/book/chapter_25_hot_lava.html")
def redirect41():
    return redirect("/book/chapter_27_hot_lava.html", code=301)


"""
TODO  (old urls/chapters as yet not renamed)

chapter_hot_lava.html
"""
