"""Generate monochrome profile panels from GitHub's public account data."""
from roboto import outline
import collections
import datetime
import html
import json
import os
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
QUERY = '''query { user(login:"MirImaadAli1") { contributionsCollection { contributionCalendar { totalContributions weeks { contributionDays { contributionCount date } } } } repositories(first:100,ownerAffiliations:OWNER,privacy:PUBLIC,isFork:false) { nodes { name url description primaryLanguage { name } stargazerCount updatedAt } } } }'''

def get_data():
    fixture = os.environ.get('PROFILE_DATA_FILE')
    if fixture:
        result = json.loads(Path(fixture).read_text())
    else:
        request = urllib.request.Request('https://api.github.com/graphql', data=json.dumps({'query': QUERY}).encode(), headers={'Authorization': 'Bearer ' + os.environ['GITHUB_TOKEN'], 'Content-Type': 'application/json', 'User-Agent': 'imaad-profile-dashboard'})
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.load(response)
    if result.get('errors'):
        raise RuntimeError(result['errors'])
    return result['data']['user']

def render(user, dark):
    paper, ink, muted, line = ('#191919','#ffffff','#ededeb','#858581') if dark else ('#ededeb','#111111','#242424','#777773')
    shades = ['#333333','#6a6a6a','#999999','#cccccc','#ffffff'] if dark else ['#d5d5cf','#a4a49e','#72726c','#42423e','#111111']
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="840" height="540" viewBox="0 0 840 540" role="img"><title>GitHub activity and repository languages</title><rect width="840" height="540" fill="{paper}"/><path d="M.5 0V540M839.5 0V540" stroke="{line}"/>']
    def text(x,y,value,size=20,color=ink):
        out.append(f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial, Helvetica, sans-serif" font-size="{size}">{html.escape(str(value))}</text>')
    text(28,40,'02 / GITHUB ACTIVITY',20)
    text(28,78,datetime.datetime.now(datetime.timezone.utc).strftime('Updated %d %b %Y / UTC'),18)
    calendar=user['contributionsCollection']['contributionCalendar']
    text(28,139,f"{calendar['totalContributions']:,}",42)
    text(185,137,'contributions in the past year',22)
    for x,week in enumerate(calendar['weeks']):
        for day in week['contributionDays']:
            date=datetime.date.fromisoformat(day['date']); y=(date.weekday()+1)%7
            n=day['contributionCount']; level=0 if n==0 else 1 if n<4 else 2 if n<9 else 3 if n<16 else 4
            out.append(f'<rect x="{28+x*14.7:.1f}" y="{165+y*15}" width="11.5" height="12" fill="{shades[level]}"><title>{day["date"]}: {n} contributions</title></rect>')
    text(28,305,'GitHub contribution data. Refreshed daily.',18)
    text(632,305,'Less',17)
    for i,color in enumerate(shades):
        out.append(f'<rect x="{674+i*18}" y="290" width="13" height="14" fill="{color}"/>')
    text(770,305,'More',17)
    out.append(f'<path d="M28 332H812" stroke="{line}"/>')
    text(28,370,'PRIMARY LANGUAGES',20)
    text(28,404,'Main language of each public original repo; not code volume.',20)
    repos=[r for r in user['repositories']['nodes'] if r['name'] not in ('MirImaadAli1','scuba-vision') and r['primaryLanguage']]
    counts=collections.Counter(r['primaryLanguage']['name'] for r in repos)
    for i,(language,count) in enumerate(counts.most_common()):
        col=i%3; row=i//3; x=28+col*264; y=448+row*56
        text(x,y,language,20); text(x+218,y,str(count),20)
        out.append(f'<rect x="{x}" y="{y+12}" width="236" height="5" fill="{shades[0]}"/><rect x="{x}" y="{y+12}" width="{236*count/len(repos):.1f}" height="5" fill="{ink}"/>')
    out.append('</svg>')
    return ''.join(out)

if __name__ == '__main__':
    user=get_data()
    for theme in ('light','dark'):
        (ROOT/'assets'/f'activity-{theme}.svg').write_text(outline(render(user,theme=='dark')))
