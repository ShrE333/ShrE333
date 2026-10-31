"""Render a truthful, visual GitHub profile. Pure stdlib. Invoked by GitHub Actions.

The script uses the authenticated GitHub REST/GraphQL APIs. If GraphQL contributions
aren't accessible, it renders an explicit unavailable state rather than guessing.
"""
import json, os, sys, urllib.request, urllib.error, math, datetime
from collections import Counter
from html import escape
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]/'assets'
USER=os.getenv('PROFILE_USER','ShrE333')
TOKEN=os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN','')
INK='#242521'; PAPER='#F2F0E8'; ORANGE='#EA5A36'; MUTED='#6A655B'; YELLOW='#F0C968'; GREEN='#C6DFCE'; BLUE='#B8D0E7'
def txt(x,y,t,size=21,color=INK,weight=700,anchor=None):
 return f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" font-weight="{weight}"'+(f' text-anchor="{anchor}"' if anchor else '')+'>'+escape(str(t))+'</text>'
def svg(width,height,inner):
 return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img"><rect width="{width}" height="{height}" fill="{PAPER}"/><rect width="{width}" height="9" fill="{ORANGE}"/>'+inner+'</svg>'
def fetch(url, payload=None):
 headers={'Accept':'application/vnd.github+json','User-Agent':'ShrE333-profile-illustration','X-GitHub-Api-Version':'2022-11-28'}
 if TOKEN:headers['Authorization']='Bearer '+TOKEN
 data=json.dumps(payload).encode() if payload else None
 if data: headers['Content-Type']='application/json'
 req=urllib.request.Request(url,data=data,headers=headers)
 with urllib.request.urlopen(req,timeout=25) as r:return json.loads(r.read())
def repos_data():
 repos=[]
 for page in range(1,16):
  batch=fetch(f'https://api.github.com/users/{USER}/repos?type=owner&per_page=100&page={page}')
  if not isinstance(batch,list):raise RuntimeError('Unexpected repository response')
  repos.extend([r for r in batch if not r.get('fork',False) and not r.get('private',False)])
  if len(batch)<100:break
 counts=Counter()
 for r in repos:
  if r.get('language'):counts[r['language']]+=1
 return repos,counts

def contribution_data():
 query='query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount weekday}}}}}}'
 payload=fetch('https://api.github.com/graphql',{'query':query,'variables':{'login':USER}})
 if payload.get('errors'):raise RuntimeError(str(payload['errors'])[:300])
 c=payload['data']['user']['contributionsCollection']['contributionCalendar']
 return c['totalContributions'],c['weeks']

