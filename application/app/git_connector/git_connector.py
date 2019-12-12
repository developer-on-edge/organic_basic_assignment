import logging
import requests

from dateutil.parser import parse as date_parser
from datetime import datetime, timezone
from utilities import convert_year_to_start_and_end_time, get_environment_variable


class GithubConnector:

    def __init__(self):
        self.username = get_environment_variable('github_username')
        self.token = get_environment_variable('github_token')


    def send_request(self, url):
        response = requests.get(
            url,
            headers={'Accept': 'application/vnd.github.v3+json'},
            auth=(self.username, self.token)
        )
        if response.status_code != 200:
            
            logging.error(response.headers)
            logging.error(response.text)
            response.raise_for_status()
        return response


    def retrieve_request_generator(self, url):
        request_url = url
        while True:
            response = self.send_request(request_url)
            yield response
            if 'next' not in response.links:
                break
            request_url = response.links['next']['url']


    def retrieve_complete_request(self, url):
        complete_response = []
        for response in self.retrieve_request_generator(url):
            complete_response += response.json()
        return complete_response


    def get_github_repos_for_org(self, github_orgname):
        url = 'https://api.github.com/orgs/%s/repos' % github_orgname
        return self.retrieve_complete_request(url)


    def get_github_repo(self, github_orgname, github_repo):
        url = 'https://api.github.com/repos/%s/%s' % (github_orgname, github_repo)
        return self.retrieve_complete_request(url)


    def get_repo_comments_for_period(self, github_orgname, repo, start_time, end_time):
        comments_url = 'https://api.github.com/repos/%s/%s/comments' % (github_orgname, repo)
        comments = self.retrieve_complete_request(comments_url)
        if len(comments) == 0:
            return
        for comment in comments:
            comment_created_at = date_parser(comment['created_at'])
            if start_time <= comment_created_at <= end_time:
                yield comment
    

    def get_org_repo_comments_for_period(self, github_orgname, start_time, end_time):
        repos = self.get_github_repos_for_org(github_orgname)
        for entry in repos:
            for comment in self.get_repo_comments_for_period(github_orgname, entry['name'], start_time, end_time):
                yield comment


    def get_repo_comments_for_year(self, github_orgname, github_repo, year):
        start_time, end_time = convert_year_to_start_and_end_time(year)
        return [{
            'created_at': entry['created_at'],
            'user_login': entry['user']['login'],
            'body': entry['body']
            } for entry in self.get_repo_comments_for_period(github_orgname, github_repo, start_time, end_time)]


    def get_repo_languages(self, github_orgname, github_repo):
        languages = set()
        for response in self.retrieve_request_generator('http://api.github.com/repos/%s/%s/languages' % (github_orgname, github_repo)):
            languages.update(response.json().keys())
        return list(languages)


    def get_latest_repos(self, github_orgname, limit=50):
        repos = self.get_github_repos_for_org('shopify')
        for repo in sorted(repos, key=lambda x: date_parser(x['created_at']), reverse=True)[:limit]:
            yield {'name': repo['name'], 'html_url': repo['html_url']}
