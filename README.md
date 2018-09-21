# vbuild

"Compile" your [VUEJS](https://vuejs.org/) [component (*.vue)](https://fr.vuejs.org/v2/guide/single-file-components.html) to standalone html/js/css ... python only (no need of nodejs)

It's just an utility to extract HTML(template), SCRIPT and STYLE from a VUE/SFC component (*.vue).
It's PURE python (py2 & py3 compatible), no nodejs !

```python
import vbuild

sfc=vbuild.VBuild("mycompo.vue")
print( sfc.html )
print( sfc.script )
print( sfc.style )
```

or

```python
import vbuild

ll=[]
ll.append( vbuild.VBuild("c1.vue") )
ll.append( vbuild.VBuild("c2.vue") )

s=sum(ll)

print( s.html )
print( s.script )
print( s.style )
```

and a VBuild is pick'able !

**Notes:**

 * Minimum component needs the `<template></template>` tags
 * Only one `<style></style>` tags !
 * `Style` are SCOPED only (just style the component, you can't style others things)
 * styles are minimized (remove comments and spaces)
 * JS is not minimized, and not babeled ! (but you can easily send it thru an online service for that)
 * `templates` are converted to a `<script type="text/x-template" id="XXX"></script>` (not converted to JS)

Its main purpose is to let you use components (.vue files) in your vuejs app, without a full nodejs stack. It's up to you to create your generator, to extract the things, and create your "index.html" file. (it's a 5 lines of python code), example:

```python
import vbuild,glob
r=sum([vbuild.VBuild(i) for i in glob.glob("*.vue")+glob.glob("*/*.vue")))
buf=readYourTemplate("index.tpl") # should contains a tag "<!-- HERE -->" that would be substitued
buf=buf.replace("<!-- HERE -->",str(r))
writeYourTemplate("index.html",buf)
```

Hope it could help ...

