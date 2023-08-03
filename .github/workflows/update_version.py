import sys,re


def patch_init(v):
    file="vbuild/__init__.py"
    content = re.sub(r'__version__ = [^#]*',f'__version__ = "{v}" ',open(file,'r+').read(),1)
    assert v in content
    with open(file,'w+') as fid:
        fid.write( content )
    return file

def patch_pyproject(v):
    file="pyproject.toml"
    content = re.sub(r'version = [^#]*',f'version = "{v}" ',open(file,'r+').read(),1)
    assert v in content
    with open(file,'w+') as fid:
        fid.write( content )
    return file

if __name__=="__main__":
    v=sys.argv[1]
    assert v.lower().startswith("v"), "version should start with 'v' (was '%s')" %v
    assert v.count(".")==2, "version is not semver (was '%s')" %v
    version=v[1:] # remove 'v'
    f1=patch_init(version)
    f2=patch_pyproject(version)
    print(f"Files '{f1}' & '{f2}' updated to version '{version}' !")