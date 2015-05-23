Title: The absolute beginner's guide to Linux servers
Tags: linux, gnu, servers, sysadmin, ssh, private keys
Author: Harry
Status: draft
Summary: <p>A very brief guide to how to start and control a Linux server</p>

This guide attempts to give people who've never used a Linux server some
of the most basic notions for how to start one, and how to control it.

The original reason for it was that, at Chapter 8 
[in my book](http://chimera.labs.oreilly.com/books/1234000000754/ch08.html) the
learning curve suddenly takes a *major* turn for the steeper, for readers
who've never had to work with Linux servers before.  This is my attempt to
provide a basic guide to how to get going with them -- not necessarily just
for my readers, but for anyone that might need a quick intro and how-to for
spinning up and remote controlling a linux server.


# Basic concepts

Don't worry if these definitions don't make sense quite yet (although do feel
free to suggest improvements to the wording).  They'll make more sense once we
actually start to *do* stuff, but it's nice to set the scene with a bit of
an overview.

* **Server/VM** A server is a computer that's designed to provide a service
  over a network, usually over the Internet. Because the services they provide
  are usually text-based or "just" ones and zeroes (like email or web pages),
  servers usually don't have a display of their own; instead, we connect to them
  remotely. These days, servers are often actually a **VMs**, or **Virtual
  Machine** -- one physical server hosts several virtual servers, but the
  virtual servers behave as if they were totally independent machines.

* **SSH**, or Secure Shell, is when you connect up the command line terminal on
  your machine to a remote machine, and you can then run commands on that
  remote machine.  To "log in" to that remote machine, you can either use a
  username and password, or...

* **public/private key authentication** is an alternative to username and
  passwords for authenticating with servers.  It's based on what's called
  public-key cryptography, where you have a pair of keys, one public and 
  one private.  The private key is the one you have to keep secret, and you
  can use the public key, along with a bit of maths voodoo, to prove to the
  server that you have the private key, without actually having to reveal
  it to anyone (unlike a password, which you have to send to the server).
  It's the same basic principle that underpins HTTPS in your web browser.
  
* **root & sudo** many of the things you'll want to do on a Linux server,
  like installing new software or configuring system services, require
  "root" (which means the highest-level) access.  **sudo** lets "normal"
  users become root temporarily.  We'll have a normal user with sudo access
  in our examples below.


# Starting a server

## At home

## Amazon AWS

## Digital Ocean


# Getting public / private key authentication set up


# Installing some software


# Vim


