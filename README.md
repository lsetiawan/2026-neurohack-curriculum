# NeuroHackademy 2026 Curriculum

This repository contains the curriculum for the 2026 NeuroHackademy!
Instructors can put course materials in this repository, and they will
appear in your home directory on the NeuroHackademy 2026 JupyterHub.

This README file additionally contains some general information on
using the JupyterHub.


## Using a terminal on the JupyterHub

When you first open the JupyterLab interface on the NeuroHackademy
JupyterHub, it should open a "launcher" panel. You can also open such
a panel by pressing the blue "+" button in the upper left corner of
the interface. One of the options toward the bottom of the launcher
panel is to launch a terminal. The terminal that is launched is just
like a terminal on your local machine except that it is running in the
cloud on the JupyterHub. You can use this interface to run shell
commands including git commands.


## Setting up Git and GitHub on the NeuroHackademy JupyterHub

Git is used heavily in the NeuroHackademy. It has already been
installed on the NeuroHackademy JupyterHub, but you'll need to
configure it before you can use it. Configuring git requires just a
few steps:
  1. Tell git your name and email address.
  2. Create an ssh key for authentication on the JupyterHub and provide GitHub
     with this key.
  3. Optionally, configure other items such as your preferred editor.

These steps are explained in detail by [the Software Carpentry tutorial on Git
and GitHub](https://swcarpentry.github.io/git-novice/index.html). In
particular, [this page explains the basic git
configuration](https://swcarpentry.github.io/git-novice/02-setup.html) and
[this page explains how to set up SSH
keys](https://swcarpentry.github.io/git-novice/07-github.html#ssh-background-and-setup).

If you are unfamiliar with these steps, we recommend that you attend the
introductory session on Git and GitHub on Tuesday (July 14th) at 1:30pm where
we will walk through them as a group.


## Uploading and Downloading Data

You can upload data to the JupyterHub by dragging files into the
left-side panel (the file browser) in the JupyterLab interface. You
can also right-click on a file in the same panel to download it.

If you need to download several files or an entire directory, you can
first tar/zip the files then untar/unzip them once you download
them. For example, if you want to download everything in a directory
called "work/" that exists in your home directory on the Hub:

```bash
tar zcf work.tar.gz work/
```

This creates a file `work.tar.gz` that contains the `work/` folder and
all of its contents. You can then download that file and unzip it
locally.

