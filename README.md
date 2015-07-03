# GratuitousGit
Python script that agressively commits and pushes changes using Git.

## What it does (complete and functional)
* Tries to commit every x seconds if a change has been made.
 * Set the timer to 1 second to get almost instant commits on save. It will not do any git commands if there are no changes, the files are monitored.
 * If multiple files are saved together they will end up in the same commit. While it is possible to commit each changed file individually on file changed events, which would be excessive and unsuitable for my purposes.
* Tries to push every y seconds if a commit has been made (by the script, does not monitor manual commits).

## Work in progress / proposed developments.
* Simple pulls.

## What it won't do
 * Use SSH (unnecessary complication for my needs).
 * Manage multiple repositories.
 * Make use of gitignore
  * Git will still use it as normal, but this script will attempt to `add -A` when ignored files are changed (though nothing is added or committed).
  * This is only a problem if you happen to have rapidly modified ignore files causing `add -A` to be spammed. In this case try adding the ignore to `ignore_patterns` in the script.

## Why
 * I'm using this to auto-save and push my Zim-Wiki to my Git server.
 * Also useful for recovering impulsively deleted un-committed content.

## Usage
### Warnings
 * The script only pushes its own branch.
 * If you allow the script to change branch it will continue from the working tree state of the branch it switches from (not a normal merge, total replacement on the same tree).

### Setup
Edit the paths at the top of the script:
 * Set `git_path` to the path of your git.
 * Set `repo_path` to the path of the repository you wish to autocommit
 * Set `ac_branch` to whatever branch name you want for automatic commits.

Edit the delay times to suit your purposes.

Edit `x.txt` inserting you username, password, host and repo. Alternatively hardcode the value into the script

Start the script in a console (if you want to run the script hidden then you must edit the pause bit of the script).

### Running
If the repository is not already on the `ac_branch` the script will pause and ask permission to change branch. The script will remain pause untill given permission.

Checking out another branch will cause the script to automatically pause. This is intended as a way to allow manual work to be done on the repository. The script will not resume until it is told to. I tend to `merge --no-ff` on to my master branch when creating properly named commits.

## Development Status
Commit and push complete and usable (in use). May implement pull another day. (03/07/2015)
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
