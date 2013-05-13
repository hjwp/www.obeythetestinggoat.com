Title: A lovely review! "like sitting down to pair-program with the author"
Date: 2013-05-13 8:35
Tags: review, pair programming, goat
Slug: review-a-conversation-with-a-developer
Author: Harry
Summary: <p>Jason wrote a review of my book, saying things like: "I find far too many programming books compartmentalize the material, each section is separate and abstract. Rather, this book's strength is in the broad use and application of these tools. By the end of this book you won't be a master with these tools but you will have used them enough to build a good foundation for starting your own projects and into the habit of test, code, refactor, commit."</p>

Jason, whom I met at PyCon this year, wrote a lovely review of my book [on the
O'Reily site](http://shop.oreilly.com/product/0636920029533.do). I'm very grateful because I think
he actually helped me to see some things I didn't realise myself about the book.  I'll reproduce
it here, for which I hope my publisher will forgive me:

> Programming books often fall into a few, easy to define categories. There are beginner's books, advanced books, reference books, books on specific libraries/frameworks, cookbooks, etc. "Test-Driven Web Development with Python" is none of the above; it's best described as a conversation with a developer.

> Reading the book is like sitting down to pair-program with the author, starting from scratch and building a basic web app. Along the way you'll obviously use Django, unit tests, and Selenium but you'll also use Git and other tools.

> I find far too many programming books compartmentalize the material, each section is separate and abstract. Rather, this book's strength is in the broad use and application of these tools. By the end of this book you won't be a master with these tools but you will have used them enough to build a good foundation for starting your own projects and into the habit of test, code, refactor, commit.

> For example, if you are new to open source development you'll hear about writing unit tests or using Git and want to use them yourself. But what's the next step, read a the unit test documentation or ProGit cover to cover? I don't need to be an expert, I just need someone to show me enough to get up and running. At that point I'll have completed a project and have the confidence and skills to tackle problems on my own.

> Like the answer to a job interview question, the book's biggest strength is also it's biggest weakness. Writing a book that covers so many tools the author must, by necessity, make assumptions about what the reader knows, and that's very, very hard.

> I came to the book without ever touching Django before. It wasn't always obvious how things worked nor why were doing them, particularly later in the book where there's more magic going on. I had to sit back and blindly follow along. At one point I got hung up because I mis-typed my URL, omitting a a forward-slash ("/") at the beginning, and my tests kept failing but I couldn't figure out why.

> Do URLs start with a forward slash? As a beginner, I don't know, and it's not obvious because Django does a lot of stuff for you. The code in the book was right, but I mis-typed it. I think had I come to the table with more Django experience I wouldn't have made that mistake.

> So while that's a particularly nasty typo, which really frustrated me, I can't say that a beginner should go off and read a Django book before attempting this one. In fact, quite the opposite. Because I got a survey of how everything works, covering so many tools so quickly, I'm in a much better position to troubleshoot and solve the problem myself. For example, "we've been writing a lot of unit tests, how can I write a unit test to help debug this unexpected failure?"

> Lastly, as I mentioned, the book is written like a conversation with a fellow developer at your side. There are numerous jokes and cultural references (e.g. refactoring cat, testing goat, etc.). This really lightens the tone (who doesn't joke with a co-worker?) as well as introduce the reader into the culture of open source development so that when you are walking around PyCon and someone has a stuffed goat or makes a "baaah" goat noise you'll fit right in! 

Writing the book in the style of a pair-programming conversation came naturally, since it's what
I do every day.  It's also the way that I learnt pretty much everything I'm writing about, so
it's natural that I should use it as a teaching style. Where Jason really has a point is that my
book isn't enough -- it's not a reference book, so you won't be able to use it as a reference
book.  It won't teach you everything about Django, or even everything about unit testing -- on
several occasions in the book I say "you should go and read the Django documentation", or "you
should take a look at the other assertion methods from the unittest module", and I think some
readers have found that frustrating.  "Why should I go elsewhwere to learn?"...

So I think this is something I need to set expectations about better, perhaps in the intro.
"This isn't a reference book".

Any thoughts? From current readers, do you agree with Jason?  Do you think the current style and
content of the book are working?

