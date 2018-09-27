# vbuild

"Compile" your [VUEJS](https://vuejs.org/) [component (*.vue)](https://fr.vuejs.org/v2/guide/single-file-components.html) to standalone html/js/css ... python only (no need of nodejs). BTW it provides a js-minimizer (es2015 compliant code)

It's just an utility to extract HTML(template), SCRIPT and STYLE from a VUE/SFC component (*.vue).
It's PURE python (py2 & py3 compatible), no nodejs ! It's fully unitested (100% !)

It won't replace webpack/nodejs/vue-cli, it fills the _"Sometimes you have to work with the tools you have, not the ones you want."_ gap.

[Available on pypi](https://pypi.org/project/vbuild/)

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

By the way, the module provide a js-minimizer (to generate ES2015 compliant) (thru on the [clojure online service](https://closure-compiler.appspot.com))

```python
js="""async function  mymethod(...a) {
    var f=(...a) => {let b=12}
}
"""
min=vbuild.minimize(js)
```

**Notes:**

 * `templates` are converted to a `<script type="text/x-template" id="XXX"></script>` (not converted to JS)
 * A Minimal component needs the `<template></template>` tag only ([specs](https://vue-loader.vuejs.org/spec.html))
 * You can use `<style></style>` and/or `<style scoped></style>` (as many as you want)
 * styles are minimized (remove comments and spaces)
 

Its main purpose is to let you use components (.vue files) in your vuejs app, without a full nodejs stack. It's up to you to create your generator, to extract the things, and create your "index.html" file. It's a 5 lines of python code; example:

```python
import vbuild,glob

r=sum([vbuild.VBuild(i) for i in glob.glob("*.vue")+glob.glob("*/*.vue")])
buf=readYourTemplate("index.tpl") # should contains a tag "<!-- HERE -->" that would be substituted
buf=buf.replace("<!-- HERE -->",str(r))
writeYourTemplate("index.html",buf)
```

Hope it could help ...


TODO:

 * more utilities
 * and docs !