def activity(repos=None,counts=None,total=None,issue=None):
 s=[txt(45,67,'GITHUB, WITHOUT THE GUESSWORK.',41,INK,900),txt(45,97,'PUBLIC REPOSITORIES / ACTUAL ACTIVITY / LIVE DATA',16,MUTED,700)]
 if repos is None:
  s +=[f'<rect x="45" y="135" width="1110" height="238" rx="12" fill="{GREEN}" stroke="{INK}" stroke-width="2"/>',txt(74,217,'AWAITING FIRST SYNC',42,INK,900),txt(74,255,'Run the “Refresh profile stats” workflow once.',21,INK,600),txt(74,289,'This space fills with real public GitHub metrics.',19,MUTED,500)]
 else:
  rcount=len(repos);stars=sum(int(r.get('stargazers_count') or 0) for r in repos)
  for i,(n,label) in enumerate([(str(rcount),'PUBLIC REPOS'),(str(stars),'REPO STARS'),(str(total) if total is not None else 'N/A','YEARLY CONTRIBUTIONS')]):
   x=45+i*377
   s +=[f'<rect x="{x}" y="132" width="355" height="150" rx="8" fill="{[GREEN,YELLOW,BLUE][i]}" stroke="{INK}" stroke-width="2"/>',txt(x+24,204,n,54,INK,900),txt(x+24,245,label,16,INK,800)]
  s +=[txt(46,329,'LANGUAGES ACROSS PUBLIC REPOS',23,INK,900)]
  top=counts.most_common(6);maxval=max((v for _,v in top),default=1)
  for i,(name,n) in enumerate(top):
   x=45+(i%3)*378;y=351+(i//3)*78
   s +=[txt(x,y+16,name.upper(),16,INK,800),txt(x+330,y+16,str(n)+' REPOS',13,MUTED,700,'end'),f'<rect x="{x}" y="{y+28}" width="330" height="15" fill="#D3D0C8"/>',f'<rect x="{x}" y="{y+28}" width="{max(2,round(330*n/maxval))}" height="15" fill="{ORANGE}"/>']
  if not top:s.append(txt(45,391,'No public repository language labels returned.',19,MUTED,600))
 if issue:s.append(txt(44,516,'Some live data was unavailable; no values were invented.',15,ORANGE,700))
 s +=[f'<rect x="0" y="540" width="1200" height="40" fill="{INK}"/>',txt(45,566,'AUTOMATICALLY GENERATED / SOURCE: GITHUB API',14,PAPER,700),txt(1150,566,'NOT A SKILL SCORE',14,YELLOW,800,'end')]
 (BASE/'activity.svg').write_text(svg(1200,580,''.join(s)),encoding='utf-8')

def skyline(weeks=None,total=None):
 s=[txt(44,67,'A YEAR, ONE LITTLE BLOCK AT A TIME.',37,INK,900),txt(45,101,'52 WEEKS OF SHOWING UP. SOME QUIET. SOME CHAOTIC.',16,MUTED,700)]
 if not weeks:
  s +=[f'<rect x="45" y="138" width="1110" height="270" rx="10" fill="{BLUE}" stroke="{INK}" stroke-width="2"/>',txt(80,250,'AWAITING FIRST SYNC',36,INK,900),txt(80,288,'Contribution skyline appears after the first workflow run.',20,INK,600)]
 else:
  # Each week is a lane; seven cells per lane. Bars are 3D-ish blocks, shaded by count.
  days=[]
  for week in weeks:
   d={int(day['weekday']):int(day['contributionCount']) for day in week['contributionDays']}
   days.append([d.get(i,0) for i in range(7)])
  if len(days)>53:days=days[-53:]
  n=len(days);dx=min(19.1,1020/max(1,n));dy=28
  for wi,daycounts in enumerate(days):
   for day,cnt in enumerate(daycounts):
    x=68+wi*dx;y=210+day*dy
    h=min(58,5+int(11*math.log2(cnt+1))) if cnt else 0
    color=('#DEDACF' if cnt==0 else '#F1CBA7' if cnt<3 else '#E99868' if cnt<7 else ORANGE)
    s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{dx-2:.1f}" height="13" rx="2" fill="{color}"/>')
    if h:
     s +=[f'<path d="M{x:.1f} {y:.1f} l4 -4 h{dx-2:.1f} l-4 4 Z" fill="#F4BE7A"/>',f'<rect x="{x:.1f}" y="{y-h:.1f}" width="{dx-2:.1f}" height="{h:.1f}" fill="{color}"/>',f'<path d="M{x+dx-2:.1f} {y-h:.1f} l4 -4 v{h:.1f} l-4 4Z" fill="#B84C2E"/>']
  s +=[txt(45,458,f'{total} CONTRIBUTIONS' if total is not None else 'CONTRIBUTIONS UNAVAILABLE',27,INK,900),txt(1152,458,'LAST 12 MONTHS / PUBLIC GITHUB CALENDAR',15,MUTED,700,'end')]
 s +=[f'<rect x="0" y="484" width="1200" height="36" fill="{INK}"/>',txt(45,508,'EACH BLOCK = ONE DAY. HEIGHT = ACTIVITY, NOT QUALITY.',13,PAPER,700)]
 (BASE/'contributions.svg').write_text(svg(1200,520,''.join(s)),encoding='utf-8')

if __name__=='__main__':
 if '--placeholder' in sys.argv:
  activity();skyline();sys.exit(0)
 repos=counts=None;total=weeks=None;errors=[]
 try:repos,counts=repos_data()
 except Exception as e: errors.append('REST: '+str(e))
 try:total,weeks=contribution_data()
 except Exception as e: errors.append('GraphQL: '+str(e))
 activity(repos,counts,total,errors)
 skyline(weeks,total)
 print('repos',len(repos) if repos is not None else None,'contributions',total,'errors',errors)
 if repos is None and weeks is None: sys.exit('GitHub data unavailable; not overwriting metrics with made-up numbers.')
