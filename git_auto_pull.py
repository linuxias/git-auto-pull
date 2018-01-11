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


def get_branch_name(repo):
    active_branch = git.Repo(repo).active_branch.name
    print(active_branch)
    return active_branch.strip()


def print_usage():
    print("Usage: auto_pull.py [-b <branch name>] [-h | --help] [-p | --path <path>]")
    sys.exit()


def git_cmd_checkout(repo, branch):
    print(repo)
    try:
        g = git.Git(repo)
        g.init()
        g.checkout(branch)
    except git.exc.GitCommandError:
        print("Fail")


def exec_pull(repo, branch):
    current_branch = get_branch_name(repo)
    if not (current_branch == branch):
        git_cmd_checkout(repo, branch)


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
