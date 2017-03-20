import argparse
import requests
import json
import datetime
import calendar


parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description='GitHub Pull Requests Script')
parser.add_argument('user', metavar='user', type=str, nargs='+', help='User for GitHub')
parser.add_argument('repo', nargs='+', type=str, help='Name of GitHub repository')
parser.add_argument('-v', '--version', action='version', version='%(prog)s 2.0')
parser.add_argument('-mcr', metavar='mcr', nargs='?', default=1, help='Basic statistics about merged/closed rate')
parser.add_argument('-atd', metavar='date', type=str, nargs='?', help='''Option to consider only pull requests opened on or after this date. Example: 2017-03-18''')
parser.add_argument('-btd', metavar='date', type=str, nargs='?', help='''Option to consider only pull requests opened before this date. Example: 2017-03-18''')
parser.add_argument('-pr', '--prequest', metavar='prequest', type=int, nargs='?', help='№ of pull request')
parser.add_argument('-o', '--option', metavar='option', type=str, nargs='*', help='''Only these options:
    ndo - Number of days opened
    ncc - Number of comments created.
    dwo - Day of the week opened.
    dwc - Day of the week closed.
    hdo - Hour of the day opened.
    hdc - Hour of the day closed.
    wo - Week opened.
    wc - Week closed.
    uo - User who opened.
    uc - User who closed.
    al - Attached labels.
    nla - Number of lines added.
    nld - Number of lines deleted.
    full - Full statistics with all options.''')

args = parser.parse_args()
args.user = ''.join(str(e) for e in args.user)
args.repo = ''.join(str(e) for e in args.repo)


auth = ('heorhivysotski', 'd5fbd4777c45c7f488b534888d165c093a16165a')
today_date = datetime.date.today()  
today_time = str(datetime.datetime.now().time()).split(':') 
url = 'https://api.github.com/search/issues?q=type:pr+repo:{0}/{1}'.format(args.user, args.repo)
url2 = 'https://api.github.com/repos/{0}/{1}/pulls/{2}.diff'.format(args.user, args.repo, args.prequest)

def pullreq(a, b):
    list = [a, b]
    rate = []
    for i in range(len(list)):
        url1 = (url+'+is:{}').format(list[i])
        R = requests.get(url1, auth=auth)
        if (R.ok):
            repoItem = json.loads(R.text or R.content)
            rate == rate.append(repoItem['total_count'])
        else:
            print('Bad requests')
    print(('The merged/closed rate is {}%').format(int(rate[0] / rate[1] * 100)))

def ndo_func():
    # Number of days opened.
    if repoItem['items'][len(repoItem['items']) - args.prequest]['state'] == 'open':
        opened_date = ((repoItem['items'][len(repoItem['items']) - args.prequest]['created_at']).split('T')[0]).split('-')
        opened_date = datetime.date(int(opened_date[0]), int(opened_date[1]), int(opened_date[2]))
        if opened_date == today_date:
            print('Pull request have been opened today.')
        else:
            print(('Number of days opened is: {} ').format(str(today_date - opened_date).split()[0]))
    else:
        closed_date = ((repoItem['items'][len(repoItem['items']) - args.prequest]['created_at']).split('T')[0]).split('-')
        closed_date = datetime.date(int(closed_date[0]), int(closed_date[1]), int(closed_date[2]))
        print(('The request was closed {}.').format(closed_date))

def ncc_func():
    # Number of comments created.
    print(('Number of created comments is: {}').format(repoItem['items'][len(repoItem['items']) - args.prequest]['comments']))

def dwo_func():
    # Day of the week opened.
    opened_date = ((repoItem['items'][len(repoItem['items']) - args.prequest]['created_at']).split('T')[0]).split('-')
    opened_date = datetime.date(int(opened_date[0]), int(opened_date[1]), int(opened_date[2]))
    print(('Day of the week opened is: {}').format(calendar.day_name[opened_date.weekday()]))

