#!/usr/bin/python3
# -*- coding: utf-8 -*-
import vbuild,sys,os
import unittest

ONLYs=[]
def only(f): # decorator to place on tests, to limit usage to only theses ones
    ONLYs.append(f.__name__)
    return f

tu=u"""<template><div>français
    <a title='España'><span class="flags es"></span></a>
    <a title='中国'><span class="flags cn"></span></a>
</div></template>"""

ts="""<template><div>français
    <a title='España'><span class="flags es"></span></a>
    <a title='中国'><span class="flags cn"></span></a>
</div></template>"""

class TestVueParserEncoding(unittest.TestCase):
    def test_unicode(self):
        r=vbuild.VueParser(tu)
        self.assertEqual( type(tu) , type(r.html.value) )
    def test_str(self):
        r=vbuild.VueParser(ts)
        self.assertEqual( type(ts) , type(r.html.value) )

class TestVBuildEncoding(unittest.TestCase):
    """ ENSURE : output type is the same as the input type
        (mainly for py2, no trouble with py3)
    """
    def test_unicode(self):
        r=vbuild.VBuild("x.vue",tu)
        self.assertEqual( type(tu) , type(r.html) )

        r=vbuild.VBuild(u"x.vue",tu)
        self.assertEqual( type(tu) , type(r.html) )

    def test_str(self):
        r=vbuild.VBuild("x.vue",ts)
        self.assertEqual( type(ts) , type(r.html) )

        r=vbuild.VBuild(u"x.vue",ts)
        self.assertEqual( type(ts) , type(r.html) )

    def test_unicode2(self):
        r=vbuild.VBuild("xé.vue",tu)
        self.assertEqual( type(tu) , type(r.html) )

        r=vbuild.VBuild(u"xé.vue",tu)
        self.assertEqual( type(tu) , type(r.html) )

    def test_str2(self):
        r=vbuild.VBuild("xé.vue",ts)
        self.assertEqual( type(ts) , type(r.html) )

        r=vbuild.VBuild(u"xé.vue",ts)
        self.assertEqual( type(ts) , type(r.html) )


