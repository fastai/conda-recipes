from requests import get
from hashlib import sha256
import yaml
from pathlib import Path

org,repo,name,user = 'jsoftware','jsource','j','jph00'
path = Path(name)
path.mkdir(exist_ok=True)

repo_d = get(f'https://api.github.com/repos/{org}/{repo}').json()
desc,url = repo_d['description'],repo_d['html_url']
ver = '9.01'
rels_d = dict(linux = 'linux', osx = 'mac')

def get_source(plat, pre):
    download = f'https://files.fast.ai/files/j901-{pre}.tgz'
    h = sha256(get(download).content).hexdigest()
    spec =  f' # [{plat}]'
    return f'  url: {download}{spec}\n  sha256: {h}{spec}\n'

sources = [get_source(*p) for p in rels_d.items()]

# Work around conda build bug - 'package' and 'source' must be first
d1 = f'''package:
  name: {name}
  version: {ver}

source:
{"".join(sources)}'''

script = f'''mkdir -p $PREFIX/share/j901
mkdir $PREFIX/bin
mv * $PREFIX/share/j901
ln -s $PREFIX/share/j901/bin/jconsole $PREFIX/bin/'''

d2 = {
    'build': {'number': 0, 'binary_relocation': False, 'script': script},
    'test': {'commands': ['jconsole -js "exit 0"']},
    'about': {
        'license': 'GPL3', 'license_family': 'GPL3',
        'home': url, 'doc_url': url, 'dev_url': url
    },
    'extra': {'recipe-maintainers': [user]}
}

yaml.SafeDumper.ignore_aliases = lambda *args : True
with (path/'meta.yaml').open('w') as f:
    f.write(d1)
    yaml.safe_dump(d2, f)

