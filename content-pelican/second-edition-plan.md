Title: Plans for the second edition
Date: 2016-09-25 18:52
Tags: Book, second edition, Persona
Author: Harry
Summary: I'm currently working on a 2nd edition for the book. Here's an outline of what I'm planning.

The second edition was mostly prompted by the [announcement by
Mozilla](https://mail.mozilla.org/pipermail/persona-notices/2016/000005.html)
that they were shutting down Persona in November 2016.  Given
that it would affect almost all the chapters from 15 thru to 21,
it seemed a good excuse to do a full second edition rather than
just an update.

Here, in brief, is an outline of the plan:


## Chapter rewrites:

* Rewrite chapters 15 + 16, replace persona with passwordless auth:
  [first draft done](http://www.obeythetestinggoat.com/book/chapter_15.html)

* Update chapters 17+ for persona changes: in progress

* Update JavaScript chapter for new version of QUnit: [done](http://www.obeythetestinggoat.com/book/chapter_14.html)

* Update deployment chapters to use Systemd instead of Upstart: started  but only in [ansible appendix](http://www.obeythetestinggoat.com/book/appendix_III_provisioning_with_ansible.html#_configuring_gunicorn_and_using_handlers_to_restart_services).

* Two new chapters on REST APIs and Ajax: 
  [code spiked](https://github.com/hjwp/book-example/commits/rest-api-spike), but
  chapters not yet written


## Minor updates + changes:

* Switch to using a virtualenv from the very beginning
* Upgrade to latest Django (1.10?)
* Use less HTML ids and more classes
* Use more early returns in FTs when refactoring partially finished user stories.


That's it, in very brief.  You can read more
[on the google group](https://groups.google.com/forum/#!topic/obey-the-testing-goat-book/fCENUr_NawM),
and feel free to join in the discussion there too, or here.  Let me know what
you think!


