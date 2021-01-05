from flask import Flask, request, jsonify
import git
import os
import subprocess

app = Flask(__name__)

ONLY_CHECK_BRANCH = "master"


def clone_repo_from_github(clone_url):
    print('Cloning {}'.format(clone_url))
    git.Git("/var/www").clone(clone_url)


def pull_repo_from_github(repo_path):
    print('Pulling {}'.format(repo_path))
    g = git.cmd.Git(repo_path)
    g.pull()

def run_start(repo_path):
    start_path = repo_path + "/" + "start.sh"

    if not os.path.isfile(start_path):
        return None

    subprocess.Popen(["/bin/bash ./start.sh"], cwd=repo_path, shell=True)

@app.route('/', methods=['POST', 'GET'])
def receive_data_from_github():
    data = request.json
    ref = data.get('ref', '')

    if not ref == "refs/heads/{}".format(ONLY_CHECK_BRANCH):
        print('{} is not {}'.format(ref, ONLY_CHECK_BRANCH))
        return jsonify({ 'error': True })

    repo = data.get('repository', {})
    clone_url = repo.get('clone_url', None)
    name = repo.get('name', '')

    full_path = '/var/www/{}'.format(name)
    
    if os.path.isdir(full_path):
        pull_repo_from_github(full_path)
    elif clone_url:
        clone_repo_from_github(clone_url)
    
    run_start(full_path)

    return jsonify({ 'hej': 1 })

app.run(debug=True, host='178.62.44.12')