class TestVueParser(unittest.TestCase):

    def test_1(self):
        h="""<template><div>XXX</div></template>"""
        r=vbuild.VueParser(h)
        self.assertTrue(isinstance(r.html,vbuild.Content))
        self.assertEqual(repr(r.html),"<div>XXX</div>")
        self.assertEqual(r.script,None)
        self.assertEqual(r.styles,[])
        self.assertEqual(r.scopedStyles,[])
        self.assertEqual(r.rootTag,"div")

        h="""<template type="xxx"><div>XXX</div></template>"""
        r=vbuild.VueParser(h)
        self.assertEqual(repr(r.html),"<div>XXX</div>")

    def test_malformed(self):
        h="""<template><div><br>XXX</div></template>"""
        r=vbuild.VueParser(h)
        self.assertEqual(repr(r.html),"<div><br>XXX</div>")
        self.assertEqual(r.script,None)
        self.assertEqual(r.styles,[])
        self.assertEqual(r.scopedStyles,[])
        self.assertEqual(r.rootTag,"div")

    def test_empty(self):
        h="""<template></template>"""
        r=vbuild.VueParser(h)
        self.assertEqual(repr(r.html),"")
        self.assertEqual(r.script,None)
        self.assertEqual(r.styles,[])
        self.assertEqual(r.scopedStyles,[])
        self.assertTrue(r.rootTag is None)

    def test_more_than_one_template(self):
        h="""<template><div>jo</div></template><template><div>jo</div></template>"""
        with self.assertRaises(vbuild.VBuildException):
            vbuild.VueParser(h) # Component  contains more than one template

    def test_2(self):
        h="""<template>\n     \n   \t     \n     <div>XXX</div> \t \n    </template>"""
        r=vbuild.VueParser(h)
        self.assertEqual(repr(r.html),"<div>XXX</div>")

        h="""<template type="xxx">\n     \n   \t     \n     <div>XXX</div> \t \n    </template>"""
        r=vbuild.VueParser(h)
        self.assertEqual(repr(r.html),"<div>XXX</div>")

        h="""<template> gsfdsgfd   <div>XXX</div>     gfdsgfd    </template>"""
        r=vbuild.VueParser(h)
        self.assertEqual(repr(r.html),"gsfdsgfd   <div>XXX</div>     gfdsgfd")    # acceptable, but not good
        self.assertEqual(r.rootTag,"div")    # acceptable, but not good


    def test_3(self):
        h="""<template type="xxx">
            <div>XXX</div></template>"""
        r=vbuild.VueParser(h)
        self.assertEqual(repr(r.html),"<div>XXX</div>")

        h="""<template type="xxx"><div>XXX</div>
        </template>"""
        r=vbuild.VueParser(h)
        self.assertEqual(repr(r.html),"<div>XXX</div>")

        h="""<template type="xxx">
            <div>XXX</div>
        </template>"""
        r=vbuild.VueParser(h)
        self.assertEqual(repr(r.html),"<div>XXX</div>")

        h="""<template type="xxx">\r\n<div>XXX</div>\r\n</template>"""
        r=vbuild.VueParser(h)
        self.assertEqual(repr(r.html),"<div>XXX</div>")
        h="""<template type="xxx">\n<div>XXX</div>\n</template>"""
        r=vbuild.VueParser(h)
        self.assertEqual(repr(r.html),"<div>XXX</div>")

    def test_bad_not_at_root(self):
        h="""<a><template type="xxx"><div>XXX</div></template></a>"""
        r=vbuild.VueParser(h)
        self.assertEqual(r.html,None)
        self.assertEqual(r.script,None)
        self.assertEqual(r.styles,[])
        self.assertEqual(r.scopedStyles,[])

    def test_bad_not_openclose(self):
        h="""<template type="xxx"><div>XXX</div>"""
        r=vbuild.VueParser(h)
        self.assertEqual(r.html,None)
        self.assertEqual(r.script,None)
        self.assertEqual(r.styles,[])
        self.assertEqual(r.scopedStyles,[])

        h="""<div>XXX</div></template>"""
        r=vbuild.VueParser(h)
        self.assertEqual(r.html,None)
        self.assertEqual(r.script,None)
        self.assertEqual(r.styles,[])
        self.assertEqual(r.scopedStyles,[])

    def test_bad_more_than_one_root(self):
        h="""<template type="xxx"> <div>XXX</div> <div>XXX</div> </template>"""
        with self.assertRaises(vbuild.VBuildException):
            vbuild.VueParser(h) # Component mycomp.vue can have only one top level tag

    def test_bad_no_template(self):
        h="""<templite type="xxx"> <div>XXX</div> <div>XXX</div> </templite>"""
        r=vbuild.VueParser(h)
        self.assertEqual(r.html,None)

    def test_bad_script_bad(self):
        h="""<template> <div>XXX</div></template><script> gdsf gfds """
        r=vbuild.VueParser(h)
        self.assertEqual(r.script,None)

    def test_bad_style_bad(self):
        h="""<template> <div>XXX</div></template><style> gdsf gfds """
        r=vbuild.VueParser(h)
        self.assertEqual(r.script,None)
        self.assertEqual(r.styles,[])
        self.assertEqual(r.scopedStyles,[])

    def test_full(self):
        h="""<template><div>XXX</div></template><style lang="sass">style</style><script lang="python">script</script>"""
        r=vbuild.VueParser(h)
        self.assertTrue(isinstance(r.html,vbuild.Content))
        self.assertTrue(isinstance(r.script,vbuild.Content))
        self.assertEqual(type(r.styles),list)
        self.assertTrue(isinstance(r.styles[0],vbuild.Content))

        self.assertEqual(repr(r.script),"script")
        self.assertEqual(repr(r.styles[0]),"style")
        self.assertEqual(r.script.type,"python")
        self.assertEqual(r.styles[0].type,"sass")

        self.assertEqual(r.html.type,None)  # not used for html (now)

        h="""<template><div>XXX</div></template><style scoped>style</style><script>script</script>"""
        r=vbuild.VueParser(h)
        self.assertEqual(repr(r.script),"script")
        self.assertEqual(repr(r.scopedStyles[0]),"style")
        self.assertEqual(r.script.type,None)
        self.assertEqual(r.scopedStyles[0].type,None)
        self.assertEqual(r.html.type,None)  # not used for html (now)


