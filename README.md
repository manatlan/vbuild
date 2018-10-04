# vbuild

"Compile" your [VueJS](https://vuejs.org/) components (*.vue) to standalone html/js/css ... python only, **no need of nodejs**.

It's just an utility to extract HTML(template), SCRIPT and STYLE from a [VUE/SFC component]((https://fr.vuejs.org/v2/guide/single-file-components.html)) (*.vue). It won't replace webpack/nodejs/vue-cli, it fills the _"Sometimes you have to work with the tools you have, not the ones you want."_ gap.

[Available on pypi](https://pypi.org/project/vbuild/)

## Features

 * **NO node-js stack**, only pure python (py2 or py3 compliant)
 * **NEW** Ability to use [python components](doc/PyComponent.md)
 * Components can be styled with [SASS or LESS ccs-pre-processors](doc/CssPreProcess.md) !
 * Provide a [JS-minimizer (ES5 compliant JS, via closure)](doc/minimize.md)
 * Ability to [post process stuff](doc/PostProcess.md), with your own processors
 * Respect [VueJs specs](https://vue-loader.vuejs.org/spec.html) (at least one template tag, many style (scoped or not) tags)
 * `templates` are converted to a `<script type="text/x-template" id="XXX"></script>` (not converted to JS)
 * Unittested (coverage 100%)
 

```python
import vbuild

c=vbuild.render("mycompo.vue")
#c=vbuild.render("vues/*.vue")
#c=vbuild.render( "c1.vue", "c2.vue" )
#c=vbuild.render( "c1.vue", "vues/*.vue" )

print( c.html )
print( c.script )
print( c.style )

#or 

print( c ) # all stuff in html tags

```

## Main Goal

Its main purpose is to let you use components (.vue files) in your vuejs app, without a full nodejs stack. It's up to you to create your generator, to extract the things, and create your "index.html" file. It's a 4 lines of python code; example:

```python
import vbuild
buf=readYourTemplate("index.tpl") # should contains a tag "<!-- HERE -->" that would be substituted
buf=buf.replace("<!-- HERE -->",str( vbuild.render( "vues/*.vue" ) ) )
writeYourTemplate("index.html",buf)
```

([a real example](https://github.com/manatlan/wuy/tree/master/examples/vueapp) of rendering vue/sfc components, using **vbuild** and the marvelous [wuy](https://github.com/manatlan/wuy))


## A python component

Here is a simple example : a "named counter" (with a button to add +1 to the counter):

```html
<template>
    <div>
        {{name}} : {{cpt}} <button @click="inc()">+1</button>
    </div>
</template>
<script lang="python">

class Component:
    def __init__(self, name):   # name is a props !
        self.cpt=0
    def inc(self):
        self.cpt+=1

</script>
<style scoped>
:scope {background:yellow}
</style>
```

If this file is named `cpt.vue` ; you can use it with `<cpt name="c"></cpt>`.


## TODO

 * more utilities
 * more rock solid version
 * and docs !
 * see the [TODO list for python components too]((doc/PyComponent.md))

