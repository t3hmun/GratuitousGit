from subprocess import check_call
import time

# Configurable paths
gitpath = 'C:/Program Files (x86)/Git/bin/git.exe'
repopath = 'W:/zim'


def commit(path):
    now = str(time.time())
    addcmd = gitpath + " add -A"
    commitcmd = gitpath + " commit -a -m 'autocommit:" + now + "'"
    check_call(addcmd, cwd=path)
    check_call(commitcmd, cwd=path)

commit(repopath)
input('end')
