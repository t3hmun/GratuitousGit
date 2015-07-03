# GratuitousGit
Python script that agressively commits and pushes changes using Git.

## What it does
* Tries to commit every x seconds if a change has been made.
* Tries to push every y seconds if a commit has been made (WIP just pushes instead of checking first).

## Work in progress
* Commit instantly on every save.
 * If many files are saved at the same time they will become grouped.
* Simple pulls.

## What it won't do
 * Use SSH (uneccassary complication for my needs).
 * Manage multiple repositories.

## Why
 * I'm using this to auto-save and push my Zim-Wiki to my Git server.
 * Also useful for recovering impulsively deleted un-commited content.

## Usage
### Warnings
 * The script only pushes its own branch.
 * If you allow the script to change branch it will continue from the state of the banch it switches from (not a normal merge).

### Setup
Edit the paths at the top of the script:
 * Set `git_path` to the path of your git.
 * Set `repo_path` to the path of the repository you wish to autocommit
 * Set `ac_branch` to whatever branch name you want for automatic commits.

Edit the delay times to suit your purposes.

Edit `x.txt` inserting you username, password, host and repo. Altenatively hardcode the value into the script

Start the script in a console (if you want to run the script hidden then you must edit the puse bit of the  script).

### Running
If the repository is not already on the `ac_branch` the script will pause and ask permission to change branch. The script will remain pause untill given permission.

Checking out another branch will cause the script to automatically pause. This is intended as a way to allow manual work to be done on the repository. The scritp will not resume untill it is told to. I tend to `merge --no-ff` on to my master branch when creating properly named commits.

## Current Status
Timer based commit and push working (03/07/2015)
Writing basic functionality (01/07/2015)
Planning (29/06/2015).

## Requirements
Built and tested on:
- WinPython 3.4 + Watchdog
- Windows 7
- git 1.9.5

## Participate
Feel free to pull-request, fork, issue or tell me where my code needs improvement, my Python is a long way from perfect.

## FAQ
 * Why no GitPython?
  * I decided this was going to be a super simple script, I thought another library might complicate things and hide simple implementation details.
