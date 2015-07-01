import time
from subprocess import check_call
from subprocess import CalledProcessError
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# Configurable paths
git_path = 'C:/Program Files (x86)/Git/bin/git.exe'
repo_path = 'W:/zim'


class DirModifiedCommitHandler(FileSystemEventHandler):
    def on_modified(self, event):
        commit()


def commit(retry=False):
    print('## Starting commit.')
    now = str(time.time())
    addcmd = git_path + " add -A"
    commit_cmd = git_path + " commit -a -m 'autocommit:" + now + "'"

    try:
        check_call(addcmd, cwd=repo_path)
    except CalledProcessError:
        print('## Add failed.')
        if not retry:
            print('## ...retrying.')
            time.sleep(100)
            commit(True)
            return  # The retry will do the commit.

    try:
        check_call(commit_cmd, cwd=repo_path)
    except CalledProcessError:
        print('## Commit failed.')
        if not retry:
            print('# ...retrying.')
            time.sleep(100)
            commit(True)
    print('## Commit attempt complete.')


def start():
    ev_handler = DirModifiedCommitHandler()
    observer = Observer()
    observer.schedule(ev_handler, repo_path, recursive=True)
    observer.start()
    input('hit enter to end')
    observer.stop()


start()
