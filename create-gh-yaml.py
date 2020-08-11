from requests import get
from hashlib import sha256
import yaml

org,repo,name,user = 'cli','cli','gh','jph00'

repo_d = get(f'https://api.github.com/repos/{org}/{repo}').json()
desc,url = repo_d['description'],repo_d['html_url']
rels = get(f'https://api.github.com/repos/{org}/{repo}/releases/latest').json()
ver = rels['name'][1:]

rels_d = dict(linux64 = 'linux_amd64',
              linux32 = 'linux_386',
              osx = 'macOS_amd64')

def get_source(plat, pre):
    download = next(o for o in rels['assets']
                    if o['name'].endswith(f'{pre}.tar.gz'))['browser_download_url']
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

lic = repo_d['license']

d2 = {
    'build': {'number': 0, 'binary_relocation': False,
              'script': 'cp -r bin share $PREFIX/'},
    'test': {'commands': ['gh --help']},
    'about': {
        'license': lic['name'],
        'license_family': lic['spdx_id'],
        'home': url, 'doc_url': url, 'dev_url': url
    },
    'extra': {'recipe-maintainers': [user]}
}

yaml.SafeDumper.ignore_aliases = lambda *args : True
with open(f'{name}/meta.yaml','w') as f:
    f.write(d1)
    yaml.safe_dump(d2, f)

