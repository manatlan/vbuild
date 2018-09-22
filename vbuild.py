#!/usr/bin/python
# -*- coding: utf-8 -*-
import re,os,json
# #############################################################################
#    Copyright (C) 2018 manatlan manatlan[at]gmail(dot)com
#
# MIT licence
#
# https://github.com/manatlan/vbuild
# #############################################################################

__version__="0.3"   #py2.7 & py3.5 !!!!

def minimize(txt):
    try:                                        #py3
        import urllib.request as urlrequest
        import urllib.parse as urlparse
    except ImportError:                         #py2
        import urllib2 as urlrequest    
        import urllib as urlparse
    data={
      'js_code':txt,
      'compilation_level':'SIMPLE_OPTIMIZATIONS',
      'output_format':'json',
      'output_info':'compiled_code',
    }
    req = urlrequest.Request("https://closure-compiler.appspot.com/compile",urlparse.urlencode(data).encode("utf8"),{'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8'})
    response=urlrequest.urlopen(req)
    buf = response.read()    
    response.close()
    return json.loads(buf)["compiledCode"]


def mkPrefixCss(css,prefix=""):
    lines=[]
    css=re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,css)
    css=re.sub(re.compile("[ \t\n]+",re.DOTALL ) ," " ,css)
    for rule in re.findall(r'[^}]+{[^}]+}', css):
        sels,decs=rule.split("{",1)
        l=[prefix+(" "+i.strip() if i.strip()!=":scope" else "") for i in sels.split(",")]
        lines.append( ", ".join(l) +" {"+decs )
    return "\n".join(lines).strip("\n ")

class VBuild:
    def __init__(self,filename,content=None):  # old vueToTplScript (only one style default scoped !)
        if content is None:
            with open(filename,"r+") as fid:
                content=fid.read()

        name=os.path.basename(filename)[:-4]
        unique = filename[:-4].replace("/","-").replace("\\","-").replace(":","-")
        # unique = name+"-"+''.join(random.choice(string.letters + string.digits) for _ in range(8))
        tplId="tpl-"+unique
        dataId="data-"+unique

        vt= re.search(r'<(template).*?>(.*)</\1>(?s)', content)
        vs= re.search(r'<(script).*?>[^\{]*(\{.*\})[^\}]*</\1>(?s)', content)   # better regex compatible real vue et marco ;-)
        vc= re.search(r'<(style).*?>(.*)</\1>(?s)', content)

        html=vt.group(2)
        js=vs and vs.group(2) or "{}"
        css=vc and vc.group(2)

        g=re.search(r'<([\w-]+).*?>',html)
        tag=g.group(1)
        dec = g.group(0)
        newdec=dec.replace("<%s"%tag,"<%s %s"%(tag,dataId))
        html=html.replace(dec,newdec,1)

        self.html="""<script type="text/x-template" id="%s">%s</script>""" % (tplId,html)
        self.script="""var %s = Vue.component('%s', %s);""" % (name,name,js.replace("{","{template:'#%s'," % tplId,1))
        self.style=mkPrefixCss(css,"%s[%s]" % (tag,dataId)) if css else ""
        self.tags=[name]

    def __add__(self,o):
        join=lambda *l: ("\n".join(l)).strip("\n")
        self.html=join(self.html,o.html)
        self.script=join(self.script,o.script)
        self.style=join(self.style,o.style)
        self.tags.extend(o.tags)
        return self
    def __radd__(self, o):
        return self if o == 0 else self.__add__(o)
    def __getstate__(self):
        return self.__dict__
    def __setstate__(self, d):
        self.__dict__ = d
    def __repr__(self):
        return """
<style>
%s
</style>
%s
<script>
%s
</script>
""" % (self.style,self.html,self.script)

    def toTestFile(self,filename):
        with open(filename,"w+") as fid:
            fid.write("""
<script src="https://unpkg.com/vue@2.5.16/dist/vue.js"></script>
%s
<div id="app"> x %s x </div>
<script>new Vue({el:"#app"});</script>
        """ % (self,"".join(["<%s/>"%t for t in self.tags])))


if __name__=="__main__":
    from glob import glob
    #~ o=sum( [VBuild(i) for i in glob("comps/**/*.vue")] )
    #~ o=VBuild("comps/c1.vue")
    #~ o=VBuild(r"D:\PROG\wreqman\web\req.vue")
    #~ o.toTestFile("aeff.html")
    #~ print(o)
    pass    
