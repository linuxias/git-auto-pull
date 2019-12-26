#!/usr/bin/env python

import os
import subprocess
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description= \
            "Pulling for all of git-repositories from a specific directory recursively")

    parser.add_argument("-b", "--branch", required=True, type=str, help="Branch name to pull")
    parser.add_argument("-p", "--path", type=str, help="Path you want to start pulling")

    args = parser.parse_args()
    return args

def is_git_repo(path):
    return subprocess.call(['git', '-C', path, 'status'], \
            stderr=subprocess.STDOUT, stdout=open(os.devnull, 'w')) == 0

def exec_pull(branch):
    checkout_cmd = "git checkout " + branch
    subprocess.call(checkout_cmd, shell=True)
    subprocess.call("git pull > /dev/null", shell=True)

def run(path, branch):
    filenames = os.listdir(path)
    pathlist = [ os.path.join(path, filename) for filename in filenames ]
    dirlist = [ path for path in pathlist if os.path.isdir(path) ]
    for path in dirlist:
        if is_git_repo(path):
            old_path = os.getcwd()
            os.chdir(path)
            print(path + " is git repo")
            if not subprocess.call("git diff --quiet 2>/dev/null >&2", shell=True):
                if subprocess.call("git status | \
                        grep \'Your branch is ahead of\' > /dev/null", shell=True):
                    exec_pull(branch)
                else:
                    print("Your branch is ahead of \'origin\'" + branch)
            else:
                print("Unstaged file is existed")
            os.chdir(old_path)
        else:
            run(path, branch)

def main():
    args = parse_args()

    branch = args.branch
    start_path = os.getcwd()

    if args.path != None:
        start_path = args.path

    run(start_path, branch)

if __name__ == "__main__":
    main()
