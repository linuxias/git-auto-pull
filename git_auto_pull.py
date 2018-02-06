import os
import sys
import getopt
import subprocess

def is_git_repo(path):
    return subprocess.call(['git', '-C', path, 'status'], stderr=subprocess.STDOUT, stdout = open(os.devnull, 'w')) == 0

def exec_pull(repo, branch):
    checkout_cmd = "git checkout " + branch
    subprocess.call(checkout_cmd, shell=True);
    subprocess.call("git pull > /dev/null", shell=True);

def run(path, branch):
    filenames = os.listdir(path)
    for filename in filenames:
        fullpath = os.path.join(path, filename)
        if os.path.isdir(fullpath):
            if (is_git_repo(fullpath)):
                old_path = os.getcwd()
                os.chdir(fullpath)
                print(fullpath + " is git repo")
                if not (subprocess.call("git diff --quiet 2>/dev/null >&2", shell=True)):
                    if (subprocess.call("git status | grep \'Your branch is ahead of\' > /dev/null", shell=True)):
                        exec_pull(fullpath, branch)
                    else:
                        print("Your branch is ahead of \'origin\'" + branch)
                else:
                    print("Unstaged file is existed")
                os.chdir(old_path)
            else:
                run(fullpath, branch)

def print_usage():
    print("Usage: auto_pull.py [-b <branch name>] [-h | --help] [-p | --path <path>]")
    sys.exit()

def main(argv):
    branch = ''
    current_path = ''

    try:
        opts, args = getopt.getopt(argv, "hb:p:", ["help=", "branch=", "path="])
    except getopt.GetoptError:
        print_usage()

    if len(argv) == 0:
        print_usage()
    else:
        current_path = os.getcwd()
        for opt, arg in opts:
            if opt in ("-b", "--branch"):
                branch = arg
            elif opt in ("-p", "--path"):
                current_path = opt
            elif opt in ("-h", "--help"):
                print_usage()
            else:
                print("Unknown option: " + opt)
                print_usage()

    run(current_path, branch)

if __name__=="__main__":
    main(sys.argv[1:])
