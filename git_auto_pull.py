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


def get_branch_name(path):
    old_path = os.getcwd()
    os.chdir(path)
    active_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    os.chdir(old_path)
    return active_branch

def print_usage():
    print("Usage: auto_pull.py [-b <branch name>] [-h | --help] [-p | --path <path>]")
    sys.exit()


def search(dirname):
    filenames = os.listdir(dirname)
    for filename in filenames:
        fullpath = os.path.join(dirname, filename)
        if os.path.isdir(fullpath):
            if (is_git_repo(fullpath)):
                print(fullpath + " is git repo")
                print(get_branch_name(fullpath))
            else:
                search(fullpath)

def main(argv):
    branch = ''
    current_path = os.getcwd()

    try:
        opts, args = getopt.getopt(argv, "hb:p:", ["help=", "branch=", "path="])
    except getopt.GetoptError:
        print_usage()

    if len(argv) == 0:
        print_usage()
    else:
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

    search(current_path)

if __name__=="__main__":
    main(sys.argv[1:])
