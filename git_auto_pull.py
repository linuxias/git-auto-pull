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


def git_cmd_checkout(repo_path, branch):
    print(repo_path)
    g = git.Git(repo_path)
    g.init()
    g.checkout(branch)


def exec_pull(path, branch):
    current_branch = get_branch_name(path)
    if not (current_branch == branch):
        git_cmd_checkout(path, branch)


def run(dirname, branch):
    filenames = os.listdir(dirname)
    for filename in filenames:
        fullpath = os.path.join(dirname, filename)
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

    run(current_path, branch)

if __name__=="__main__":
    main(sys.argv[1:])