class TesCss(unittest.TestCase):
    def test_css1(self):
        self.assertEqual(vbuild.mkPrefixCss("","XXX"),"")

    def test_css2(self):
        self.assertEqual(vbuild.mkPrefixCss("   a    {color}  "),      "a {color}")
        self.assertEqual(vbuild.mkPrefixCss("   a    {color}  ","XXX"),"XXX a {color}")

    def test_cssTop(self):
        t="""
:scope
    {padding:4px;background: yellow}

      button[ name  ] {\t\tbackground:red /*que neni*/
}
   hr *,        body:hover {
    color:red;}

p > a, p>i { /*nib*/ }

"""
        ok="""
XXX {padding:4px;background: yellow}
XXX button[ name ] {background:red }
XXX hr *, XXX body:hover {color:red;}
XXX p > a, XXX p>i {}
"""
        tt=vbuild.mkPrefixCss(t,"XXX")
        self.assertEqual(tt,ok.strip())


class TestVBuild(unittest.TestCase):

    def test_bad_more_than_one_root(self):
        h="""<template type="xxx"> <div>XXX</div> <div>XXX</div> </template>"""
        with self.assertRaises(vbuild.VBuildException):
            r=vbuild.VBuild("mycomp.vue",h) # Component mycomp.vue can have only one top level tag

    def test_bad_no_template(self):
        h="""<templite type="xxx"> <div>XXX</div> <div>XXX</div> </templite>"""
        with self.assertRaises(vbuild.VBuildException):
            r=vbuild.VBuild("comp.vue",h)   # Component comp.vue doesn't have a template

    def test_bad_script_bad(self):
        h="""<template> <div>XXX</div></template><script> gdsf gfds </script>"""
        with self.assertRaises(vbuild.VBuildException):
            r=vbuild.VBuild("comp.vue",h)   # Component %s contains a bad script

    def test_bad_script_not_closed(self):
        h="""<template> <div>XXX</div></template><script> gdsf gfds """
        r=vbuild.VBuild("comp.vue",h)   # Component %s contains a bad script
        self.assertTrue(r.script)

    def test_composant_complet(self):
        h="""
<template>
  <div>
    {{c}} <button @click="inc">++</button>
  </div>
</template>
<script>
export default {
  data () {
    return {
      c: 0,
    }
  },
  methods: {
    inc() {this.c+=1;}
  }
}
</script>
<style scoped>
:scope {
    padding:4px;
    background: yellow
}
  button {background:red}
</style>
<style>
  button {background:black}
</style>
"""
        r=vbuild.VBuild("name.vue",h)
        self.assertEqual(r.tags,["name"])
        self.assertEqual(r.style.count("*[data-name]"),2)
        self.assertEqual(r.style.count("background"),3)
        self.assertFalse(":scope" in repr(r))
        self.assertTrue("<div data-name>" in repr(r))
        self.assertTrue('<script type="text/x-template" id="tpl-name">' in repr(r))
        self.assertTrue("var name = Vue.component('name', {template:`#tpl-name`," in repr(r))

    def test_composant_complet_minify(self):
        h="""
<template>
  <div>
    {{c}} <button @click="inc">++</button>
  </div>
</template>
<script>
export default {
  data () {
    return {
      c: 0,
    }
  },
  methods: {
    inc() {this.c+=1;}
  }
}
</script>
<style scoped>
:scope {
    padding:4px;
    background: yellow
}
  button {background:red}
</style>
<style>
  button {background:black}
</style>
"""
        oh=vbuild.transHtml
        oj=vbuild.transScript
        oc=vbuild.transStyle
        try:
            vbuild.transHtml=lambda x:"h"
            vbuild.transScript=lambda x:"j"
            vbuild.transStyle=lambda x:"c"
            r=vbuild.VBuild("name.vue",h)
            self.assertEqual(r.html,'<script type="text/x-template" id="tpl-name">h</script>')
            self.assertEqual(r.script,"j")
            self.assertEqual(r.style,"c")
        finally:
            vbuild.transHtml=oh
            vbuild.transScript=oj
            vbuild.transStyle=oc

    def test_composant_min(self):
        h="""
<template>
  <div>Load</div>
</template>
"""
        r=vbuild.VBuild("name.vue",h)
        self.assertTrue("<div data-name>" in str(r))
        self.assertTrue('<script type="text/x-template" id="tpl-name">' in str(r))
        self.assertTrue("var name = Vue.component('name', {template:`#tpl-name`," in str(r))


    def test_bad_composant_add(self):
        c=vbuild.VBuild("c.vue","""<template><div>XXX</div></template>""")
        with self.assertRaises(vbuild.VBuildException):
            cc=sum([c,c]) # You can't have multiple set(['c'])

    def test_composant_add(self):
        c=vbuild.VBuild("c.vue","""<template><div>XXX</div></template>""")
        d=vbuild.VBuild("d.vue","""<template><div>XXX</div></template>""")
        cc=sum([c,d])
        self.assertTrue(cc.html.count("<div data-c>XXX</div>")==1)
        self.assertTrue(cc.html.count("<div data-d>XXX</div>")==1)
        self.assertTrue(cc.script.count("var c = Vue.component('c', {template:`#tpl-c`,});")==1)
        self.assertTrue(cc.script.count("var d = Vue.component('d', {template:`#tpl-d`,});")==1)

    def test_pickable(self):    # so it's GAE memcach'able !
        h="""
<template>
  <div>Load</div>
</template>
"""
        import pickle
        r=vbuild.VBuild("name.vue",h)
        f_string = pickle.dumps(r)
        f_new = pickle.loads(f_string)
        self.assertEqual(str(r),str(f_new))

    def test_script_good(self):    # so it's GAE memcach'able !
        h="""
<template>
  <div>Load</div>
</template>
<script>
export default {
    mounted() {}
}
</script>
"""
        r=vbuild.VBuild("name.vue",h)
        self.assertEqual(r.script,"""var name = Vue.component('name', {template:`#tpl-name`,\n    mounted() {}\n});""")

    def test_sass(self):
        if not vbuild.hasSass: self.skipTest("Don't test sass (miss pyScss)")

        h="""<template><div>XXX</div></template>
        <Style scoped lang="sass">
        body {
            font: 2px *3;
            color: red + green;
        }
        </style>"""
        r=vbuild.VBuild("comp.vue",h)
        self.assertTrue("6px" in r.style)
        self.assertTrue("#ff8000" in r.style)

        h="""<template><div>XXX</div></template>
        <Style scoped lang="sass">
        body {
            font: $unknown;
        }
        </style>"""
        r=vbuild.VBuild("comp.vue",h)
        with self.assertRaises(vbuild.VBuildException):     # vbuild.VBuildException: Component 'comp.vue' got a CSS-PreProcessor trouble : Error evaluating expression:
            r.style

        # ensure inline def class are OK
        h="""<template><div>XXX</div></template>
        <Style scoped lang="sass">
        :scope {
            color:blue;

            div {color:red}
        }
        </style>"""
        r=vbuild.VBuild("comp.vue",h)
        self.assertEqual(r.style,"""*[data-comp] {color: blue; }\n*[data-comp] div {color: red; }""")


    def test_less(self):
        if not vbuild.hasLess: self.skipTest("Cant test Less (instal lesscpy)")

        h="""<template><div>XXX</div></template>
        <Style scoped Lang = "leSS" >
        body {
            border-width: 2px *3;
        }
        </style>"""
        r=vbuild.VBuild("comp.vue",h)
        self.assertTrue("6px" in r.style)

        h="""<template><div>XXX</div></template>
        <Style scoped lang="less">
        body {
            font: @unknown;
        }
        </style>"""
        r=vbuild.VBuild("comp.vue",h)
        with self.assertRaises(vbuild.VBuildException):     # vbuild.VBuildException: Component 'comp.vue' got a CSS-PreProcessor trouble : Error evaluating expression:
            r.style

    def testVoidElements(self):
        t="""<template>
<div>
    <hr>
    hello {{name}}<br>
    <hr>
</div>
</template>
<style>
h1 {color:blue}
</style>
<script>
export defailt {
    props:["name"],
}
</script>
    """
        rendered="""
<style>
h1 {color:blue}
</style>
<script type="text/x-template" id="tpl-j"><div data-j>
    <hr>
    hello {{name}}<br>
    <hr>
</div></script>
<script>
var j = Vue.component('j', {template:`#tpl-j`,
    props:["name"],
});
</script>
"""
        r=vbuild.VBuild("jo.vu",t)
        self.assertEqual(str(r),rendered)
    def testVoidElements_closed(self):
        t="""<template>
<div>
    <hr/>
    hello {{name}}<br/>
    <hr>
</div>
</template>
<style>
h1 {color:blue}
</style>
<script>
export defailt {
    props:["name"],
}
</script>
    """
        rendered="""
<style>
h1 {color:blue}
</style>
<script type="text/x-template" id="tpl-j"><div data-j>
    <hr/>
    hello {{name}}<br/>
    <hr>
</div></script>
<script>
var j = Vue.component('j', {template:`#tpl-j`,
    props:["name"],
});
</script>
"""
        r=vbuild.VBuild("jo.vu",t)
        self.assertEqual(str(r),rendered)

