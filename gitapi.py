import requests
from requests.auth import HTTPBasicAuth
from pprint import pprint
import io
import urllib
import whatthepatch

def commit_page_count(username, repo_owner,repo, auth_key,branch):
    """
    Return the number of commit pages to a project
    """
    pc=0
    sha ={branch}
    url = f'https://api.github.com/repos/{repo_owner}/{repo}/commits'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'token {auth_key}',
    }
    params = {
        'sha': sha,
        'per_page': 1,
    }
    resp = requests.get(url,auth=HTTPBasicAuth(username, auth_key))
    if (resp.status_code // 100) != 2:
        raise Exception(f'invalid github response: {resp.content}')
    # check the resp count, just in case there are 0 commits
    commit_count = len(resp.json())
    last_page = resp.links.get('last')
    # if there are no more pages, the count must be 0 or 1
    if last_page:
        # extract the query string from the last page url
        qs = urllib.parse.urlparse(last_page['url']).query
        # extract the page number from the query string
        pc = int(dict(urllib.parse.parse_qsl(qs))['page'])
    return pc

username = "jnewell88"
auth_key = "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"

url = f"https://api.github.com/users/{username}"

user_data = requests.get(url,auth=HTTPBasicAuth(username, auth_key)).json()

#repo_owner = "siyengar16"
#repo = "mogra_ui_pasco"
repo_owner = "KeenanDS"
repo ="dusk_website"

contributor_commits = {}
contributor_additions = {}
contributor_deletions = {}
contributor_file_additions = {}
new_files = []
modified_files = []
get_branches_url = f"https://api.github.com/repos/{repo_owner}/{repo}/branches"
branch_data = requests.get(get_branches_url,auth=HTTPBasicAuth(username, auth_key)).json()
for branch in branch_data:
	contributor_commits.clear()
	contributor_additions.clear()
	contributor_deletions.clear()
	contributor_file_additions.clear()
	pprint("BRANCH:" +branch['name'])
	page_count = commit_page_count(username,repo_owner,repo,auth_key,branch['commit']['sha'])
	if(page_count == 0):
		commit_url = f"https://api.github.com/repos/{repo_owner}/{repo}/commits?sha={branch['commit']['sha']}"
		commit_data = requests.get(commit_url,auth=HTTPBasicAuth(username, auth_key)).json()
		for commit in commit_data:
			new_files.clear()
			modified_files.clear()
			msg = commit['commit']['message']
			user = commit['committer']['login']
			date = commit['commit']['committer']['date']
			if user in contributor_commits.keys():
				pprint("COMMIT (" +user+"--"+date+"):" + branch['name'] +"-"+msg)
				contributor_commits[user] +=1 
			else:
				pprint("COMMIT (" +user+"--"+date+"):" + branch['name'] +"-"+msg)
				contributor_commits[user] = 1
			url_get_commits_data = commit['url']
			commit_details = requests.get(url_get_commits_data,auth=HTTPBasicAuth(username, auth_key)).json()
			committed_files = commit_details['files']
			for file in committed_files:
				if(file['additions'] > 0 and file['deletions'] > 0 and file['changes'] > 0  and 'patch' in file):
					#pprint(file['filename'])
					if(file['additions'] > 0):
						if user in contributor_additions.keys():
							contributor_additions[user] += file['additions']
						else:
							contributor_additions[user] = file['additions']
					if(file['deletions'] > 0):
						if user in contributor_deletions.keys():
							contributor_deletions[user] += file['deletions']
						else:
							contributor_deletions[user] = file['deletions']
					modified_files.append(file['filename'])
					diff = [x for x in whatthepatch.parse_patch(file['patch'])]
					#pprint(diff[0])
				else:
					new_files.append(file['filename'])
					if user in contributor_file_additions.keys():
						contributor_file_additions[user] += 1
					else:
						contributor_file_additions[user] =1
	else:
		i=1
		while i <= page_count:
			commit_url = f"https://api.github.com/repos/{repo_owner}/{repo}/commits?page={i}&sha={branch['commit']['sha']}"
			commit_data = requests.get(commit_url,auth=HTTPBasicAuth(username, auth_key)).json()
			for commit in commit_data:
				new_files.clear()
				modified_files.clear()
				msg = commit['commit']['message']
				user = commit['committer']['login']
				date = commit['commit']['committer']['date']
				if user in contributor_commits.keys():
					pprint("COMMIT (" +user+"--"+date+"):" + branch['name'] +"-"+msg)
					contributor_commits[user] +=1 
				else:
					pprint("COMMIT (" +user+"--"+date+"):" + branch['name'] +"-"+msg)
					contributor_commits[user] = 1
				url_get_commits_data = commit['url']
				commit_details = requests.get(url_get_commits_data,auth=HTTPBasicAuth(username, auth_key)).json()
				committed_files = commit_details['files']
				for file in committed_files:
					if(file['additions'] > 0 and file['deletions'] > 0 and file['changes'] > 0  and 'patch' in file):
						#pprint(file['filename'])
						if(file['additions'] > 0):
							if user in contributor_additions.keys():
								contributor_additions[user] += file['additions']
							else:
								contributor_additions[user] = file['additions']
						if(file['deletions'] > 0):
							if user in contributor_deletions.keys():
								contributor_deletions[user] += file['deletions']
							else:
								contributor_deletions[user] = file['deletions']
						modified_files.append(file['filename'])
						diff = [x for x in whatthepatch.parse_patch(file['patch'])]
						#pprint(diff[0])
					else:
						new_files.append(file['filename'])
						if user in contributor_file_additions.keys():
							contributor_file_additions[user] += 1
						else:
							contributor_file_additions[user] =1
			i+=1
	pprint("CONTRIBUTOR COMMITS:")
	pprint(contributor_commits)
	pprint("CONTRIBUTOR ADDITIONS:")
	pprint(contributor_additions)
	pprint("CONTRIBUTOR DELETIONS:")
	pprint(contributor_deletions)
	pprint("CONTRIBUTOR NEW FILE ADDITIONS:")
	pprint(contributor_file_additions)






# new_url = f"https://api.github.com/repos/{user}/{repo}/contents/config.py"
# files = requests.get(new_url,auth=HTTPBasicAuth(username, auth_key)).json()
# pprint(files)

# url_new = "https://raw.githubusercontent.com/siyengar16/mogra_ui_pasco/main/config.py?token=ABHTP5QF4X73RDR3LX53ZB3BF7TQU"
# resp = requests.get(url_new,auth=HTTPBasicAuth(username, auth_key))

# import io
# with io.open("Benchmark_Data.py", "w", encoding="utf-8") as f:
#     f.write(resp.text)
# f.close()

