#!/usr/bin/env python3
"""Check navigation, local links, legacy anchors, and API operation references."""
import json,re,sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
errors=[]

def clean(text):
 return re.sub(r'```.*?```|<!--.*?-->','',text,flags=re.S)

def slug(text):
 return re.sub(r'[^\w\s-]','',text.lower()).strip().replace(' ','-')

def anchors(text):
 result=set(re.findall(r'\bid=["\']([^"\']+)',text))
 for h in re.findall(r'^#{1,6}\s+(.+)$',clean(text),re.M):result.add(slug(h))
 return result

pages={str(p.relative_to(ROOT))[:-4]:p.read_text() for p in ROOT.rglob('*.mdx') if not any(x.startswith('.') for x in p.relative_to(ROOT).parts)}
nav=[]
def walk(x):
 if isinstance(x,list):
  for v in x:walk(v)
 elif isinstance(x,dict):
  if 'root' in x:nav.append(x['root'])
  for k,v in x.items():
   if k=='pages':
    for p in v:
     if isinstance(p,str):nav.append(p)
     else:walk(p)
   elif k in ('groups','tabs','dropdowns','anchors','products','versions','global'):walk(v)
walk(json.loads((ROOT/'docs.json').read_text())['navigation'])
for route,n in Counter(nav).items():
 if route not in pages:errors.append(f'Navigation missing page: {route}')
 if n>1:errors.append(f'Duplicate navigation page: {route}')
for route in pages.keys()-set(nav):errors.append(f'Page absent from navigation: {route}')
for route,text in pages.items():
 prose=clean(text)
 links=re.findall(r'\]\((/[^\s)]+)\)',prose)+re.findall(r'\bhref=["\'](/[^"\']+)',prose)
 for link in links:
  target,_,fragment=link.partition('#');target=target.split('?')[0].strip('/')
  if not target:target='introduction'
  if target not in pages:
   if not (ROOT/target).exists():errors.append(f'{route}: missing link {link}')
  elif fragment and fragment not in anchors(pages[target]):errors.append(f'{route}: missing anchor {link}')
 m=re.search(r'^openapi:\s*["\']?(/[^\s]+)\s+(GET|POST|PUT|PATCH|DELETE)\s+([^\s"\']+)',text,re.M)
 if m:
  file,method,path=m.groups()
  try:
   spec=json.loads((ROOT/file.lstrip('/')).read_text())
   if method.lower() not in spec['paths'].get(path,{}):errors.append(f'{route}: operation absent from {file}')
  except Exception as exc:errors.append(f'{route}: {exc}')
legacy=json.loads((ROOT/'scripts/legacy-routes.json').read_text())
for route,ids in legacy.items():
 if route not in pages:errors.append(f'Removed legacy route: {route}');continue
 for id in ids:
  if id not in anchors(pages[route]):errors.append(f'Removed legacy anchor: /{route}#{id}')
for file in (ROOT/'openapi').glob('*.json'):
 spec=json.loads(file.read_text())
 def refs(x):
  if isinstance(x,dict):
   ref=x.get('$ref','')
   if ref.startswith('#/'):
    value=spec
    try:
     for part in ref[2:].split('/'):value=value[part.replace('~1','/').replace('~0','~')]
    except (KeyError,TypeError):errors.append(f'{file.name}: unresolved {ref}')
   for v in x.values():refs(v)
  elif isinstance(x,list):
   for v in x:refs(v)
 refs(spec)
if errors:
 print('\n'.join(sorted(set(errors))));sys.exit(1)
print(f'PASS: {len(pages)} pages, {len(nav)} unique navigation entries, local links, legacy anchors, and API references')
