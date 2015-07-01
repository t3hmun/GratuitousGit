import time
from subprocess import check_call
from subprocess import CalledProcessError
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


# Configurable paths
git_path = 'C:/Program Files (x86)/Git/bin/git.exe'
repo_path = 'W:/zim'
# Minimum delay between commits in seconds.
delay = 5

changed_detected = False


class DirModifiedCommitHandler(PatternMatchingEventHandler):
    def __init__(self):
        PatternMatchingEventHandler.__init__(self, ignore_patterns=['*\.git*'])

    def on_modified(self, event):
        print('\n### Change detected in\n ' + event.src_path)
        global changed_detected
        changed_detected = True


def commit(retry=False):
    print('## Starting commit.')
    now = str(time.time())

    # Git commands
    addcmd = git_path + " add -A"
    check_if_commit_is_needed = git_path + ' diff-index --quiet HEAD'
    commit_cmd = git_path + " commit -a -m 'autocommit:" + now + "'"

    # Try to add all, test is anything is added and then commit.
    try:
        check_call(addcmd, cwd=repo_path)
    except CalledProcessError:
        print('## Add failed.')
        if not retry:
            print('## ...retrying.')
            time.sleep(5)
            commit(True)
            return  # The retry will do the commit.
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
    global changed_detected
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