def dwc_func():
    # Day of the week closed.
    if repoItem['items'][len(repoItem['items']) - args.prequest]['state'] == 'closed':
        closed_date = ((repoItem['items'][len(repoItem['items']) - args.prequest]['closed_at']).split('T')[0]).split('-')
        closed_date = datetime.date(int(closed_date[0]), int(closed_date[1]), int(closed_date[2]))
        print(('Day of the week closed is: {} ').format(calendar.day_name[closed_date.weekday()]))
    else:
        print('The request is still opened.')

def hdo_func():
    # Hour of the day opened.
    if repoItem['items'][len(repoItem['items']) - args.prequest]['state'] == 'open':
        if (repoItem['items'][len(repoItem['items']) - args.prequest]['created_at']).split('T')[0] == str(datetime.date.today()):
            opened_time = (repoItem['items'][len(repoItem['items']) - args.prequest]['created_at']).split('T')[1].split('Z')[0]
            print(('Pull request was opened at {}').format(opened_time))
        else:
            print('The pull request is opened more then 1 day.')
    else:
        print('The pull request was closed.')

def hdc_func():
    # Hour of the day closed.
    if repoItem['items'][len(repoItem['items']) - args.prequest]['state'] == 'closed':
        if (repoItem['items'][len(repoItem['items']) - args.prequest]['closed_at']).split('T')[0] == str(datetime.date.today()):
            opened_time = ((repoItem['items'][len(repoItem['items']) - args.prequest]['closed_at']).split('T')[1]).split('Z')[0].split(':')
            opened_time = str(datetime.time(int(opened_time[0]), int(opened_time[1]), int(opened_time[2]))).split(':')
            print(('Pull request was closed at {}').format(int(opened_time[0])))
        else:
            print('The pull request was closed more then 1 day ago.')
    else:
        print('The pull request is still opened.')

def wo_func():
    # Week opened.
    opened_date = ((repoItem['items'][len(repoItem['items']) - args.prequest]['created_at']).split('T')[0]).split('-')
    opened_date = datetime.date(int(opened_date[0]), int(opened_date[1]), int(opened_date[2]))
    print(('The pull request was opened on {}th week ').format(opened_date.isocalendar()[1]))

def wc_func():
    # Week closed.
    if repoItem['items'][len(repoItem['items']) - args.prequest]['state'] == 'open':
        print('The pull request still opened.')
    else:
        closed_date = ((repoItem['items'][len(repoItem['items']) - args.prequest]['closed_at']).split('T')[0]).split('-')
        closed_date = datetime.date(int(closed_date[0]), int(closed_date[1]), int(closed_date[2]))
        print(('The pull request was closed on {}th week ').format(closed_date.isocalendar()[1]))

def uo_func():
    # User who open.
    user = ((repoItem['items'][len(repoItem['items']) - args.prequest]['user']['login']))
    print(('User who opened pull request - {}').format(user))

def al_func():
    # Attached labels.
    if len(repoItem['items'][len(repoItem['items']) - args.prequest]['labels'])>0:
        for i in range(len(repoItem['items'][len(repoItem['items']) - args.prequest]['labels'])):
            label = ((repoItem['items'][len(repoItem['items']) - args.prequest]['labels'][i]['name']))
            print(('The label {}: {}').format(i + 1, label), end='\n')
    else:
        print('Pull request does not have any labels.')

def nla_func():
    # Number of lines added.
    print('Number of lines added - {}'.format(repoItem2['additions']))
def nld_func():
    # Number of lines deleted.
    print('Number of lines deleted - {}'.format(repoItem2['deletions']))


if args.mcr==None:
    # Getting basic statistics about merged/closed rate.
    pullreq('merged', 'closed')

