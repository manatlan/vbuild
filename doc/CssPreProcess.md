# Css Pre-processors

**vbuild** let you use CSS Pre-Processors in your style's declarations. Currently, only two are availables, (thoses was backported to pure python) :
 
    * [SASS/SCSS](https://sass-lang.com/) (new syntax only) : using `<style lang="scss"></style>` or `<style lang="sass"></style>`). You'll need to install [pyscss](https://pypi.org/project/pyScss/)
    * [LESS](http://lesscss.org/) : using `<style lang="less"></style>`). You'll need to install [lesscpy](https://pypi.org/project/lesscpy/)

Technically, you can merge sass and less components (but it's not a good practice !), but you can only use one partial (common declarations) for all.

If you need to use your own css processor, you can override the transform method [vbuild.transStyle](PostProcess.md) !

## Example using SASS
```html
<!-- hbox.vue -->
<template>
    <div><slot/></div>
</template>
<style scoped lang="sass">
:scope {
    display: flex;
    flex-flow: row nowrap;
    background: $color;          /* <-- SASS variable */
}
</style>
```

and when rendering, you can define your `partial` (aka 'common declarations') using `vbuild.partial` like that:

```python
import vbuild
vbuild.partial="$color: red;"
buf=readYourTemplate("index.tpl") # should contains a tag "<!-- HERE -->" that would be substituted
buf=buf.replace("<!-- HERE -->",str( vbuild.render( "vues/*.vue" ) ) )
writeYourTemplate("index.html",buf)
```

In this case, the (scoped) style rendering will look like that :
```css
*[data-hbox] {display: flex;flex-flow: row nowrap;background: red;}
```

## Example using LESS
```html
<!-- hbox.vue -->
<template>
    <div><slot/></div>
</template>
<style scoped lang="less">
:scope {
    display: flex;
    flex-flow: row nowrap;
    background: @color;          /* <-- LESS variable */
}
</style>
```

and when rendering, you can define your `partial` (aka 'common declarations') using `vbuild.partial` like that:

```python
import vbuild
vbuild.partial="@color: red;"
buf=readYourTemplate("index.tpl") # should contains a tag "<!-- HERE -->" that would be substituted
buf=buf.replace("<!-- HERE -->",str( vbuild.render( "vues/*.vue" ) ) )
writeYourTemplate("index.html",buf)
```

In this case, the (scoped) style rendering will look like that :
```css
*[data-hbox] {display: flex;flex-flow: row nowrap;background: red;}
```
