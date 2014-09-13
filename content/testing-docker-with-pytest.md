Title: Test-Driving a docker-based Postgres service using py.test
Date: 2014-09-11 16:59
Tags: Docker, py.test, integrated tests, integration tests
Author: Harry
Summary: <p>We've been experimenting with Docker and py.test with integrated tests.  Is there any sense of writing unit tests here?</p>

*[Cross-posted on the [PythonAnywhere blog](https://blog.pythonanywhere.com/97/)]*

We've been working on incorporating a Postgres database service into PythonAnywhere, and we decided to make it into a bit of a standalone project.  The shiny is that we're using Docker to containerise Postgres servers for our users, and while we were at it we thought we'd try a bit of a different approach to testing.  I'd be interested in feedback -- what do you like, what might you do differently?

## Context:  A Docker-based Postgres service

The objective is to build a service that, on demand, will spin up a Docker container with Postgres running on it, and listening on a particular port.  The service is going to be controlled by a web API.  We've got Flask to run the web service, docker-py to control containers, and Ansible to provision servers.


## A single loop of integrated tests

Normally we use a "double-loop" TDD process, with an outside loop of functional tests that use selenium to interact with our web app, and an inner loop of more isolated unit tests.  For our development of the Postgres service, we still have the outer loop of functional tests -- selenium tests that log into the site via a browser, and test the service from the perspective of the user -- clicking through the right buttons on our UI and seeing if they can get a console that connects to a new Postgres service.

But for the inner loop we were in a green field -- this wasn't going to be another app in our monolithic Django project, we wanted it to be a standalone service, one that you could package up and use in another context.  It would provide all its services via an API, and need no knowledge of the rest of PythonAnywhere.  So how should we write the self-contained tests for this app?  Should it, in turn, have a double loop?  Relying on isolated unit tests only felt like a waste of time -- after all, the whole app was basically a thin wrapper that hooks up a web service to a series of Docker commands.  All boundaries.  Isolated unit tests would end up being all mocks.  And from a TDD-process point of view, because we'd never actually used docker-py before, we didn't know its API, so we wouldn't know what mocks to write before we'd actually decided what the code was going to look like, and tried it out.  And trying it out would involve either running one of the PythonAnywhere FTs (super-slow, so a tediously and onerous feedback loop), or with manual tests, with all the uncertainty that implies.

So instead, it felt like starting with an intermediate-level layer of integrated tests might be best: we've already got our top-level UI layer full-stack tests in the form of functional tests.  The next level down was the API level -- does calling this particular URL on the API *actually* give us a working container?

## An example test

```python
def test_create_starts_container_with_postgres_connectable(docker_cleanup):
    response = post_to_api_create()

    port = response.json()["port"]
    assert port > 1024

    connection = psycopg2.connect(
        database="postgres",
        user="pythonanywhere_helper", password="papwd",
        host="localhost", port=port,
    )
    connection.close()
```

Where

```python
def post_to_api_create():
    response = requests.post(
        "http://localhost:5000/api/create",
        {"admin_password": "papwd"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "OK"
    return response
```


So you can see that's a very integration-ey, end-to-end test -- it does a real POST request, to a place where it expects to see an actual webapp running, and it expects to see a real, connectable database spun up and ready for it.

Now this test runs in about 10 seconds - not super-fast, like the milliseconds you might want a unit test to run in, but much faster than our FT, which takes 5 or 6 minutes. And, meanwhile, we can actually write this test first. To write an isolated, mocky test, we'd need to know the docker-py API already, and be sure that it was going to work, which we weren't.

To illustrate this point, take a look at the difference between an early implementation and a later one:


### A first implementation

```python
USER_IMAGE_DOCKERFILE = '''
FROM postgres
USER postgres
RUN /etc/init.d/postgresql start && \\
    psql -c "CREATE USER pythonanywhere_helper WITH SUPERUSER PASSWORD '{hashed}';"
CMD ["/usr/lib/postgresql/9.3/bin/postgres", "-D", "/var/lib/postgresql/9.3/main", "-c", "config_file=/etc/postgresql/9.3/main/postgresql.conf"]
'''

def get_user_dockerfile(admin_password):
    hashed = 'md5' + md5(admin_password + 'pythonanywhere_helper').hexdigest()
    return USER_IMAGE_DOCKERFILE.format(
        hashed=hashed,
    )

def create_container_with_password(password):
    tempdir = tempfile.mkdtemp()
    with open(os.path.join(tempdir, 'Dockerfile'), 'w') as f:
        f.write(get_user_dockerfile(password))

    response = docker.build(path=tempdir)
    response_lines = list(response)

    image_finder = r'Successfully built ([0-9a-f]+)'
    match = re.search(image_finder, response_lines[-1])
    if match:
        image_id = match.group(1)
    else:
        raise Exception('Image failed to build:\n{}'.format(
            '\n'.join(response_lines)
        ))

    container = docker.create_container(
        image=image_id,
    )
    return container
```

(These are some library functions we wrote, I won't show you the trivial flask app that calls them).

This was one of our first attempts -- we needed to be able to customise the Postgres superuser password for each user, and our initial solution involved building a new image for each user, by generating and running a custom Dockerfile for them.

We were never quite sure whether the Dockerfile voodoo was going to work, and we weren't really Postgres experts either, so having the high-level integration test, which actually tried to spin up a container and connect to the Postgres database that should be running inside it, was a really good way of getting to a solution that worked.

Imagine what a more isolated test for this code might look like:

```python
@patch('containers.docker')
def test_uses_dockerfile_to_build_new_image(mock_docker):
    expected_dockerfile = USER_IMAGE_DOCKERFILE.format(
        'md5sekritpythonanywhere_helper'
    ).hexdigest()
    def check_dockerfile_contents(path):
        with open(os.path.join(path, 'Dockerfile')) as f:
            assert f.read() == expected_dockerfile

    mock_docker.build.side_effect = check_dockerfile_contents

    create_container_with_password('sekrit')

    assert mock_docker.build.called is True

 @patch('containers.docker')
def test_creates_container_from_docker_image(mock_docker):
    create_container_with_password('sekrit')
    mock_docker.create_container.assert_called_once_with(
        mock_docker.build.return_value
    )
```



There's no way we could have written that test until we actually had a working solution.  And, on top of that, the test would have been totally useless when it came to evolving our requirements and our solution

### A later implementation -- but minimal change to the main test

To give you an idea, here's what our current implementation looks like:

```python
def start_new_container(storage_dirname, password, requested_port):
    prep_storage_dir(storage_dirname)
    run_command_on_temporary_container_with_mounts(
        command=['chown', '-R', 'postgres:postgres', POSTGRES_DIR],
        storage_dirname=storage_dirname,
        user='root',
    )
    run_command_on_temporary_container_with_mounts(
        command=[
            'bash', '-c', 
            INITIALISE_POSTGRES_AND_SET_PASSWORD.format(password)
        ],
        storage_dirname=storage_dirname
    )
    user_container = create_postgres_container(name=storage_dirname)
    start_container_with_storage(
        user_container, storage_dirname, 
        ports={POSTGRES_PORT: requested_port},
    )
    with open(port_file_path(storage_dirname), 'w') as f:
        f.write(str(requested_port))
    return requested_port
```

I won't bore you with the details of `run_command_on_temporary_container_with_mounts`, but one way or another we realised that building separate images for each user wasn't going to work, and that instead we were going to want to have some permanent storage mounted in from outside of Docker, which would contain the Postgres data directory, and which would effectively "save" customisations like the user's password.

So a radically different implementation, but look how little the main test changed:

```python
def post_to_api_create(storage_dir=None, port=None):
    if storage_dir is None:
        storage_dir = uuid.uuid4()
    if port is None:
        port = random.randint(6000, 9999)
    response = requests.post(
        "https://localhost/api/containers/",
        {
            "storage_dir": storage_dir,
            "admin_password": OUR_PASSWORD,
            "port": port,
        },
        verify=False,
    )
    return response

def test_create_starts_container_with_postgres_connectable(docker_cleanup):
    response = post_to_api_create(port=6123)
    # rest of test as before!
```


And now imagine all the time we'd have had to spend rewriting mocks, if we'd decided to have isolated tests as well.


## Aside: py.test observations

One py.test selling point is "less boilerplate". Notice that none of these tests are methods in a class, and there's no self variable.  On top of that, we just use `assert` keywords, no complicated remembering of `self.assertIn`, `self.assertIsNotNone`,  and so on.  Absolutely loving that.


### py.test fixtures

Another thing you may be interested in is the `docker_cleanup` argument to the test.  py.test will magically look for a special fixture function named the same as that argument, and use it in the test.  Here's how it looks:


```python
from docker import Client
docker = Client(base_url='unix://var/run/docker.sock')

@pytest.fixture()
def docker_cleanup(request):
    containers_before = docker.containers()

    def kill_new_containers():
        current_containers = docker.containers()
        for container in current_containers:
            if container not in containers_before:
                print('killing {}'.format(container['Names'][0]))
                docker.kill(container)

    request.addfinalizer(kill_new_containers)
    return kill_new_containers
```

The fixture function has a couple of jobs:

* It adds a "finalizer" (the equivalent of unittest `addCleanup` or `tearDown`) which will run at the end of the tests, to kill any containers that have been started by the test

* It provides that same finalizer, and a helper method to identify new containers, to the tests that use the fixture, as a helper tool (I haven't showed any examples of that here though)

As it's illustrated here, there are no obvious advantages over the unittest `setUp/tearDown` ideas, although you can see it would make it a little easier to share setup and cleanup code between tests in different files and tests.  There's a lot more to them, and if you really want to get #mindblown, go checkout out [pytest yield fixtures](http://pytest.org/latest/yieldfixture.html)

Incidentally, until I started using py.test I'd always associated "fixtures" with Django "fixtures", which basically meant serialized versions of model data, but really py.test is using the word in a more correct usage of the term, to mean "state that the world has to be in for the test to run properly".



# The pros & cons of the "integrated-tests-only" workflow

#### Pros:

* Allowed us to experiment freely with an API that was new to us, and get feedback on whether it was *really* working
* Allowed us to refactor code freely, extracting helper functions etc, without needing to rewrite mocky unit tests

#### Cons:

* Being end-to-end tests, they ran much slower than unit tests would - on the order of seconds, and later, a minute or two, once we grew from three or four tests to a dozen or two. And, on top of that...

* Being integrated tests, they're not designed to run on a development machine. Instead, each code change means pushing updated source up to the server using Ansible, restarting the control webapp, and then re-running the tests in an SSH session.

* Because the tests call across a web API, the code being tested runs in a different process to he test code, meaning tracebacks aren't integrated into your test results.  Instead, you have to tail a logfile, and make sure you have logging set up appropriately.


## Conclusions and next steps

I can potentially imagine a time when we might start to see value in a layer of "real" unit tests... So far though, there's really no "business logic" that we could extract and write fast unit tests for. Or at least, there's no business logic that I identify as such, and I'd be very pleased for someone to come along and school me about it?

On the other hand, I can definitely see a time where we might want to split out our tests for the web API from the tests for the Postgres and Docker stuff, and I can see value in a setup where a developer can run these tests locally rather than having to push code up to a dev box.  Vagrant and VirtualBox might be one solution, but, honestly, installing Docker and Postgres on a dev box doesn't feel that onerous either, as long as we know we'll be testing on a "real" box in CI. Or at least, it doesn't feel onerous until we start talking about my poor laptop with its paltry 120GB SSD.  No room here!

And the bonus of being able to see honest-to-God tracebacks in your test run output feels like it might be worth it.

But, overall, at this stage in development, given the almost total lack of "business logic" in our app, and given the fact that we were working with a new API and a new set of technologies -- I've found that doing without "real" unit tests has actually worked very well.