elif args.prequest:
    R = requests.get(url, auth=auth)
    R2 = requests.get(url2, auth=auth)
    if (R.ok) and (R2.ok):
        repoItem = json.loads(R.text or R.content)
        repoItem2 = json.loads(R2.text or R2.content)
        if len(repoItem['items']) >= args.prequest:
            if args.option:
                args.option = ''.join(str(e) for e in args.option)
                if 'ndo' in args.option:
                    ndo_func()
                if 'ncc' in args.option:
                    ncc_func()
                if 'dwo' in args.option:
                    dwo_func()
                if 'dwc' in args.option:
                    dwc_func()
                if 'hdo' in args.option:
                    hdo_func()
                if 'hdc' in args.option:
                    hdc_func()
                if 'wo' in args.option:
                    wo_func()
                if 'wc' in args.option:
                    wc_func()
                if 'uo' in args.option:
                    uo_func()
                if 'al' in args.option:
                    al_func()
                if 'nla' in args.option:
                    nla_func()
                if 'nld' in args.option:
                    nld_func()
                if 'full' in args.option:
                    print('Pull request {} '.format(args.prequest))
                    ndo_func()
                    ncc_func()
                    dwo_func()
                    dwc_func()
                    hdo_func()
                    hdc_func()
                    wo_func()
                    wc_func()
                    uo_func()
                    al_func()
                    nla_func()
                    nld_func()
            else:
                print(' Pull request № {} Choose some option.'.format(args.prequest))

        else:
            print('Do not have such pull request')
    else:
        print('Bad requests')

elif args.atd:
    # Getting full statistic about all requests, which was created on or after this date.
    url = 'https://api.github.com/search/issues?q=type:pr+repo:{0}/{1}+created:>={2}'.format(args.user, args.repo, args.atd)
    R = requests.get(url, auth=auth)
    if (R.ok):
        repoItem = json.loads(R.text or R.content)
        for i in range(len(repoItem['items'])):
            args.prequest = i + 1
            url2 = 'https://api.github.com/repos/{0}/{1}/pulls/{2}.diff'.format(args.user, args.repo, i + 1)
            R2 = requests.get(url2, auth=auth)
            repoItem2 = json.loads(R2.text or R2.content)
            print('''Pull request'''.format(i + 1))
            ndo_func()
            ncc_func()
            dwo_func()
            dwc_func()
            hdo_func()
            hdc_func()
            wo_func()
            wc_func()
            uo_func()
            al_func()
            nla_func()
            nld_func()
elif args.btd:
    # Getting full statistic about all requests, which was created before this date.
    url = 'https://api.github.com/search/issues?q=type:pr+repo:{0}/{1}+created:<{2}'.format(args.user, args.repo, args.btd)
    R = requests.get(url, auth=auth)
    if (R.ok):
        repoItem = json.loads(R.text or R.content)
        for i in range(len(repoItem['items'])):
            args.prequest = i + 1
            url2 = 'https://api.github.com/repos/{0}/{1}/pulls/{2}.diff'.format(args.user, args.repo, i + 1)
            R2 = requests.get(url2, auth=auth)
            repoItem2 = json.loads(R2.text or R2.content)
            print('''Pull request'''.format(i + 1))
            ndo_func()
            ncc_func()
            dwo_func()
            dwc_func()
            hdo_func()
            hdc_func()
            wo_func()
            wc_func()
            uo_func()
            al_func()
            nla_func()
            nld_func()

else:
    R = requests.get(url, auth=auth)
    if (R.ok):
        repoItem = json.loads(R.text or R.content)
        for i in range(len(repoItem['items'])):
            args.prequest = i+1
            url2 = 'https://api.github.com/repos/{0}/{1}/pulls/{2}.diff'.format(args.user, args.repo, i+1)
            R2 = requests.get(url2, auth=auth)
            repoItem2 = json.loads(R2.text or R2.content)
            print('''Pull request {}'''.format(i+1))
            ndo_func()
            ncc_func()
            dwo_func()
            dwc_func()
            hdo_func()
            hdc_func()
            wo_func()
            wc_func()
            uo_func()
            al_func()
            nla_func()
            nld_func()


