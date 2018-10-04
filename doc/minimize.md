# Minimize JS (ES5 compliant)

**vbuild** provide a js-minimizer(transpiler) (to generate ES5 compliant js), which will use [closure](https://pypi.org/project/closure/) if it's installed, or will use the online version [clojure online service](https://closure-compiler.appspot.com)).

Its signature is :

`vbuild.minimize( jsScript) -> jsScript`

But you can use too :
- `vbuild.jsmin( jsScript) -> jsScript` : for the local version (which use closure)
- `vbuild.jsminOnline( jsScript) -> jsScript` : for the online version

`vbuild.minimize()` is just a wrapper around thoses functions.

## example

```python
js="""async function  mymethod(...a) {
    var f=(...a) => {let b=12}
}
"""
min=vbuild.minimize(js)
min=vbuild.jsmin(js)
min=vbuild.jsminOnline(js)

```