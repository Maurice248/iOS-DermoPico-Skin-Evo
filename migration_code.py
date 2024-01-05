import re
import requests
from requests.auth import HTTPBasicAuth
import time
import json

# Jira and GitHub credentials
jira_username = 'cmae@chowis.com'
jira_token = 'ATATT3xFfGF00qncQVm1HSYrY6Z4QACK-LHrhzeOcROGRxSDRqirJLaunRUFwxy5vbUviARU_Kl_M9iCjb3g3LJ_O5LzqZRqfjIHEzx5rUdjnKPFpsJAt2ukDRq4GJEmV7-n454UGKtdQPQ0uPB7IrQdObPfdxQdfNyZ1EgIScy0qpiDcAVy3nA=CE2A2101'
github_token = 'ghp_CkDkRVFR7BNUNv0wkqFxNV6cQoQpcm376un'

# Jira and GitHub URLs
jira_url = 'https://chowis.atlassian.net/rest/api/2/'
github_url = 'https://api.github.com/repos/Maurice248/iOS-DermoPico-Skin-Evo/issues'

# Fetch Jira issues
jira_issues_url = jira_url + 'search?jql=project=IDPS'
jira_issues_response = requests.get(jira_issues_url, auth=HTTPBasicAuth(jira_username, jira_token))
jira_issues = jira_issues_response.json()['issues']

# Transfer issues to GitHub
batch_size = 5  # Adjust as needed
for i in range(0, len(jira_issues), batch_size):
    batch = jira_issues[i:i + batch_size]

    for jira_issue in batch:
        # jira_status = jira_issue['fields']['status']['name']
        
        print(jira_issue['fields']['description'])

        github_issue_data = {
            'title': jira_issue['fields']['summary'],
            'body': jira_issue['fields']['description'],
            'labels': [label['name'] for label in jira_issue['fields']['labels']],
                # Add more fields as needed
        }

        github_headers = {'Authorization': f'token {github_token}'}
        github_response = requests.post(github_url, json=github_issue_data, headers=github_headers)

        if github_response.status_code == 201:
            print(f"Successfully transferred Jira issue {jira_issue['key']} to GitHub.")
        else:
            print(f"Failed to transfer Jira issue {jira_issue['key']} to GitHub. Error: {github_response.text}")

        time.sleep(1)  # Introduce a 1-second delay between GitHub requests

    time.sleep(5)  # Introduce a 5-second delay between batches for Jira API rate limiting
    
