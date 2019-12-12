import pprint

from git_connector.git_connector import GithubConnector
from utilities import convert_year_to_start_and_end_time

def assigment_a(conn, github_orgname, pp):
    # The body, author username and date of all commit comments from 2017 in Shopify's repository list
    start_time, end_time = convert_year_to_start_and_end_time(2017)
    comments = conn.get_org_repo_comments_for_period(github_orgname, start_time, end_time)
    return [{'created_at': entry['created_at'], 'user_login': entry['user']['login'],'body': entry['body']} for entry in comments]


def assigment_b(conn, github_orgname, pp):
    # A list of all programming languages in Shopify's repository list
    repos = conn.get_github_repos_for_org(github_orgname)
    languages = set()
    for repo in repos:
        languages.update(conn.get_repo_languages(github_orgname, repo['name']))
    return languages


def assigment_c(conn, github_orgname, pp):
    # The names and URLs of the 50 most recent repositories in Shopify's repository list
    return [entry for entry in conn.get_latest_repos(github_orgname, limit=50)]


if __name__ == '__main__':
    conn = GithubConnector()
    pp = pprint.PrettyPrinter(indent=4)
    github_orgname = 'shopify'
    print('######## ASSIGNMENT A #########')
    pp.pprint(assigment_a(conn, github_orgname, pp))
    print('######## ASSIGNMENT B #########')
    pp.pprint(assigment_b(conn, github_orgname, pp))
    print('######## ASSIGNMENT C #########')
    pp.pprint(assigment_c(conn, github_orgname, pp))