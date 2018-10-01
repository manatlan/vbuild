#!/usr/bin/python
import vbuild

c1="""
<template>
    <div>
        {{name}} {{cpt}}
        {{hashtag}} {{wcpt}}
        <button @click="inc()" ref="btn1">++</button>
        <button @click="dinc()">**</button>    
    </div>
</template>
<script>
class Component:
    props=["name"]

    def __init__(self):
        self.cpt=0
        self.wcpt=""

    def inc(self):
        def getv(): return 1
        self.cpt+=getv()
        print("===",self.name)

    def dinc(self):
        self.inc()
        self.inc()

    def COMPUTED_hashtag(self):
        return self.cpt*"#"

    def MOUNTED(self):
        self.inc()
        print("--mounted",self.name)
        print(self)

    def CREATED(self):
        print("CREATED")

    def WATCH_1(self,newVal,oldVal,name="cpt"):
        print("WATCH",name,oldVal,"-->",newVal)
        self.wcpt=self.cpt*"+"
</script>
<style scoped lang="sass">
:scope {background:#FFE;border:1px solid black;margin: $v;padding:$v;}
</style>
"""

vbuild.partial="$v: 12px;"

with open("aeff.html","w+") as fid:
    fid.write("""
<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
%s
<div id="app">
    <comp name="n1"></comp>
    <comp name="n2"></comp>
</div>
</script>
<script>new Vue({el:"#app"})</script>    
""" % vbuild.render("comp.vue",c1)
    )

