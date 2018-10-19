# How generation works 

When you ```vbuild.VBuild("compo1.vue","...")``` or ```vbuild.render("compo1.vue")```, and `compo1.vue` contains scoped style.

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
## For <style> : the styles
...

## For <script type="text/x-template"> : the template
...

## For <script> : the code
...

