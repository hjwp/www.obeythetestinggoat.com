Title: [OT] HiDPI on Ubuntu with a Samsung Ativ 9 
Date: 2014-12-14 23:39
Tags: Linux on the Desktop
Author: Harry
Summary: Totally off-topic, but my brief notes on getting HiDPI working with Ubuntu

This post isn't about TDD, but I just wanted to gather some notes into one place about how to get Hi-DPI working on Ubuntu.  I found other sources but my hope is that this will bring all the important tips into one place.

I have a character flaw as regards overly shiny laptops, and when my golden Sony Vaio Z series finally packed in after 3 years of service, it was time to get a new one.  The sensible choice would have been a Thinkpad or a Galago from System 76, but then I saw [this thing](http://www.mobiletechreview.com/notebooks/Samsung-ATIV-Book-9-Plus.htm), and I had to have it.  It has a ridiculous 3200x1600 Hi-DPI screen, which I knew for sure was never going to work properly under Linux.  But then, GNU/Linux is *meant* to be a bit rough on the desktop.  It's all part of the fun.


# Hi-DPI on Ubuntu in brief

* Set two Gnome UI settings:

```
gsettings set org.gnome.settings-daemon.plugins.xsettings overrides "{'Gdk/WindowScalingFactor': <2>}"

gsettings set org.gnome.desktop.interface scaling-factor 2
```

(You can also install `gnome-tweak-tool` to fiddle with these, cf the "Window" section for the most important one).

* In Firefox and Thunderbird, open *about:config* and change `layout.css.devPixelsPerPx` to somewhere between 1.6 and 2

*(Do *not* touch `layout.css.dpi`, that's a red herring).*

* Then fix up your grub prompt and TTY consoles, more info on that below.

Credit to the ever-impressive [Arch linux documentation](https://wiki.archlinux.org/index.php/HiDPI) for those tips.


# Adjusting the grub boot menu to make it readable

You'll have noticed that the GRUB boot menu is in a ridiculously small font because of all our teeny-tiny pixels.  Fix it by generating a new font in 30-point:

```
sudo grub-mkfont -s 30 -o /boot/grub/DejaVuSansMono.pf2 /usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf
```


DejaVu works well because it has all the glyphs for the line art, others may not work so well. 

Edit */etc/default/grub* and add a line saying `GRUB_FONT=/boot/grub/DejaVuSansMono.pf2`, and run `update-grub` to commit. There's more info [here](http://askubuntu.com/questions/11846/changing-the-default-grub-font). While you're at it, why not add a delightful background image to your boot screen?  Check out the [Ubuntu wiki](https://help.ubuntu.com/community/Grub2/Displays) for details.


# Adjusting your TTY console

One final thing that's pretty much unusable out of the box are the TTY consoles you get from pressing, eg, *CTRL+ALT+F1*.  To change their font, you'll want to do a:

    sudo dpkg-reconfigure console-setup

I picked the VGA font in 32x16, and it looks fine, if somewhat retro.



# And that's your lot!

Loads of things will still look pretty wrong.  Chromium is a bit broken, but I don't use it enough to warrant a lengthy investigation. I haven't tried any non-gnome apps, but presumably they will suffer.

Next challenge is getting reasonably good touchscreen support!


I leave you with a screenshot...

<a href="/static/images/hidpi_desktop_screenshot.png">
    <figure>
        <img src="/static/images/hidpi_desktop_screenshot.png" alt="screenshot" />
        <figcaption>So. Many. Pixels.</figcaption>
    </figure>
</a>


