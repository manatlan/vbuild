# Transform html/style/script (Post Processor stuff)

**vbuild** let you setup your post processors, which will be called for each component stuffs. It can be usefull for tasks like :

    * Minify your (html/script/style ...)
    * Add a comment date in your rendered stuff.
    * Transpile your script
    * Use another css pre-processor
    * ...

There a 3 kinds of post process :

    * transHtml : post process the html of the component (by default `lambda x:x`)
    * transScript : post process the script of the component (by default `lambda x:x`)
    * transStyle : post process the style of the component (by default `lambda x:x`)

Just override them to use yours ...

## Example (minify your js)

```python
import vbuild
from YourMinimzer import jsmin

vbuild.transScript = lambda x: jsmin(x, force=True )
r=vbuild.render("*.vue")

r.script # contains the JS which was transScript'ed
```
