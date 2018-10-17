# vbuild

"Compile" your [VueJS](https://vuejs.org/) components (*.vue) to standalone html/js/css ... python only, **no need of nodejs**. And you can use [python components](https://github.com/manatlan/vbuild/blob/master/doc/PyComponent.md) with **vbuild**, in your vue/sfc files !!!

It's just an utility to extract HTML(template), SCRIPT and STYLE from a [VUE/SFC component]((https://fr.vuejs.org/v2/guide/single-file-components.html)) (*.vue). It won't replace webpack/nodejs/vue-cli, it fills the _"Sometimes you have to work with the tools you have, not the ones you want."_ gap.

[Available on pypi](https://pypi.org/project/vbuild/)

[Changelog](https://github.com/manatlan/vbuild/blob/master/changelog.md)

## Features

 * **NO node-js stack**, only pure python (py2 or py3 compliant)
 * **NEW 0.6.0** Ability to use [python components](https://github.com/manatlan/vbuild/blob/master/doc/PyComponent.md)
  * Components can be styled with [SASS or LESS ccs-pre-processors](https://github.com/manatlan/vbuild/blob/master/doc/CssPreProcess.md) !
 * Provide a [JS-minimizer (ES5 compliant JS, via closure)](https://github.com/manatlan/vbuild/blob/master/doc/minimize.md)
 * Ability to [post process stuff](https://github.com/manatlan/vbuild/blob/master/doc/PostProcess.md), with your own processors
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


## Vue/sfc component compatibility

All classical JS vue/sfc components are compatibles. But now, you can use [python component](https://github.com/manatlan/vbuild/blob/master/doc/PyComponent.md) too. 

Here is, side by side, the same component (in js, and in python):

<image src="https://raw.githubusercontent.com/manatlan/vbuild/master/doc/vs.png"/>

## To use the full features of vbuild

If you want to use the full features, you'll need to install the optionnal's libs.

```
sudo pip install pyscss lesscpy closure
```

All theses libs works with py2 and/or py3, and you could use the [ccs-pre-processors SASS and LESS](https://github.com/manatlan/vbuild/blob/master/doc/CssPreProcess.md), and [closure to minify js](https://github.com/manatlan/vbuild/blob/master/doc/minimize.md).

## TODO

 * more utilities
 * more rock solid version
 * and docs !
 * add pyscss lesscpy closure to pip setup.py (optionnal's modules)
 * see the [TODO list for python components too](https://github.com/manatlan/vbuild/blob/master/doc/PyComponent.md)