class TestRenderFiles(unittest.TestCase):
    def testfiles(self):
        if not os.path.isdir("vues"): self.skipTest("Don't test real vue files (you haven't a vues folder with .vue files)")

        import glob
        for i in glob.glob("vues/*.vue"):
            r=vbuild.render(i)
            self.assertTrue(str(r))

        self.assertTrue(str(vbuild.render( "vues/list.vue")))
        self.assertTrue(str(vbuild.render( "vues/*.vue")))
        self.assertTrue(str(vbuild.render( "*/*.vue")))
        self.assertTrue(str(vbuild.render( "vues/test.vue", "vues/todo.vue" )))
        self.assertTrue(str(vbuild.render( ["vues/test.vue","vues/todo.vue"] )))
        self.assertTrue(str(vbuild.render( glob.glob("vues/*.vue"))))


    def test_bad_file(self):
        with self.assertRaises(vbuild.VBuildException):
            vbuild.render("unknown_file.vue") # No such file or directory

class TestPyComponent(unittest.TestCase):
    """ urgghh ... minimal tests here ;-) """

    def test_ok(self):
        c="""<template>
    <div>
        {{name}} {{cpt}}
        <button @click="inc()">++</button>
    </div>
</template>
<script lang="python">

class Component:
    def __init__(self, name):
        self.cpt=0

    def inc(self):
        self.cpt+=1

</script>
<style scoped>
    :scope {background:#EEE}
</style>"""
        r=vbuild.VBuild("pyc.vue",c)
        self.assertTrue("_pyfunc_op_instantiate" in r.script)
        self.assertTrue("Vue.component(" in r.script)

    def test_ko_syntax(self):
        c="""<template>
    <div>
        {{name}} {{cpt}}
        <button @click="inc()">++</button>
    </div>
</template>
<script lang="python">

class Component:
    def __init__(self, name):
        self.cpt=0

    def inc(self)           # miss : !!!
        self.cpt+=1

</script>
<style scoped>
    :scope {background:#EEE}
</style>"""
        with self.assertRaises(vbuild.VBuildException): # Python Component 'pyc.vue' is broken
            vbuild.VBuild("pyc.vue",c)

    def test_ko_semantic(self):
        c="""<template>
    <div>
        {{name}} {{cpt}}
        <button @click="inc()">++</button>
    </div>
</template>
<script lang="python">

class ComponentV0:                  # bad class name
    def __init__(self, name):
        self.cpt=0

    def inc(self):
        self.cpt+=1

</script>
<style scoped>
    :scope {background:#EEE}
</style>"""
        with self.assertRaises(vbuild.VBuildException): # Component pyc.vue contains a bad script
            vbuild.VBuild("pyc.vue",c)

