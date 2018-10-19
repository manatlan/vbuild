# How generation works 

When you ```vbuild.VBuild("compo1.vue","...")``` or ```vbuild.render("compo1.vue")```, and `compo1.vue` contains scoped style (and, in this example, the first/root tag is a `div`)

(never mind if it's a classical js component or a python components)

Il will generate HTML stuffs like that:

```html

<style>*[data-compo1] {...}</style>

<script type="text/x-template" id="tpl-compo1">
  <div data-compo1>
    ... 
  </div>
</script>

<script>
var compo1= Vue.component('compo1',{
        name: "compo1",
        template: `#tpl-compo1`,
        ...
});
</script>
```

Note that, you can't use several components with the same name ! Because **vbuild** needs to make them unique.

## For <style> : the styles
The rules are prefixed with a css-selector to scope the template : it will match any tag which contains the `unique attribute`.
**note**: non-scoped styles are not prefixed, and so apply to all matched tags.

## For <script type="text/x-template"> : the template
The first/root tag is modified to contain the `unique attribute`, to be sure to be scoped by "scoped style".
The script-template is created with an `unique template id`, which will be referenced in the code as the template.

## For <script> : the code
A global var is declared, with the `unique name` (so you can use it, in $router, for example).
The component is named with the `unique name`, and declare its template with the `unique template id`.

## What are this unique things ?
- `unique name` : it's the (base)name of the component (without the extension ".vue").
- `unique attribut` : it is prefixed with `data-`, and the full path to the component (paths separated by `-`)
- `unique template id` : it is prefixed with `tpl-`, and the full path to the component (paths separated by `-`)

So if the component is "vues/compo1.vue"
- its `unique name` will be `compo1`
- its `unique attribut` will be `data-vues-compo1`
- its `unique template id` will be `tpl-vues-compo1`



