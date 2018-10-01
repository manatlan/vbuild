#!/usr/bin/python
import vbuild

c1="""
<template>
    <div>
        {{name}} ({{originalName}})
        <button @click="inc()" ref="btn1">++</button>
        <button @click="dinc()">**</button>    
        {{cpt}}
        {{ccpt}} {{wcpt}}
    </div>
</template>
<script>
class Component:

    def __init__(self, name="?"):
        print("DATA INIT",name)
        self.cpt=0
        self.wcpt=""
        self.originalName=name

    def inc(self):
        print("++",self.name)
        def getv(): return 1
        self.cpt+=getv()

    def dinc(self):
        self.inc()
        self.inc()

    def CREATED(self):
        print("CREATED",self.name)

    def MOUNTED(self):
        print("mounted",self.name,"in",self["$parent"]["$options"].name)
        print(self["$parent"])
        self.inc()

    def COMPUTED_ccpt(self):
        return self.cpt*"#"

    def WATCH_1(self,newVal,oldVal,name="cpt"):
        print("WATCH",self.name,name,oldVal,"-->",newVal)
        self.wcpt=self.cpt*"+"
</script>
<style scoped lang="sass">
:scope {background:#FFE;border:1px solid black;margin: $v;padding:$v;}
</style>
"""

cp="""
<template>
    <div>
        {{nom}} <button @click="inc()">n</button>
        <comp :name="nom"></comp>
        <comp name="n2"></comp>
        <comp></comp>

    </div>
</template>
<script>
class Component:

    def __init__(self):
        self.nom="nx"

    def inc(self):
        self.nom+="x"

</script>
"""

vbuild.partial="$v: 12px;"

with open("aeff.html","w+") as fid:
    fid.write("""
<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
%s
<div id="app">
    <maman/>
</div>
</script>
<script>new Vue({el:"#app"})</script>    
""" % (vbuild.render("comp.vue",c1)+vbuild.render("maman.vue",cp))
    )

