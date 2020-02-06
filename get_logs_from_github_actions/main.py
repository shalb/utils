#!/usr/bin/env python3

import requests
import json
import time
import configuration as cfg


headers = {'Authorization': f'token {cfg.github_token}'}

def sleep_logs(seconds, msg):
    color = '\033[90m'
    reset_color = '\033[0m'

    if cfg.enable_sleep_logs:
        print(f'{color}{msg}, sleep {seconds}s{reset_color}')

    time.sleep(seconds)


def get_run_id(org, repo, workflow, headers):
    url = f'https://api.github.com/repos/{org}/{repo}/actions/workflows/{workflow}/runs'
    r = requests.get(url, headers=headers)
    try:
        run_id = json.loads(r.text)['workflow_runs'][0]['id']
    except KeyError:
        print('\033[93mCheck that "workflow_filename" variable set right\033[0m')
        exit(0)

    return run_id


def get_last_job_id(org, repo, run_id, headers):
    url = f'https://api.github.com/repos/{org}/{repo}/actions/runs/{run_id}/jobs'
    r = requests.get(url, headers=headers)
    job_id = json.loads(r.text)['jobs'][0]['id']

    return job_id


def get_logs(org, repo, job_id, headers):
    """
    Continiosly grub logs
    """
    old_logs = []
    no_logs = 0 # iterations

    while True:
        url = f'https://api.github.com/repos/{org}/{repo}/actions/jobs/{job_id}/logs'
        r = requests.get(url, headers=headers)

        logs = r.text.split('\n')
        difference = [ x for x in logs if x not in old_logs ]

        if len(difference):
            print('\n'.join(difference))
            no_logs = 0
        else:
            no_logs += 1

        if no_logs == cfg.leave_job_after_no_logs_iterations:
            break

        old_logs = logs
        sleep_logs(cfg.job_logs_update_interval, f'No new logs in job {job_id}')


def main():
    old_job_id = 0

    run_id = get_run_id(cfg.org, cfg.repo, cfg.workflow_filename, headers)
    job_id = get_last_job_id(cfg.org, cfg.repo, run_id, headers)

    while True:
        if job_id != old_job_id:
            print('\n'*80, f'Get logs from: https://github.com/{cfg.org}/{cfg.repo}/runs/{job_id}')
            get_logs(cfg.org, cfg.repo, job_id, headers)

        sleep_logs(cfg.search_for_new_jobs_interval, f'No new jobs in workflow {workflow_filename}')

        old_job_id = job_id


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        exit(0)
