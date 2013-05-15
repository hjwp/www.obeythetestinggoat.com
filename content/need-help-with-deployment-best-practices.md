Title: What to say about deployment?
Date: 2013-05-15 7:37
Tags: deploy, django, production, heroku, fabric, staging
Author: Harry
Summary: Time to deploy the site... But how?  And where does TDD fit in?

My book has got to the stage of a minimum viable site.  I want the next chapter
to be about actually deploying the site, even though it's ridiculously early --
to encourage the habit of "deploy early, deploy often".

But how to introduce deployment in a beginner-friendly way?  It's a very simple
site, so we don't need to cover all the complexities of deployment, but what's 
the minimum? Here's what I've got so far..

------

Deploying a site to a live web server can be a tricky topic.  Oft heard in 
office corridors, IRC and tech forums is the forlorn cry -- *"but it works on my machine"*

Some of the danger areas of deployment include:

- **static files** (CSS, javascript, images etc): web servers usually need special
  configuration for serving these
- the **database**: there can be permissions and path issues, and we need to be
  careful about preserving data between deploys
- **dependencies**: we need to make sure that the packages are software relies on
  are installed on the server, and have the correct versions

But there are solutions to all of these.  In order:

- Using a **staging site**, on the same infrastructure as the production site, can
  help us test out our deployments and get things right before we go to the
  "real" site
- We can also **run our functional tests against the staging site**. They could
  include some smoke tests that, eg, CSS is loaded correctly.
- We can write a special functional **test that checks the deploy process**, for
  example making sure database data is preserved (later, we can talk about South 
  + data migrations...)
- **Virtualenvs** are a useful tool for managing packages and dependencies on a
  server that's not entirely under your own control
- And finally, automation, automation, automation.  By using an **automated
  script** to deploy new versions, and by using the same script to deploy to
  staging and production, we can reassure ourselves that staging is as much
  like live as possible.

------

So far, so good (at least, I think.  feel free to pick holes!)

But the question is: now what?  What platform to choose to deploy to?  What
should be in my automated deploy script?

Platform:

- Obviousy I think [PythonAnywhere](http://www.pythonanywhere.com) is the
  natural choice and the easiest and the best and stuff. But I would say that.
  So I can't say that
- Heroku / Dotcloud et al are an option, but they involve quite a lot of
  specific config.  The precise tools used to deploy are all different, and
  might change by the time the book comes out
- How about "a generic VPS"?  Assuming the user has SSH access, I could use
  fabric to deploy...  That would let people use AWS, Digital Ocean, Linode or
  whoever. But then I get into the mess of apache / nginx / uwsgi config... and
  the trend these days seems to be to try and let users avoid that sort of
  hassle... Also, I really want to make sure people *actually* do this, and
  deploy their site, and I'd rather they were able to do it somewhere free...
- Can I make some instructions generic enough that they apply to all platforms?
  I'm not sure...

So, your suggestions much appreciated! How do you do your deploys?  Fabric?
FTP?  Git hooks?  Something else?  What do you think would work as a simple
solution for beginners?


