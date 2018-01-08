import os
import git
import sys
import getopt

def search(dirname):
    filenames = os.listdir(dirname)
    for filename in filenames:
        fullpath = os.path.join(dirname, filename)
        if os.path.isdir(fullpath):
            if (is_git_repo(fullpath)):
                print(fullpath + " is git repo")
            else:
                search(fullpath)

def is_git_repo(path):
    try:
        _ = git.Repo(path).git_dir
        return True
    except git.exc.InvalidGitRepositoryError:
        return False

def print_usage():
    print("Usage : auto_pull.py -b <branch_name>")
    sys.exit()

def main(argv):
    branch = ''
    try:
        opts, args = getopt.getopt(argv, "hb:", ["branch="])
    except getopt.GetoptError:
        print_usage()

    if len(argv) == 0:
        print_usage()
    else:
        for opt, arg in opts:
            if opt in ("-b", "--branch"):
                branch = arg
            else:
                print_usage()
    print("Branch is " + branch)
    current_path = os.getcwd()
    search(current_path)

if __name__=="__main__":
    main(sys.argv[1:])
