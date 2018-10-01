#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re,os,json,glob,itertools
# #############################################################################
#    Copyright (C) 2018 manatlan manatlan[at]gmail(dot)com
#
# MIT licence
#
# https://github.com/manatlan/vbuild
# #############################################################################
__version__="0.5.0+"   #py2.7 & py3.5 !!!!

try:
    from HTMLParser import HTMLParser
    import urllib2 as urlrequest    
    import urllib as urlparse
except ImportError:
    from html.parser import HTMLParser
    import urllib.request as urlrequest
    import urllib.parse as urlparse


transHtml = lambda x:x    # override them to use your own transformer/minifier
transStyle = lambda x:x
transScript = lambda x:x

partial=""

class VBuildException(Exception): pass


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


def preProcessCSS(css,partial=""):
    if css.type in ["scss","sass"]:
        try:
            from scss.compiler import compile_string   #lang="scss" 
            return compile_string(partial+"\n"+css) 
        except ImportError:
            print("***WARNING*** : miss 'sass' preprocessor : sudo pip install pyscss")
            return css
    elif css.type in ["less"]:
        try:
            import lesscpy
            from six import StringIO  
            return lesscpy.compile( StringIO(partial+"\n"+css) , minify=True)
        except ImportError:
            print("***WARNING*** : miss 'less' preprocessor : sudo pip install lesscpy")
            return css
    else:
        return css



class Content(str):
    def __new__(cls, v, type=None):
        s= str.__new__(cls, v and v.strip("\n\r\t "))
        s.type=type
        return s

class VueParser(HTMLParser):
    def __init__(self,buf,name=""):
        HTMLParser.__init__(self)
        self.name=name
        self._p1=None
        self._level=0
        self._scriptLang=None
        self._styleLang=None
        self.rootTag=None
        self.html,self.script,self.styles,self.scopedStyles=None,None,[],[]
        self.feed(buf.strip("\n\r\t "))
    
    def handle_starttag(self, tag, attrs):
        self._tag=tag
        self._level+=1
        attributes=dict([(k.lower(),v and v.lower()) for k,v in attrs])
        if tag=="style" and attributes.get("lang",None):
            self._styleLang= attributes["lang"]
        if tag=="script" and attributes.get("lang",None):
            self._scriptLang= attributes["lang"]
        if self._level==1 and tag=="template":
            if self._p1 is not None: raise VBuildException( "Component %s contains more than one template" % self.name)
            self._p1=self.getOffset()+len(self.get_starttag_text())
        if self._level==2 and self._p1: # test p1, to be sure to be in a template
            if self.rootTag is not None: raise VBuildException( "Component %s can have only one top level tag !" % self.name)
            self.rootTag = tag

    def handle_endtag(self, tag):
        if tag=="template" and self._p1: # don't watch the level (so it can accept mal formed html
            self.html=Content(self.rawdata[self._p1:self.getOffset()])
        self._level-=1
        
    def handle_data(self, data):
        if self._level==1:
            if self._tag=="script": self.script=Content(data,self._scriptLang)
            if self._tag=="style": 
                if "scoped" in self.get_starttag_text().lower():
                    self.scopedStyles.append( Content(data,self._styleLang) )
                else:
                    self.styles.append( Content(data,self._styleLang))
                    
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

            self.html="""<script type="text/x-template" id="%s">%s</script>""" % (tplId,html)
            self.style=""
            
            for style in vp.styles:
                self.style+=mkPrefixCss( preProcessCSS(style,partial) )+"\n"
            for style in vp.scopedStyles:
                self.style+=mkPrefixCss( preProcessCSS(style,partial),"*[%s]" % dataId)+"\n"

            self.tags=[name]

            if vp.script and "class Component:" in vp.script:
                ######################################################### python
                self.script=mkPythonVueComponent(name,'#'+tplId,vp.script)
            else:
                ######################################################### js
                if vp.script:
                    p1=vp.script.find("{")
                    p2=vp.script.rfind("}")
                    if 0 <= p1 <= p2:
                        js= vp.script[p1:p2+1]
                    else:
                        raise VBuildException("Component %s contains a bad script" % filename)                    
                else:
                    js="{}"
                
                self.script="""var %s = Vue.component('%s', %s);""" % (name,name,js.replace("{","{template:'#%s'," % tplId,1))

            self.html=transHtml(self.html)
            self.script=transScript(self.script)
            self.style=transStyle(self.style)

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

def mkPythonVueComponent(name,template,code):
    import pscript,json,inspect
    code=code.replace("class Component:","class C:")
    exec(code,globals(),locals())
    assert "C" in locals()
    klass=locals()["C"]
    tpl="""
    <span data--home-manatlan-Documents-python-wuy-examples-vueapp-web-comp>{{name}} {{cpt}}
        {{hashtag}} {{wcpt}}
        <button @click="inc()" ref="btn1">++</button>
        <button @click="dinc()">**</button>
    </span>"""

    computeds=[]
    watchs=[]
    methods=[]
    lifecycles=[]
    classname=klass.__name__
    for oname,obj in vars(klass).items():
        if callable(obj) and not oname.startswith("_") :
            if oname.startswith("COMPUTED_"):
                computeds.append('"%s": %s.prototype.%s,'%(oname[9:],classname,oname))
            elif oname.startswith("WATCH_"):
                if obj.__defaults__:
                    varwatch=obj.__defaults__[0] #not neat (take the first default as whatch var)
                    watchs.append('"%s": %s.prototype.%s,'%(varwatch,classname,oname))
                else:
                    raise VBuildException("name='var_to_watch' is not specified")
            elif oname in ["MOUNTED","CREATED"]:
                lifecycles.append('"%s": %s.prototype.%s,'%(oname.lower(),classname,oname))
            else:
                methods.append('"%s": %s.prototype.%s,'%(oname,classname,oname))

    methods="\n".join(methods)
    computeds="\n".join(computeds)
    watchs="\n".join(watchs)
    lifecycles="\n".join(lifecycles)

    pyjs=pscript.py2js(code).replace("_s_","$") #https://pscript.readthedocs.io/en/latest/api.html

    return """
var %(name)s=(function() {

    %(pyjs)s

    return Vue.component('%(name)s',{
        "name": %(name)s,
        "props": %(classname)s.prototype.props,
        "template": "%(template)s",
        "data": function() {
            return JSON.parse(JSON.stringify( new %(classname)s() ));
        },
        "computed": {
            %(computeds)s
        },
        "methods": {
            %(methods)s
        },
        "watch": {
            %(watchs)s
        },
        %(lifecycles)s
    })
})();

    """ % locals()


def render(filename,content=None):
    isPattern=lambda f: ("*" in f) or ("?" in f)
    if content:
        if isPattern(filename): raise VBuildException("Can't have a pattern name when content is provided !")
        return VBuild(filename,content)
    else:
        files=[filename] if not isinstance(filename,list) else filename
        files=[glob.glob(i) if isPattern(i) else [i] for i in files]
        files=list(itertools.chain(*files))
        return sum( [VBuild(f) for f in files] )
            


if __name__=="__main__":
    exec(open("./tests.py").read())
