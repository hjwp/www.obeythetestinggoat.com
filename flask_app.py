
from flask import Flask, redirect

app = Flask(__name__)


@app.route('/')
def hello_world():
    return (
        "If you're seeing this, I'm probably rebuilding the site. "
        "It should be back within seconds... "
    )


REDIRECTS = {
    'appendix_II_Django_Class-Based_Views.html': 'appendix_Django_Class-Based_Views.html',
    'appendix_VII_DjangoRestFramework.html': 'appendix_DjangoRestFramework.html',
    'appendix_VI_rest_api.html': 'appendix_rest_api.html',
    'appendix_V_bdd_tools.html': 'appendix_bdd.html',
    'chapter_02.html': 'chapter_02_unittest.html',
    'chapter_03.html': 'chapter_unit_test_first_view.html',
    'chapter_04.html': 'chapter_philosophy_and_refactoring.html',
    'chapter_05.html': 'chapter_post_and_database.html',
    'chapter_06.html': 'chapter_explicit_waits_1.html',
    'chapter_07.html': 'chapter_working_incrementally.html',
    'chapter_08.html': 'chapter_prettification.html',
    'chapter_09.html': 'chapter_manual_deployment.html',
    'chapter_10.html': 'chapter_automate_deployment_with_fabric.html',
    'chapter_11.html': 'chapter_database_layer_validation.html',
    'chapter_12.html': 'chapter_simple_form.html',
    'chapter_13.html': 'chapter_advanced_forms.html',
    'chapter_14.html': 'chapter_javascript.html',
    'chapter_15.html': 'chapter_deploying_validation.html',
    'chapter_16.html': 'chapter_spiking_custom_auth.html',
    'chapter_17.html': 'chapter_mocking.html',
    'chapter_18.html': 'chapter_server_side_debugging.html',
    'chapter_19.html': 'chapter_outside_in.html',
    'chapter_20.html': 'chapter_purist_unit_tests.html',
    'chapter_21.html': 'chapter_CI.html',
    'chapter_22.html': 'chapter_page_pattern.html',
    'chapter_23.html': 'chapter_hot_lava.html',
}


@app.route('/book/chapter_<n>.html')
def chapter_redirector(n):
    old_name = 'chapter_{n}.html'.format(n=n)
    return redirect('/book/' + REDIRECTS[old_name])


@app.route('/book/appendix_<thing>.html')
def appendix_redirector(thing):
    old_name = 'appendix_{thing}.html'.format(thing=thing)
    return redirect('/book/' + REDIRECTS[old_name])

