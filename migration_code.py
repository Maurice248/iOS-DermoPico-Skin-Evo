import re
import requests
from requests.auth import HTTPBasicAuth
import time
import json

# Jira and GitHub credentials
jira_username = 'cmae@chowis.com'
jira_token = 'ATATT3xFfGF0vq9EHUQ6359pD1gGx3ORN7sZfEs3791D38Ny23_NeVV4nCxGtc0ugRerHCB9cbx2o_sGkdCPOzpyoT6DyjlUI0h4-XxQFSimynQPOoWngYoidvqzFlOhwfQH0uVmTGOAn370E7KtAtjB8V0kEjYXODRXDRZ4KPcs1FEZgFK1Rx8=B30B3604'
github_token = 'ghp_CkDkRVFR7BNUNv0wkqFxNV6cQoQpcm376un'

# Jira and GitHub URLs
jira_url = 'https://chowis.atlassian.net/rest/api/2/'
github_url = 'https://api.github.com/repos/Maurice248/iOS-DermoPico-Skin-Evo/issues'

# Fetch Jira issues
jira_issues_url = jira_url + 'search?jql=project=ADBS'
jira_issues_response = requests.get(jira_issues_url, auth=HTTPBasicAuth(jira_username, jira_token))
jira_issues = jira_issues_response.json()['issues']
github_issues_data = jira_issues

#JSon generator
with open ( 'github_issues_data.json', 'w' ) as json_file:     
    json.dump(github_issues_data, json_file, indent=2)

print ("GitHub issue data has been saved to 'github_issues_data.json'")    

# Transfer issues to GitHub
batch_size = 5  # Adjust as needed
x=0
for i in range(0, len(jira_issues), batch_size):
    batch = jira_issues[i:i + batch_size]

    for jira_issue in batch:
        # jira_status = jira_issue['fields']['status']['name']
        
        if jira_issue['fields']['status']['statusCategory']['name'] == 'To Do':
            print('\n\nTitle: '+ jira_issue['fields']['summary'] + '\nProject Name:' + jira_issue['fields']['project']['projectCategory']['name'] + '\n\nStatus Color: ' + jira_issue['fields']['status']['statusCategory']['colorName'])
            print('Issue:' + jira_issue['fields']['issuetype']['name'])
        
        x+=1

        github_issue_data = {
            'title': jira_issue['fields']['summary'],
            'body': jira_issue['fields']['description'],
            # 'labels': [label['name'] for label in jira_issue['fields']['labels']],
                # Add more fields as needed
        }

        # github_headers = {'Authorization': f'token {github_token}'}
        # github_response = requests.post(github_url, json=github_issue_data, headers=github_headers)

        # if github_response.status_code == 201:
        #     print(f"Successfully transferred Jira issue {jira_issue['key']} to GitHub.")
        # else:
        #     print(f"Failed to transfer Jira issue {jira_issue['key']} to GitHub. Error: {github_response.text}")

        # time.sleep(1)  # Introduce a 1-second delay between GitHub requests
        
       

    time.sleep(5)  # Introduce a 5-second delay between batches for Jira API rate limiting

print('There are {}  issues'.format(x)) 

