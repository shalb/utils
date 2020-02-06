#!/usr/bin/python3

import os
import requests
import json
import time

TOKEN=os.environ['GITHUB_TOKEN']
ORG='shalb'
REPO='cluster.dev'
WORKFLOW_FILENAME='gh-5.yaml'

headers = {'Authorization': f'token {TOKEN}'}


def get_run_id(org, repo, workflow, headers):
    url = f'https://api.github.com/repos/{org}/{repo}/actions/workflows/{workflow}/runs'
    r = requests.get(url, headers=headers)
    run_id = json.loads(r.text)['workflow_runs'][0]['id']

    return run_id


def get_last_job_id(org, repo, run_id, headers):
    url = f'https://api.github.com/repos/{ORG}/{REPO}/actions/runs/{run_id}/jobs'
    r = requests.get(url, headers=headers)
    job_id = json.loads(r.text)['jobs'][0]['id']

    return job_id


def get_logs(org, repo, job_id, headers):
    """
    Continiosly grub logs
    """
    old_logs = []
    no_logs = 0 # iterations
    second_sleep = 3

    while True:
        url = f'https://api.github.com/repos/{org}/{repo}/actions/jobs/{job_id}/logs'
        r = requests.get(url, headers=headers)

        logs = r.text.split('\n')
        difference = [ x for x in logs if x not in old_logs ]

        if len(difference):
            print('\n'.join(difference))
            no_logs = 0
        else:
            no_logs += 1 # iterations

        if no_logs > 10: # iterations
            break

        old_logs = logs
        print (f'\033[90mNo new logs in job {job_id}, waiting {second_sleep}s\033[0m')
        time.sleep(second_sleep) # seconds


old_job_id = 0

run_id = get_run_id(ORG, REPO, WORKFLOW_FILENAME, headers)
job_id = get_last_job_id(ORG, REPO, run_id, headers)

while True:
    if job_id != old_job_id:
        get_logs(ORG, REPO, job_id, headers)

    print (f'\033[90mNo new jobs in workflow {WORKFLOW_FILENAME}, sleep 10s\033[0m')
    time.sleep(10)

    old_job_id = job_id
