# Minimize JS (ES5 compliant)

**vbuild** provide a js-minimizer(transpiler) (to generate ES5 compliant js) (thru on the [clojure online service](https://closure-compiler.appspot.com))

## example

```python
js="""async function  mymethod(...a) {
    var f=(...a) => {let b=12}
}
"""
min=vbuild.minimize(js)
```