class TestPy2Js(unittest.TestCase):
    def test_1(self):
        c="class Component: pass"
        js=vbuild.mkPythonVueComponent("toto","<div></div>",c)
        self.assertTrue("_pyfunc_op_instantiate" in js)
        self.assertTrue("Vue.component('toto',{" in js)
        self.assertTrue('name: "toto",' in js)
        self.assertTrue('template: `<div></div>`,' in js)

    def test_MOUNTED(self):
        c="""class Component:
  def MOUNTED(self):
    pass"""
        js=vbuild.mkPythonVueComponent("toto","<div></div>",c)
        self.assertTrue("_pyfunc_op_instantiate" in js)
        self.assertTrue("Vue.component(" in js)
        self.assertTrue('mounted: C.prototype.MOUNTED,' in js)

    def test_CREATED(self):
        c="""class Component:
  def CREATED(self):
    pass"""
        js=vbuild.mkPythonVueComponent("toto","<div></div>",c)
        self.assertTrue("_pyfunc_op_instantiate" in js)
        self.assertTrue("Vue.component(" in js)
        self.assertTrue('created: C.prototype.CREATED,' in js)


    def test_COMPUTED(self):
        c="""class Component:
  def COMPUTED_var(self):
    pass"""
        js=vbuild.mkPythonVueComponent("toto","<div></div>",c)
        self.assertTrue("_pyfunc_op_instantiate" in js)
        self.assertTrue("Vue.component(" in js)
        self.assertTrue('var: C.prototype.COMPUTED_var,' in js)

    def test_WATCH(self):
        c="""class Component:
  def WATCH_var(self,oldVal,newVal,name="$store.state.yo"):
    pass"""
        js=vbuild.mkPythonVueComponent("toto","<div></div>",c)
        self.assertTrue("_pyfunc_op_instantiate" in js)
        self.assertTrue("Vue.component(" in js)
        self.assertTrue('"$store.state.yo": C.prototype.WATCH_var,' in js)

    def test_WATCH_ko(self):
        c="""class Component:
  def WATCH_var(self):
    pass"""
        with self.assertRaises(vbuild.VBuildException): # vbuild.VBuildException: name='var_to_watch' is not specified in WATCH_var
            vbuild.mkPythonVueComponent("toto","<div></div>",c)

        c="""class Component:
  def WATCH_var(self,oldVal,newVal,name):
    pass"""
        with self.assertRaises(vbuild.VBuildException): # vbuild.VBuildException: name='var_to_watch' is not specified in WATCH_var
            vbuild.mkPythonVueComponent("toto","<div></div>",c)

    def test_INIT_PROPS(self):
        c="""class Component:
  def __init__(self,prop1="?",prop2="?"):
    self.val1=42
    self.val2=True
    self.val3="hello"
"""
        js=vbuild.mkPythonVueComponent("toto","<div></div>",c)
        self.assertTrue("_pyfunc_op_instantiate" in js)
        self.assertTrue("Vue.component(" in js)
        self.assertTrue("props: ['prop1', 'prop2']," in js)
        self.assertTrue("for(var n of ['prop1', 'prop2']) props.push( this.$props[n] )" in js)
        jsinit="""C.prototype.__init__ = function (prop1, prop2) {
    prop1 = (prop1 === undefined) ? "?": prop1;
    prop2 = (prop2 === undefined) ? "?": prop2;
    this.val1 = 42;
    this.val2 = true;
    this.val3 = "hello";
    return null;
};"""
        self.assertTrue(jsinit in js)

    def test_METHODS(self):
        c="""class Component:
  def method1(self,nb):
    self["$parent"].nb=nb;
"""
        js=vbuild.mkPythonVueComponent("toto","<div></div>",c)
        self.assertTrue("_pyfunc_op_instantiate" in js)
        self.assertTrue("Vue.component(" in js)
        self.assertTrue("method1: C.prototype.method1," in js)
        self.assertTrue('this["$parent"].nb = nb;' in js)

