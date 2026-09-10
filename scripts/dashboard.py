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
    paper, ink, muted, line = ('#191919','#ededeb','#b0b0ac','#656562') if dark else ('#ededeb','#171717','#52524e','#a1a19b')
    shades = ['#30302e','#686865','#969692','#c2c2bd','#ededeb'] if dark else ['#deded8','#b7b7af','#85857e','#50504a','#171717']
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="840" height="390" viewBox="0 0 840 390" role="img" aria-labelledby="title"><title id="title">GitHub contribution calendar and primary languages of public original repositories</title><rect x=".5" y=".5" width="839" height="389" fill="{paper}" stroke="{line}"/>']
    def text(x,y,value,size=16,color=ink):
        out.append(f'<text x="{x}" y="{y}" fill="{color}" font-family="monospace" font-size="{size}">{html.escape(str(value))}</text>')
    text(24,30,'02 / GITHUB ACTIVITY',16)
    text(526,30,datetime.datetime.now(datetime.timezone.utc).strftime('UPDATED %d %b %Y / UTC').upper(),14,muted)
    out.append(f'<path d="M24 46H816" stroke="{line}"/>')
    calendar=user['contributionsCollection']['contributionCalendar']
    text(24,86,f"{calendar['totalContributions']:,}",30)
    text(155,84,'contributions / past year',16,muted)
    weeks=calendar['weeks']
    for x,week in enumerate(weeks):
        for day in week['contributionDays']:
            date=datetime.date.fromisoformat(day['date']); y=(date.weekday()+1)%7
            n=day['contributionCount']; level=0 if n==0 else 1 if n<4 else 2 if n<9 else 3 if n<16 else 4
            out.append(f'<rect x="{24+x*14.9:.1f}" y="{104+y*12}" width="11.5" height="9" fill="{shades[level]}"><title>{day["date"]}: {n} contributions</title></rect>')
    text(24,210,'Contribution activity over the past 12 months.',14,muted)
    text(650,210,'LESS',9,muted)
    for i,color in enumerate(shades):
        out.append(f'<rect x="{681+i*17}" y="201" width="12" height="10" fill="{color}"/>')
    text(774,210,'MORE',9,muted)
    out.append(f'<path d="M24 230H816" stroke="{line}"/>')
    text(24,257,'PRIMARY LANGUAGES',16)
    text(24,278,'Public original repos, counted once each.',14,muted)
    repos=[r for r in user['repositories']['nodes'] if r['name'] not in ('MirImaadAli1','scuba-vision') and r['primaryLanguage']]
    counts=collections.Counter(r['primaryLanguage']['name'] for r in repos)
    for i,(language,count) in enumerate(counts.most_common()):
        col=i%3; row=i//3; x=24+col*266; y=312+row*44
        text(x,y,language,16); text(x+215,y,str(count),16)
        out.append(f'<rect x="{x}" y="{y+9}" width="230" height="3" fill="{shades[0]}"/><rect x="{x}" y="{y+9}" width="{230*count/len(repos):.1f}" height="3" fill="{ink}"/>')
    out.append('</svg>')
    return ''.join(out)

if __name__ == '__main__':
    user=get_data()
    for theme in ('light','dark'):
        (ROOT/'assets'/f'activity-{theme}.svg').write_text(outline(render(user,theme=='dark')))
