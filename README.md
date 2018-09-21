# vbuild

"Compile" your VUE component (*.vue) to standalone html/js/css ... python only (no need of nodejs)

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
``

and a VBuild is pick'able !