class TestTrans(unittest.TestCase):
    def test_1(self):
        vbuild.transScript=lambda x: x.upper()
        vbuild.transStyle=lambda x: x+"/*Hello*/"
        vbuild.transHtml=lambda x: x.upper()
        r=vbuild.VBuild("toto.vue","<template><div></div></template>")
        self.assertTrue("VUE.COMPONENT('TOTO'" in r.script)
        self.assertTrue('<script type="text/x-template" id="tpl-toto"><DIV DATA-TOTO></DIV></script>' in r.html)
        self.assertEqual(r.style,"/*Hello*/")


    def tearDown(self):
        vbuild.transScript=lambda x: x
        vbuild.transStyle=lambda x: x
        vbuild.transHtml=lambda x: x

class TestPyStdLibIncludeOrNot(unittest.TestCase):
    cj="""<template><div>yo</div></template>"""
    cp="""<template><div>yo</div></template><script>class Component: pass</script>"""

    def setUp(self):
        self.default=vbuild.fullPyComp

    def tearDown(self):
        vbuild.fullPyComp=self.default # reset to default

    def isPythonComp(self,r):
        return "_pyfunc_op_instantiate(" in r.script

    def nbPythonLibIncluded(self,r):
        return r.script.count("var _pyfunc_op_instantiate")

    def test_base(self):
        r=vbuild.VBuild("c.vue",self.cj)
        self.assertFalse(self.isPythonComp(r))  # comp is js

        r=vbuild.VBuild("c.vue",self.cp)
        self.assertTrue(self.isPythonComp(r))   # comp is py

    def test_fullPyComp_Default(self):
        r=vbuild.VBuild("c.vue",self.cj)
        self.assertEqual(self.nbPythonLibIncluded(r),0)    # no py no lib
        r+=vbuild.VBuild("c1.vue",self.cp)
        r+=vbuild.VBuild("c2.vue",self.cp)
        self.assertTrue(self.isPythonComp(r))
        self.assertEqual(self.nbPythonLibIncluded(r),2)    # each comp got its own std methods

    def test_fullPyComp_False(self):
        vbuild.fullPyComp=False
        r=vbuild.VBuild("c.vue",self.cj)
        self.assertEqual(self.nbPythonLibIncluded(r),0)    # no py no lib
        r+=vbuild.VBuild("c1.vue",self.cp)
        r+=vbuild.VBuild("c2.vue",self.cp)
        self.assertTrue(self.isPythonComp(r))
        self.assertEqual(self.nbPythonLibIncluded(r),1)    # the full std lib is included

    def test_fullPyComp_True(self):
        vbuild.fullPyComp=True
        r=vbuild.VBuild("c.vue",self.cj)
        self.assertEqual(self.nbPythonLibIncluded(r),0)    # no py no lib
        r+=vbuild.VBuild("c1.vue",self.cp)
        r+=vbuild.VBuild("c2.vue",self.cp)
        self.assertTrue(self.isPythonComp(r))
        self.assertEqual(self.nbPythonLibIncluded(r),2)    # each comp got its own std methods

    def test_fullPyComp_None(self):
        vbuild.fullPyComp=None
        r=vbuild.VBuild("c.vue",self.cj)
        self.assertEqual(self.nbPythonLibIncluded(r),0)    # no py no lib
        r+=vbuild.VBuild("c1.vue",self.cp)
        r+=vbuild.VBuild("c2.vue",self.cp)
        self.assertTrue(self.isPythonComp(r))
        self.assertEqual(self.nbPythonLibIncluded(r),0)    # nothing is included, it's up to you

