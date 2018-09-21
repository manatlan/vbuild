import vbuild,sys
import unittest

class TesCss(unittest.TestCase):
    def test_css1(self):
        self.assertEqual(vbuild.mkCss("","XXX"),"")

    def test_css2(self):
        self.assertEqual(vbuild.mkCss("   a    {color}  "),      "a {color}")
        self.assertEqual(vbuild.mkCss("   a    {color}  ","XXX"),"XXX a {color}")

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
XXX button[ name ] { background:red }
XXX hr *, XXX body:hover { color:red;}
XXX p > a, XXX p>i { }
"""
        tt=vbuild.mkCss(t,"XXX")
        self.assertEqual(tt,ok.strip())


class TestB(unittest.TestCase):

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
<style>
:scope {
    padding:4px;
    background: yellow
}
  button {background:red}
</style>
"""
        r=vbuild.VBuild("name.vue",h)
        #~ print(r, file=sys.stdout)
        self.assertEqual(r.tags,["name"])

        self.assertEqual(str(r).count("div[data-name]"),2)
        self.assertFalse(":scope" in str(r))
        self.assertTrue("<div data-name>" in str(r))
        self.assertTrue('<script type="text/x-template" id="tpl-name">' in str(r))
        self.assertTrue("var name = Vue.component('name', {template:'#tpl-name'," in str(r))

    def test_composant_min(self):
        h="""
<template>
  <div>Load</div>
</template>
"""
        r=vbuild.VBuild("name.vue",h)
        self.assertTrue("<div data-name>" in str(r))
        self.assertTrue('<script type="text/x-template" id="tpl-name">' in str(r))
        self.assertTrue("var name = Vue.component('name', {template:'#tpl-name'," in str(r))

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

if __name__ == '__main__':
    unittest.main()
