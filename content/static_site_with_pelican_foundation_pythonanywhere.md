Title: Building a static blog site with Pelican and Foundation on PythonAnywhere
Date: 2013-04-19 10:00
Tags: pelican, blog, tools
Author: Harry
Status: draft
Summary: How I put this site together, using the Pelican static blog site generator, the Foundation HTML5/CSS framework, and PythonAnywhere

I thought a few notes on how I pulled together this site by integrating the
Pelican static blog generator and the Foundation HTML5/CSS framework might be
of interest.

A static HTML site on PythonAnywhere
------------------------------------

Full disclosure: I work at PythonAnywhere.  Skip this bit if you prefer a
different hosting provider. But we do happen to have built a pretty 
low-effort way of getting websites off the ground.

Even though we don't have a specific option for "static HTML site",
PythonAnywhere has support for static file directories, and is set up to serve
any files called "index.html" that are inside any of your static directories.

So when starting a new site on PythonAnywhere, you can just pick any of the 
WSGI microframeworks on offer, and then completely ignore it from there on
(although who knows, it might come in useful later if you want to add some
more functionality to the site).  I chose Flask.

The next step is creating a simple *index.html* and serving it from a static
directory mapped to the URL for the root of the site, `/`

<insert screenshot>

    <html>
        <p>Hello from a static page</p>
    </html>

That should replace the "Hello from Flask" on the site with a "Hello from 
a static page"


<insert screenshot>

Starting with a basic Foundation site
-------------------------------------

I wanted to achieve two things:  have a homepage for my book that would
point people towards where they can buy it or read it for free, and also
to host a new blog.  The first was more important, so in true agile style
I decided to make sure I could do that first.

I started by replacing *index.html* with one of the samples from the foundation
site, and checking that it worked.  The main thing to check was that the css
all loaded OK.

<link>
<screenshot>

I actually set up a separatic static files directory with the URL /static/, but
in retrospect I think you could get away without that, just using subfolders in
the main directory which is already mapped to "/".

Then I had the usual pain of fiddlinig with CSS to get the exact column + 
row alignmment I wanted.  Made substantially easier by Foundation, yes, but 
still a hassle.  By the end I had something like this:

<screenshot>

The main bit of customisation of foundation I did was to use different fonts.
I got mine from google web fonts.

<how did I get scss to work??>


Bringing in Pelican
-------------------

I then installed Pelican on my local PC and went through its default 
'quickstart' setup.  Once it's configured, you just run `make html` and
it pulls in all your blog posts and other pages from a folder called
*content*, converting them from mardown or RST to HTML.  Perfect,
except it has its own CSS and theme, which look nothing like my site.

A pelican theme is a series of jinja2 templates in a folder. Making a custom
theme just means replacing those files.  I just copied the basic theme,
stripped out a lot of the unnecessary HTML scaffolding (mostly class=) stuff,
and used tools from foundation instead.  The key thing is that the pelican
theme shows all the template tags you might want to use for each part of the
theme, which means it really is a matter of tweaking things rather than
reinventing the wheel. Here's the diff from my version of *article.html*, the
template for blog posts:


    $ diff -b `pwhich.py pelican`/themes/simple/templates/article.html theme/templates/article.html 
    3c3,4
    < <section id="content" class="body">
    ---
    > <div class="row">
    >     <div class="large-9 small-12 columns"> <!-- blog post div -->
    5,7c6,7
    <     <h2 class="entry-title">
    <       <a href="{{ article.url }}" rel="bookmark"
    <          title="Permalink to {{ article.title|striptags }}">{{ article.title }}</a></h2>
    ---
    >             <h2><a href="{{ article.url }}" rel="bookmark" title="Permalink to {{ article.title|striptags }}">{{ article.title }}</a></h2>
    > 
    9a10
    > 
    21c22,23
    <   <div class="entry-content">
    ---
    > 
    >         <div>
    24c26,31
    < </section>
    ---
    > 
    >         {% include 'comments.html' %}
    > 
    >     </div>
    >     {% include 'sidebar.html' %}
    > </div>



