from django.shortcuts import render
from django.conf import settings
import requests

from github import Github, GithubException


def home(request):
    is_cached = ('geodata' in request.session)

    if not is_cached:
        IPSTACK_KEY = 'hogehoge' # 書き換え
        response = requests.get('http://api.ipstack.com/check?access_key={}'.format(IPSTACK_KEY))
        result = response.json()
        response = requests.get('http://api.ipstack.com/{0}?access_key={1}'.format(result['ip'], IPSTACK_KEY))
        request.session['geodata'] = response.json()

    geodata = request.session['geodata']

    return render(request, 'apisumple/home.html', {
        'ip': geodata['ip'],
        'country': geodata['country_name'],
        'latitude': geodata['latitude'],
        'longitude': geodata['longitude'],
        'api_key': 'hogehoge', # 書き換え
        'is_cached': is_cached,
    })

def github(request):
    search_result = {}
    if 'username' in request.GET:
        username = request.GET['username']
        url = 'https://api.github.com/users/%s' % username
        response = requests.get(url)
        search_was_successful = (response.status_code == 200)
        search_result = response.json()
        search_result['success'] = search_was_successful
        search_result['rate'] = {
            'limit': response.headers['X-RateLimit-Limit'],
            'remaining': response.headers['X-RateLimit-Remaining'],
        }
    return render(request, 'apisumple/github_api.html', {'search_result': search_result})

def github_client(request):
    search_result = {}
    if 'username' in request.GET:
        username = request.GET['username']
        client = Github()

        try:
            user = client.get_user(username)
            search_result['name'] = user.name
            search_result['login'] = user.login
            search_result['public_repos'] = user.public_repos
            search_result['success'] = True
        except GithubException as ge:
            search_result['message'] = ge.data['message']
            search_result['success'] = False

        rate_limit = client.get_rate_limit()
        search_result['rate'] = {
            'limit': rate_limit.rate.limit,
            'remaining': rate_limit.rate.remaining,
        }

    return render(request, 'apisumple/github_api.html', {'search_result': search_result})
