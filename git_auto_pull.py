import os
import sys
import getopt
import git
import subprocess

def is_git_repo(path):
    try:
        _ = git.Repo(path).git_dir
        return True
    except git.exc.InvalidGitRepositoryError:
        return False


def print_usage():
    print("Usage: auto_pull.py [-b <branch name>] [-h | --help] [-p | --path <path>]")
    sys.exit()


def exec_pull(repo, branch):
    g = git.cmd.Git(repo)
    g.init()
    try:
        g.checkout(branch)
        g.pull()
    except git.exc.GitCommandError:
        print("Fail")


def run(path, branch):
    filenames = os.listdir(path)
    for filename in filenames:
        fullpath = os.path.join(path, filename)
        if os.path.isdir(fullpath):
            if (is_git_repo(fullpath)):
                print(fullpath + " is git repo")
                old_path = os.getcwd()
                os.chdir(fullpath)
                exec_pull(fullpath, branch)
                os.chdir(old_path)
            else:
                search(fullpath)


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
                path = opt
            elif opt in ("-h", "--help"):
                print_usage()
            else:
                print("Unknown option: " + opt)
                print_usage()

    run(current_path, branch)

if __name__=="__main__":
    main(sys.argv[1:])
