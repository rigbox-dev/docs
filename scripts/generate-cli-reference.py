#!/usr/bin/env python3
"""Render offline Clap export. Regenerate: python3 scripts/generate-cli-reference.py.
Pass --source exported.json to adopt an export, --check to detect generated drift.
Curated prose/examples live in cli-reference/command-notes.json and are never overwritten.
"""
import argparse, html, json, pathlib, shlex, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--source', type=pathlib.Path)
p.add_argument('--check', action='store_true')
a=p.parse_args()
source_path=ROOT/'cli-reference/command-surface.json'
surface=json.loads((a.source or source_path).read_text())
notes=json.loads((ROOT/'cli-reference/command-notes.json').read_text())
commands={}
for mode in ('local','workspace'):
    for cmd in surface[mode]:
        if cmd['path']:
            key='/'.join(cmd['path'])
            commands.setdefault(key,{})[mode]=cmd
missing=set(commands)-set(notes)
if missing or any(not notes[k].get('examples') for k in commands if k in notes):
    sys.exit('Missing curated examples: '+', '.join(sorted(missing or {k for k in commands if not notes[k].get('examples')})))
def escaped(value):
    return html.escape(str(value)).replace('{','&#123;').replace('}','&#125;').replace('|','&#124;').replace('\n','<br />')
def inline(value): return '`'+str(value).replace('`','').replace('|','&#124;')+'`'
outputs={}
if a.source: outputs[source_path]=json.dumps(surface,indent=2)+'\n'
for key,modes in sorted(commands.items()):
    cmd=next(iter(modes.values())); title='rig '+' '.join(cmd['path'])
    out=['---','title: '+json.dumps(title),'sidebarTitle: '+json.dumps(cmd['path'][-1]),'description: '+json.dumps((cmd['about'] or title).split('\n')[0]),'---','',f'Available **'+ ' and '.join(modes)+'**. Reference source: CLI `'+surface['version']+'` (`'+surface['revision'][:12]+'`).','',notes[key].get('description',''),'','## Examples','']
    if notes[key].get('warning'):
        out += ['<Warning>', notes[key]['warning'], '</Warning>', '']
    for ex in notes[key]['examples']:
        out += [ex['description'],'','```bash',ex['command'],'```','']
    aliases=cmd['aliases']
    if aliases: out+=['Aliases: '+', '.join('['+x+'](/cli-reference/commands/'+key+')' for x in aliases)+'.','']
    for mode,c in modes.items():
        out+=['## '+mode.title()+' syntax','','```text',c['usage'],'```','','### Arguments and flags','','| Argument | Description | Details |','| --- | --- | --- |']
        for arg in c['arguments']:
            label=', '.join(value for value in [('-'+arg['short']) if arg['short'] else '', ('--'+arg['long']) if arg['long'] else ''] if value) or arg['id']
            details=[]
            if arg['required']: details.append('Required')
            if arg['global']: details.append('Global')
            if arg['value_names'] and arg.get('num_args', {}).get('max', 0) > 0: details.append('Value: '+', '.join(arg['value_names']))
            if arg['defaults']: details.append('Default: '+', '.join(arg['defaults']))
            if arg['values']: details.append('Choices: '+', '.join(arg['values']))
            if arg['aliases']: details.append('Aliases: '+', '.join(arg['aliases']))
            if arg['conflicts']: details.append('Conflicts: '+', '.join(arg['conflicts']))
            out.append('| '+inline(label)+' | '+escaped(arg['help'] or '')+' | '+escaped('; '.join(details))+' |')
        out+=['','<Accordion title="Complete command help">','','```text',c['help'].rstrip(),'```','','</Accordion>','']
    children=[x for x in commands if x.startswith(key+'/') and x.count('/')==key.count('/')+1]
    if children: out+=['## Subcommands','']+['- ['+x.split('/')[-1]+'](/cli-reference/commands/'+x+')' for x in sorted(children)]+['']
    outputs[ROOT/'cli-reference/commands'/f'{key}.mdx']='\n'.join(out)
def tree(prefix=''):
    result=[]
    for k in sorted(commands):
        if ('/' not in k if not prefix else k.startswith(prefix+'/') and k.count('/')==prefix.count('/')+1):
            children=tree(k); route='cli-reference/commands/'+k
            result.append({'group':k.split('/')[-1],'root':route,'pages':children} if children else route)
    return result
outputs[ROOT/'scripts/cli-navigation.json']=json.dumps(tree(),indent=2)+'\n'
samples=[]
for key,modes in sorted(commands.items()):
    mode=next(iter(modes))
    for index,example in enumerate(notes[key]['examples']):
        samples.append({'key':key+':'+str(index),'mode':mode,'argv':shlex.split(example['command'])})
outputs[ROOT/'scripts/cli-examples.json']=json.dumps(samples,indent=2)+'\n'
stale=set((ROOT/'cli-reference/commands').rglob('*.mdx'))-set(outputs)
fail=[]
for path,content in outputs.items():
    if a.check:
        if not path.exists() or path.read_text()!=content: fail.append(str(path.relative_to(ROOT)))
    else:
        path.parent.mkdir(parents=True,exist_ok=True); path.write_text(content)
if a.check and (fail or stale): sys.exit('Generated CLI drift: '+', '.join(fail+[str(x.relative_to(ROOT)) for x in stale]))
if not a.check:
    for path in stale: path.unlink()
print(f'{len(commands)} command pages verified' if a.check else f'Generated {len(commands)} command pages')
