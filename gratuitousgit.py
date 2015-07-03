import time
from subprocess import check_call
from subprocess import check_output
from subprocess import CalledProcessError
import subprocess
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


# Configurable paths
git_path = 'C:/Program Files (x86)/Git/bin/git.exe'
repo_path = 'W:/zim'
ac_branch = 'autocommit'
remote = "syncserver"

# Minimum delays in seconds.
commit_delay = 1
push_delay = 2  # Needs to be a multiple of commit_delay.
changed_detected = False

# The SSH password used on push.
with open('x.txt', 'r') as cf:
    password = cf.read()


class DirModifiedCommitHandler(PatternMatchingEventHandler):
    """Handles modification events, ignoring the git directory"""

    def __init__(self):
        PatternMatchingEventHandler.__init__(self, ignore_patterns=['*\.git*'])

    def on_modified(self, event):
        print('\n### Change detected in\n ' + event.src_path)
        global changed_detected
        changed_detected = True


def push():
    """ Pushes onto same name tracking branch."""
    push_cmd = git_path + ' push ' + remote + ' ' + ac_branch + ' -u'
    print(push_cmd)
    try:
        print(check_output(push_cmd, cwd=repo_path))
    except CalledProcessError:
        print('CPE bro')

    print('end_push')


def commit(retry=False):
    """ Changes to autocommit branch and commits all changes."""
    print('## Starting commit.')
    now = str(time.time())

    # Git commands
    addcmd = git_path + " add -A"
    check_if_commit_is_needed = git_path + ' diff-index --quiet HEAD'
    commit_cmd = git_path + " commit -a -m 'autocommit:" + now + "'"
    get_branch_name = git_path + " symbolic-ref --short -q HEAD"
    reset = git_path + ' reset'
    switch_without_changing_working_dir = git_path + ' symbolic-ref HEAD refs/heads/' + ac_branch
    check_branch_exists = git_path + ' rev-parse --verify ' + ac_branch  # 0 return code for success.
    create_branch = git_path + ' checkout -b ' + ac_branch

    # Switch or create branch.
    # It is done in a manner that does not affect the working tree.
    # Results in morphing the autocommit branch into the current working state.
    # If you manually switch to another branch this script becomes paused.
    # Decode because its bytes not unicode, and also strip the newline.
    actual_branch = check_output(get_branch_name, cwd=repo_path).decode('ascii').strip()
    if actual_branch != ac_branch:
        print('## PAUSED: ON WRONG BRANCH')
        if input('## Would you like to switch branch or retry now (y/n)?') != 'y':
            print('## Commit attempt aborted.')
            commit()
            return
        try:
            check_call(check_branch_exists, cwd=repo_path)
        except CalledProcessError:
            check_call(create_branch, cwd=repo_path)
        try:
            check_call(switch_without_changing_working_dir, cwd=repo_path)
            check_call(reset, cwd=repo_path)
        except CalledProcessError:
            print('## Branch change failed, quitting.')
            raise SystemExit(1)

    # Try to add all.
    try:
        check_call(addcmd, cwd=repo_path)
    except CalledProcessError:
        print('## Add failed.')
        if not retry:
            print('## ...retrying.')
            time.sleep(5)
            commit(True)
            return  # The retry will do the commit.

    # Check if there is anything to commit then commit.
    try:
        check_call(check_if_commit_is_needed, cwd=repo_path)
        print('## Nothing to commit.')
    except CalledProcessError:
        try:
            check_call(commit_cmd, cwd=repo_path)
        except CalledProcessError:
            print('## Commit failed.')
            if not retry:
                print('# ...retrying.')
                time.sleep(2)
                commit(True)
    print('## Commit attempt complete.')


def start():
    # Start with a commit, handle any required branch change.
    commit()

    global changed_detected
    # Configure the directory monitor.
    ev_handler = DirModifiedCommitHandler()
    observer = Observer()
    observer.schedule(ev_handler, repo_path, recursive=True)
    observer.start()

    try:
        counter = 0
        while True:
            time.sleep(commit_delay)
            counter += commit_delay
            if changed_detected:
                changed_detected = False
                commit()
            if counter >= push_delay:
                counter = 0
                push()

    except (KeyboardInterrupt, SystemExit):
        observer.stop()
        raise


start()
