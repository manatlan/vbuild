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
__version__="0.4.3"   #py2.7 & py3.5 !!!!


try:
    from HTMLParser import HTMLParser
    import urllib2 as urlrequest    
    import urllib as urlparse
except ImportError:
    from html.parser import HTMLParser
    import urllib.request as urlrequest
    import urllib.parse as urlparse

def minimize(txt):
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


class VueParser(HTMLParser):
    def __init__(self,buf,name=""):
        HTMLParser.__init__(self)
        self.name=name
        self._p1=None
        self._level=0
        self.rootTag=None
        self.html,self.script,self.styles,self.scopedStyles=None,None,[],[]
        self.feed(buf.strip("\n\r\t "))
    
    def handle_starttag(self, tag, attrs):
        self._tag=tag
        self._level+=1
        
        if self._level==1 and tag=="template":
            if self._p1 is not None: raise VBuildException( "Component %s contains more than one template" % self.name)
            self._p1=self.getOffset()+len(self.get_starttag_text())
        if self._level==2 and self._p1: # test p1, to be sure to be in a template
            if self.rootTag is not None: raise VBuildException( "Component %s can have only one top level tag !" % self.name)
            self.rootTag = tag

    def handle_endtag(self, tag):
        if tag=="template" and self._p1: # don't watch the level (so it can accept mal formed html
            self.html=self.rawdata[self._p1:self.getOffset()].strip("\n\r\t ")
        self._level-=1
        
    def handle_data(self, data):
        if self._level==1:
            if self._tag=="script": self.script=data.strip("\n\r\t ")
            if self._tag=="style":  
                if "scoped" in self.get_starttag_text().lower():
                    self.scopedStyles.append(data)
                else:
                    self.styles.append(data.strip("\n\r\t "))
                    
    def getOffset(self):
        lineno, off = self.getpos()
        rtn = 0
        for _ in range(lineno - 1):
            rtn = self.rawdata.find('\n', rtn) + 1
        return rtn + off        

def mkPrefixCss(css,prefix=""):
    lines=[]
    css=re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,css)
    css=re.sub(re.compile("[ \t\n]+",re.DOTALL ) ," " ,css)
    for rule in re.findall(r'[^}]+{[^}]+}', css):
        sels,decs=rule.split("{",1)
        l=[prefix+(" "+i.strip() if i.strip()!=":scope" else "") for i in sels.split(",")]
        lines.append( ", ".join(l) +" {"+decs )
    return "\n".join(lines).strip("\n ")

class VBuildException(Exception): pass

class VBuild:
    def __init__(self,filename,content=None):  # old vueToTplScript (only one style default scoped !)
        if content is None:
            try:
                with open(filename,"r+") as fid:
                    content=fid.read()
            except IOError as e:
                raise VBuildException(str(e))

        name=os.path.basename(filename)[:-4]
        unique = filename[:-4].replace("/","-").replace("\\","-").replace(":","-")
        # unique = name+"-"+''.join(random.choice(string.letters + string.digits) for _ in range(8))
        tplId="tpl-"+unique
        dataId="data-"+unique

        vp=VueParser(content,filename)
        if vp.html is None:
            raise VBuildException("Component %s doesn't have a template" % filename)
        else:
            html=re.sub(r'^<([\w-]+)',r"<\1 "+dataId,vp.html)

            if vp.script:
                p1=vp.script.find("{")
                p2=vp.script.rfind("}")
                if 0 <= p1 <= p2:
                    js= vp.script[p1:p2+1]
                else:
                    raise VBuildException("Component %s contains a bad script" % filename)                    
            else:
                js="{}"
            
            self.html="""<script type="text/x-template" id="%s">%s</script>""" % (tplId,html)
            self.script="""var %s = Vue.component('%s', %s);""" % (name,name,js.replace("{","{template:'#%s'," % tplId,1))
            self.style=""
            # if vp.scopedStyles: self.style=mkPrefixCss("\n".join(vp.scopedStyles),"%s[%s]" % (vp.rootTag,dataId))
            if vp.scopedStyles: self.style=mkPrefixCss("\n".join(vp.scopedStyles),"*[%s]" % dataId)
            if vp.styles: self.style+="\n"+mkPrefixCss("\n".join(vp.styles))
            self.tags=[name]

    def __add__(self,o):
        join=lambda *l: ("\n".join(l)).strip("\n")
        same=set(self.tags).intersection(set(o.tags))
        if same: raise VBuildException("You can't have multiple '%s'" % list(same)[0])
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



if __name__=="__main__":
    exec(open("./tests.py").read())
    