class TestjsMin(unittest.TestCase):
    def test_bad(self):
        if not vbuild.hasClosure: self.skipTest("Don't test local jsmin (miss closure)")

        s="""
        kk{{_=*juhgj;://\\}$bc(.[hhh]
        """
        with self.assertRaises(vbuild.VBuildException): # vbuild.VBuildException: minimize error: [{'type': 'JSC_PARSE_ERROR', 'file': 'Input_0', 'lineno': 2, 'charno': 10, 'error': 'Parse error. Semi-colon expected', 'line': '        kk{{_=*jùhgj;://\\}$bc(.[hhh]'}]
            vbuild.jsmin(s)

    def test_min(self):
        if not vbuild.hasClosure: self.skipTest("Don't test local jsmin (miss closure)")

        s="""
        async function  jo(...a) {
            var f=(...a) => {let b=`hello`}
        }
        """
        x=vbuild.jsmin(s)
        self.assertTrue( "$jscomp" in x)

class TestJSminOnline(unittest.TestCase):
    def test_bad(self):
        s="""
        kk{{_=*jùhgj;://\\}$bc(.[hhh]
        """
        with self.assertRaises(vbuild.VBuildException): # vbuild.VBuildException: minimize error: [{'type': 'JSC_PARSE_ERROR', 'file': 'Input_0', 'lineno': 2, 'charno': 10, 'error': 'Parse error. Semi-colon expected', 'line': '        kk{{_=*jùhgj;://\\}$bc(.[hhh]'}]
            vbuild.jsminOnline(s)

    def test_min(self):
        s="""
        async function  jo(...a) {
            var f=(...a) => {let b=`hello`}
        }
        """
        x=vbuild.jsminOnline(s)
        self.assertTrue( "$jscomp" in x)

    def test_pycomp_onlineClosurable(self):
        """ Ensure python component produce a JS which is closure's online ready !"""
        cp="""<template><div>yo</div></template><script>class Component: pass</script>"""
        try:
            default=vbuild.fullPyComp
            vbuild.fullPyComp=False
            r=vbuild.VBuild("c.vue",cp)
            x=vbuild.jsminOnline(r.script)
            self.assertTrue(x)
        finally:
            vbuild.fullPyComp=default


if __name__ == '__main__':

    if ONLYs:
        print("*** WARNING *** skip some tests !")
        def load_tests(loader, tests, pattern):
            suite = unittest.TestSuite()
            for c in tests._tests:
                suite.addTests( [t for t in c._tests if t._testMethodName in ONLYs] )
            return suite

    unittest.main()
