import json
import os
import re

from flask import abort, Flask, jsonify, request, Response
from flask_httpauth import HTTPBasicAuth
from git_connector.git_connector import GithubConnector

app = Flask(__name__)
auth = HTTPBasicAuth()
git_conn = GithubConnector()

@auth.verify_password
def verify_password(username, password):
    # This is extremely bad, and should not ever be done in real life.
    # But for the shake of just having and showing use of basic auth
    # it will do for now.
    return username == 'username' and password == 'password'


@app.before_request
def check_repo_and_org():
    if 'LIMITED_INPUT' not in os.environ or os.environ['LIMITED_INPUT'] != 'TRUE':
        return
    allowed_organizations_and_repos = {
        'shopify': [
            'node-themekit',
            'shopify_api',
            'eslint-plugin-shopify',
        ]
    }
    exception_endpoints = ['most_recent_repos']

    path_components = str.split(request.path.lower(), '/')
    if path_components[-1] in exception_endpoints:
        return
    org_name = path_components[1].lower()
    repo_name = path_components[2].lower()
    if (org_name not in allowed_organizations_and_repos or 
        repo_name not in allowed_organizations_and_repos[org_name]):
        abort(Response(
            '''
                Your supplied organization or repo (%s, %s), is not in the accepted set. <br/>
                Please use an approved orginazation or repo, or disable this functionality. <br/>
                The approved parameters are <br/>
                %s
            ''' % (org_name, repo_name, json.dumps(allowed_organizations_and_repos)),
            status=400))
    

@app.route("/<orgname>/<repo>/<year>/comments")
@auth.login_required
def get_comments_for_repo_for_year(orgname, repo, year):
    if not re.match('[1-2]\d{3}', year):
        abort(Response(
            'Year parameter was not in the correct format, expected: YYYY, got %s' % year,
            status=400))
    year_int = int(year)
    return jsonify(git_conn.get_repo_comments_for_year(orgname, repo, year_int))


@app.route("/<orgname>/<repo>/languages")
@auth.login_required
def get_languages_for_repo(orgname, repo):
    return jsonify(git_conn.get_repo_languages(orgname,repo))


@app.route("/<orgname>/<int:limit>/most_recent_repos")
@auth.login_required
def get_most_resent_repo(orgname, limit):
    return jsonify([entry for entry in git_conn.get_latest_repos(orgname, limit)])


if __name__ == "__main__":
    app.run(host='0.0.0.0')