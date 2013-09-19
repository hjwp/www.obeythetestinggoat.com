Title: Unit testing fabric scripts for deployment
Date: 2013-09-19 07:30
Tags: unit tests, fabric, deployment, mocking
Slug: unit-testing-fabric-deployment-scripts
Author: Harry
Status: published
Summary: <p>Should we unit test deployment scripts? If so, how?</p>

In chapter 8 of my [book](http://www.obeythetestinggoat.com/pages/book.html) I introduce a fabric script as a way of automating the deployment of our example app.  You can see the section where I do so [here](http://chimera.labs.oreilly.com/books/1234000000754/ch08.html#_automating_deployment_with_fabric).

After 7 chapters of building everything step-by-step with TDD and detailed unit tests, this fairly large script leaps out fully-formed, It prompted one of my readers to write in (Thanks Nick):

> It didn't work the first time I used it (I retype, rather than copy-paste, to better understand the code. Occasional typos are inevitable, and unit testing is a great way to catch these small errors). With the rest of the project, there was substantial testing that went into the creation of each source file, meaning small errors were swiftly located and corrected. However, running the fabfile often caused errors in code that wasn't tested, which took me much longer to find a fix.

> There should be a way to test the deployment script as thoroughly as the rest of the project code. Especially considering how critical deployment is to a web app, and how often it will likely need to be done, maintaining error-free consistency in this process seems like a critical part of the workflow, and worth writing tests for.

Nick is right isn't he? There's a bit of a disjoint here. Surely we need some kind of testing for our deployment scripts? 

Admittedly in this chapter I'm explaining how to run Selenium tests against a staging site to make sure that our deployment procedure works, so our deployment script *is* tested indirectly, but everywhere else in the book I've *also* written unit tests for all my code.

At PythonAnywhere, we decided not to write tests for our fabric scripts, and we now regret it.  There's about 3000 lines of messy code in there, which we're scared of refactoring.

But how to write some kind of low-level tests for a fabric script? Here's a sample function:


    :::python
    def _update_virtualenv(source_folder):
        virtualenv_folder = path.join(source_folder, '../virtualenv')
        if not exists(path.join(virtualenv_folder, 'bin', 'pip')): #<11>
            run('virtualenv --python=python3.3 %s' % (virtualenv_folder,))
        run('%s/bin/pip install -r %s/requirements.txt' % (
                virtualenv_folder, source_folder
        ))

It seems to me there's no great ways of testing this sort of stuff?  Here's three I can think of:

### 1. Mock out Fabric

You could mock out the Fabric API, and write a bunch of tests that say things like:

    :::python
    self.assertEqual(
        mock_run.method_calls,
        [
            call('virtualenv --python=python3.3 /path/to/virtualenv'),
            call('/path/to/virtualenv/bin/pip install -r /path/to/my/folder/requirements.txt'),
        ]
    )

But I hate that kind of unit test!  It's just duplicating your code with a bunch of mocks.  It's not that it has *no* value -- it's a bit like double-entry accounting, so it might help Nick or I catch the occasional typo -- but it doesn't really feel like testing, you know?  It's so tightly coupled to the implementation as to be almost identical, and we'd definitely be testing implementation rather than behaviour.

I mean, would you really test-drive writing your fabric scripts using these kinds of tests?


### 2. Monkeypatch fabric to work in /tmp

You could write a sort of hacked-up integration test, which redirects all the fabric calls to a temp folder on the machine you're using for testing, something like this:

    :::python
    # assumes we have some recognisable prefix for path given
    def mock_run(cmd_given):
        cmd_redirected = cmd_given.replace(
            path_prefix, tmp_path + path_prefix
        )
        # use fabric local() function to run command locally instead
        local(cmd_redirected)
    #...
    self.assertTrue(os.path.exists(
        tmp_path + given_path + '../virtualenv'
    ))

So we can check the effects of that function on the temp folder - more of an integration test than a unit test, but at least we're now testing behaviour rather than testing the implementation.  But it'll involve a lot of logic to correctly mock out the fabric API... `run` may not be too hard, but I'm also using `append` and `sed`...  I'm worried I'll spend as much time debuggin test code as the real code!


### 3. Run the actual commands against a test VM

You could spin up some kind of lightweight VM / linux container (docker?) and let the fabric script run against that, checking the effects using fabric too.

That might be kinda cool, but it definitely feels very heavyweight -- it's certainly more than I want to tell my readers to set up on their machines (what about Windows users!), and it ends up being a lot like what I'm doing with Selenium, running the acceptance tests against the staging server...

--------------------------

So what to do? One possibility would be to consign all this stuff to an appendix, in which I demonstrate all three approaches, and then tell the reader that it's up to them to choose which they like... But can I do better? And should I even bother?

So folks, what do you think?  Is it worth writing unit tests for fabric scripts?  If so, how?

