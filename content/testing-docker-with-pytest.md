Title: Test-Driving a docker-based Postgres service using py.test
Date: 2014-07-20 10:39
Tags: Docker, py.test, integration tests
Author: Harry
Summary: <p>We've been experimenting with docker and py.test with integrated tests.  Is there any sense of writing unit tests here?</p>


We've been working on incorporating a Postgres database service into PythonAnywhere, and we decided to make it into a bit of a standalone project.  The shiny is that we're using docker to containerise postgres servers for our users, and while we were at it we thought we'd try a bit of a different approach to testing.  I'd be interested in feedback -- what do you like, what might you do differently?

## Context:  A docker-based postgres service

The objective is to build a service that, on demand, will spin up a docker container with postgres running on it, and listening on a particular port.  The service is going to be controlled by a web API.  We've got Flask to run the web service, docker-py to control containers, and ansible to provision servers.


## A single loop of integrated tests

Normally we use a "double-loop" TDD process, with an outside loop of functional tests that use selenium to interact with our web app, and an inner loop of more isolated unit tests.  For our development of the Postgres service, we still have the outer loop of functional tests -- selenium tests that log into the site via a browser, and test the service from the perspective of the user -- clicking through the right buttons on our UI and seeing if they can get a console that connects to a new postgres service.

But for the inner loop we were in a green field -- this wasn't going to be another app in our monolithic django project, we wanted it to be a standalone service, one that you could package up and use in another context.  It would provide all its services via an API, and need no knowledge of the rest of PythonAnywhere.  So how should we write the self-contained tests for this app?  Should it, in turn, have a double loop?  Relying on isolated unit tests only felt like a waste of time -- after all, the whole app was basically a thin wrapper that hooks up a web service to a series of docker commands.  All boundaries.  Isolated unit tests would end up being all mocks.  And from a TDD-process point of view, because we'd never actually used docker-py before, we didn't know its API, so we wouldn't know what mocks to write before we'd actually decided what the code was going to look like, and tried it out.  And trying it out would involve either running one of the PythonAnywhere FTs (super-slow, so a tediously and onerous feedback loop), or with manual tests, with all the uncertainty that implies.

So instead, it felt like starting with an intermeditate-level layer of integrated tests might be best: we've already got our top-level UI layer tests in the form of functional tests.  The next level down was the API level -- does calling this particular URL on the API actually give us a working container?

## An example test

    def test_create_starts_container_and_returns_port_with_postgres_connectable(docker_cleanup):
        response = post_to_api_create(port=6123)

        port = response.json()["port"]
        assert port == 6123

        connection = _get_db_connection(port)
        connection.close()

Where

    def post_to_api_create(port):
        response = requests.post(
            "https://localhost/api/containers/",
            {
                "admin_password": OUR_PASSWORD,
                "port": port,
            },
            verify=False,
            auth=(POSTGRES_API_USERNAME, POSTGRES_API_PASSWORD),
        )
        assert response.status_code == 200
        assert response.json()["status"] == "OK"
        return response

And

    def _get_db_connection(port, database='postgres'):
        return psycopg2.connect(
            database=database,
            user="pythonanywhere_helper",
            password=OUR_PASSWORD,
            host="localhost",
            port=port,
        )

So you can see that's a very integration-ey, end-to-end test -- it does a real POST request, to a place where it expects to see an actual webapp running, and it expectes to see a real, connectable database spun up and ready for it.

(it also tests another thing, which is, whether the api returns the same port it was given.  that's a little naughty, but by-the-bye)

Now this test runs in about 10 seconds - not super-fast, like the milliseconds you might want a unit test to run in, but much faster than our FT, which takes 5 or 6 minutes. And, meanwhile, we can actually write this test first. To write an isolated, mocky test, we'd need to know the docker-py API already, and be sure that it was going to work, which we weren't.


## py.test observations

One Py.test selling point is "less boilerplate". Notice that none of these tests are methods in a class, and there's no self variable.  On top of that, we ust use `assert` keywords, no complicated remembering of `self.assertIn`, `self.assertIsNotNone`,  and so on.

### py.test fixtures

Another thing you may be interested in is the `docker_cleanup` argument to the test.  py.test will magically look for a special fixture function named the same as that argument, and use it in the test.  Here's how it looks:

    from docker import Client
    docker = Client(base_url='unix://var/run/docker.sock')

    @pytest.fixture()
    def docker_cleanup(request):
        all_containers_before = docker.containers(all=True)

        def kill_new_containers():
            for container in docker.containers(all=True):
                if container not in all_containers_before:
                    docker.remove_container(container, force=True)

        def identify_new_container():
            return next(
                c for c in docker.containers() if c not in all_containers_before
            )

        request.addfinalizer(kill_new_containers)

        helper = FixtureHelper()
        helper.identify_new_container = identify_new_container
        helper.kill_new_containers = kill_new_containers
        return helper

    class FixtureHelper(object):
        pass

The fixture function has a couple of jobs:

* it adds a "finalizer" (the equivalent of unittest `addCleanup` or `tearDown`) which will run at the end of the tests, to kill any containers that have been started by the test
* it provides that same finalizer, and a helper method to identify new containers, to the tests that use the fixture, as a helper tool (I haven't showed any examples of that here though)

I've found it to be an interesting model for cleanup and teardown.

Incidentally, until I started using py.test I'd always associated "fixtures" with Django "fixtures", which basically meant serialized versions of model data, but really py.test is using the word in a more correct usage of the term, to mean "state that the world has to be in for the test to run properly".


# A peek at the implementation, for the curious



