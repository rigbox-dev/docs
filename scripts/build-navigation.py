#!/usr/bin/env python3
"""Build the curated native Mintlify navigation with the generated CLI tree."""
import argparse
import json
from pathlib import Path

def group(label,pages,root=None):
 result={'group':label,'pages':pages}
 if root:result.update(root=root,expanded=False)
 return result

def area(label,pages):
 icons={'Start here':'flag','Deploy applications':'rocket','Configure applications':'sliders','Workspaces and storage':'server','AI and tools':'robot','Operate and troubleshoot':'wrench','Examples':'flask','CLI reference':'terminal','Build on Rigbox':'code'}
 return {'dropdown':label,'icon':icons[label],'groups':pages}

j=json.loads(Path('docs.json').read_text())
old=j['navigation']['tabs'][1]
if Path('scripts/api-navigation-base.json').exists():original=json.loads(Path('scripts/api-navigation-base.json').read_text())
else:
 original=old['groups'];Path('scripts/api-navigation-base.json').write_text(json.dumps(original,indent=2)+'\n')
api={g['group']:g for g in original}
areas=[
area('Start here',[group('Get started',['introduction','quickstart','guides/install-cli','concepts/core'])]),
area('Deploy applications',[
 group('Deploy',['deploy/overview','guides/deploying',group('GitHub',['guides/github-actions','guides/deploy-button'],'guides/github'),group('Multi-app projects',['deploy/dependencies','deploy/single-app'],'deploy/multi-app')]),
 group('App releases',['deploy/development-loop','deploy/stage-and-activate','deploy/app-rollback']),
 group('Workspace images',[group('Reproducible builds',['deploy/build-cache','deploy/reimage','guides/releases-and-rollback'],'deploy/reproducible-builds'),'guides/bluegreen'])]),
area('Configure applications',[
 group('Configuration',['configure/overview','configure/environment','configure/secrets','configure/parameters','configure/commands','configure/health']),
 group('Networking',['guides/visibility','guides/expose-and-route','guides/custom-domains']),
 group('Manifest reference',[group('rig.yaml',['reference/rig-yaml/application','reference/rig-yaml/workspace','reference/rig-yaml/source','reference/rig-yaml/configuration','reference/rig-yaml/deployment'],'reference/rig-yaml')])]),
area('Workspaces and storage',[
 group('Workspaces',['workspaces/overview','guides/workspaces','concepts/limits',group('SSH',['workspaces/ssh-keys','workspaces/file-transfer'],'guides/ssh-access'),'guides/images-and-templates']),
 group('Storage',[group('Persistent volumes',['workspaces/volume-management'],'guides/persistent-volumes'),group('Snapshots',['workspaces/snapshot-restore','workspaces/recovery-limits'],'guides/snapshots')]),
 group('Environment',['guides/workspace-services','guides/setup-scripts','guides/service-specs'])]),
area('AI and tools',[
 group('AI',['ai/overview','guides/ai-coding-tools','guides/managed-proxy','guides/byok']),
 group('Tools',['guides/catalog','ai/spawn','guides/virtual-browser','guides/firecrawl','guides/architecture-explorer'])]),
area('Operate and troubleshoot',[
 group('Observe',['operate/overview','operate/app-logs','operate/build-logs','operate/telemetry']),
 group('Troubleshoot',['operate/health','operate/deployment','operate/github','operate/ssh','operate/resources','operate/storage'])]),
area('Examples',[
 group('Build an app',['examples/overview','examples/first-app','examples/frontend-api','examples/ai-chat','examples/webhook','examples/background-worker','examples/persistent-notes','examples/parameters']),
 group('Environments',['examples/bluegreen','examples/self-hosted','examples/catalog'])]),
area('CLI reference',[
 group('Use the CLI',['cli-reference/cli','cli-reference/authentication','guides/using-cli','cli-reference/configuration','cli-reference/execution-modes'])]),
area('Build on Rigbox',[
 group('Integrate',['build/overview','build/quickstart','build/workspace-lifecycle','build/deploy-monitor','guides/build-hosting-platform','build/api-conventions']),
 group('Platform',['concepts/architecture','concepts/security']),
 group('First-party integrations',['sandbox-api-surface','clawd-api-surface','clawd-runtime-services'])])]
api_groups=[group('Start',['api-reference/overview']),group('Access',[api['API Keys'],api['Access Control']]),group('Workspaces',[api['Workspaces'],api['Workspace Services'],api['SSH Keys']]),group('Applications and releases',[api['Apps'],api['App Logs'],group('App releases',[f'api-reference/app-releases/{x}' for x in ['list','create','get','activate','logs']])]),group('Storage',[api['Snapshots']]),group('AI and tools',[api['AI'],api['Managed Proxy'],api['Tools']]),group('Registry',[api['App Catalog'],api['Templates'],api['Setup Scripts'],api['Service Specs']]),group('Account and platform',[api['User Settings'],api['Roadmap'],api['System']])]
extra=Path('scripts/deployment-api-navigation.json')
if extra.exists():
 for name,pages in json.loads(extra.read_text())['groups'].items():
  if not pages:continue
  entry=group(name.title(),pages)
  if name=='volumes':api_groups[4]['pages'].append(entry)
  else:api_groups.insert(4,entry)
j['navigation']['tabs']=[{'tab':'Docs','groups':[group(a['dropdown'],[page for section in a['groups'] for page in section['pages']]) for a in areas]},{'tab':'API Reference','groups':api_groups}]
j['styling']={'eyebrows':'breadcrumbs'};j['interaction']={'drilldown':False}
# Mintlify group roots navigate when expanded. Put the overview inside each
# group so expanding a branch is distinct from opening a page.
def separate_overviews(node):
 if isinstance(node,dict):
  if 'root' in node:
   node['pages'].insert(0,node.pop('root'))
   node['expanded']=False
  for value in node.values():separate_overviews(value)
 elif isinstance(node,list):
  for value in node:separate_overviews(value)
separate_overviews(j['navigation'])
parser=argparse.ArgumentParser()
parser.add_argument('--check',action='store_true')
args=parser.parse_args()
rendered=json.dumps(j,indent=2)+'\n'
if args.check:
 if Path('docs.json').read_text()!=rendered:
  raise SystemExit('Navigation drift: run python3 scripts/build-navigation.py')
 print('PASS: navigation matches curated and generated trees')
else:Path('docs.json').write_text(rendered)
