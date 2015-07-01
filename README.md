# GratuitousGit
Background python script to agressively commit changes and push them on a timer. 

## What it will do
* Watch project folder.
* Commit ~~on every file change~~ _every x seconds if a files changes_ on a special autocommit branch.
  *  Often many files change together (especially in Zim) so commits always need to be grouped. A polled model seems to be more efficient than triggering a hundred changed file events suddenly.
* Automatically rolls up automatic-commits when user wants to manually commit.
* Automatically pushes on a timer.

* One file script (ideally).


## What it wont do
* Pull

* Making it a one file script limits the max level of maintainable complexity.

## Why
I'm planning on using this to add auto-save and push functionality to Zim-Wiki on windows.

Also be useful for making freshly written impulsively deleted code recpverable.

## Current Status
Writing basic functionality (01/07/2015)
Planning (29/06/2015).

## Requirements
Built and tested on:
Python 3.4, Windows 7, git 1.9.5
