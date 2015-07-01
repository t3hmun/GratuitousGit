import time
from subprocess import check_call
from subprocess import check_output
from subprocess import CalledProcessError
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


# Configurable paths
git_path = 'C:/Program Files (x86)/Git/bin/git.exe'
repo_path = 'W:/zim'
ac_branch = 'autocommit'
# Minimum delay between commits in seconds.
delay = 5

changed_detected = False


class DirModifiedCommitHandler(PatternMatchingEventHandler):
    """Handles modification events, ignoring the git directory"""

    def __init__(self):
        PatternMatchingEventHandler.__init__(self, ignore_patterns=['*\.git*'])

    def on_modified(self, event):
        print('\n### Change detected in\n ' + event.src_path)
        global changed_detected
        changed_detected = True


def commit(retry=False):
    """ Changes to autocommit branch and commits all changes"""
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
    if check_output(get_branch_name, cwd=repo_path) != ac_branch:
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
        while True:
            time.sleep(delay)
            if changed_detected:
                changed_detected = False
                commit()

    except (KeyboardInterrupt, SystemExit):
        observer.stop()
        raise


start()
