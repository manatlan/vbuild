# Using python component in vue's script

Here is a first version. **vbuild** use and install [pscript](https://pypi.org/project/pscript/) (it comes with **vbuild** for py2 and/or py3 ). **pscript** is used to transpile python to javascript version. A lot of python goodies are usable, but be sure to read the [pscript caveats](https://pscript.readthedocs.io/en/latest/intro.html) before.

**VBuild** needed to create a frame on how to declare a python component (because there was nothing yet, [except that](https://github.com/QQuick/Transcrypt/issues/287)). This frame/definitions may evolve, but **vbuild** will understand the current and the future versions (based on how the class is defined), so the `class Component:` is the first usable version.

I've made a lot of trys, and this one is (IMO) the best (usefull and readable). I'm feeling more and more confortable using python component: life is better without braces ;-) (and syntaxic errors are sorted at compilation/rendering time)

Here is a working component which cover all of the current/implemented features :
- Instanciate the `data`
- `props`
- Access to $attributes (works with $store/[vuex](https://vuex.vuejs.org/))
- Lifecycle events: `created` & `mounted`
- `computed` field
- `watch`ers
    
```html
<template>
    <div>
        {{name}} ({{originalName}})
        <button @click="inc(3)">+3</button>
        <button @click="inc()">+1</button>
        {{cpt}} : {{ccpt}} {{wcpt}}
    </div>
</template>
<script lang="python">
class Component:

    def __init__(self, name="?"):
        print("DATA INIT",name)
        self.cpt=0
        self.wcpt=""
        self.originalName=name  # copy the $props.name

    def inc(self,nb=1):                 # with py3, you can make this a async method !
        print("inc(%s)"%nb,self.name)
        self.cpt+=nb

    def CREATED(self):
        print("CREATED",self.name)

    def MOUNTED(self):
        print("mounted",self.name,"in",self["$parent"]["$options"].name)
        self.inc()

    def COMPUTED_ccpt(self):
        print("COMPUTE",self.name,self.cpt,"changed")
        return self.cpt*"#"

    def WATCH_1(self,newVal,oldVal,name="cpt"):
        print("WATCH",self.name,name,oldVal,"-->",newVal)
        self.wcpt=self.cpt*"+"
        
    def WATCH_2(self,newVal,oldVal,name="name"):    # watch the prop !
        print("WATCH",name,oldVal,"-->",newVal)

</script>
```
With py3 : you can use async/await things in python methods (not in py2 !)


## Features in details

By convention : lowercase methods are classic python methods, uppercase methods are special Vue's [options](https://vuejs.org/v2/api/#Options-Data). **vbuild** transpile the python class to a javascript one, and link methods in the vue's options. (I wanted to use "@decorators", but **pscript** doesn't support them (but in the future))

**pscript** needs to generate js wrapper to python functions : it's called the standard lib.
You can choose to let **vbuild** generate the pscript standard lib, on the fly, for each component, or generate one standard lib for all, depending on your needs. (It could save bandswidth, if you have a lot of Python Components, to opt for the second option)

Just set `vbuild.fullPyComp` (boolean, 3 states), before `vbuild.render`'ing :

```python
vbuild.fullPyComp=True  # (default) each components generate its needs.
vbuild.fullPyComp=False # minimal js transpilation, but vbuild will automatically include the "js standard lib" for you.
vbuild.fullPyComp=None  # minimal js transpilation, but it's up to you to include the js from "pscript.get_full_std_lib()".
```

### Instanciate the data
Like in python, the initialization of the instance is done in the `__init__()`. In this statement, just init your data. All initialized properties will be used in the `data` options of the vue component (which will make them reactives).

(see `def __init__(...)` ^^)


### props
The `props` are declared in the keywords of the `__init__` statement. In the upper example, there is prop called 'name' ; so you can use the component like this :

```html
<comp name="MyName"></comp>
```

The value of `name` will be passed when the `__init__` statement is called (note that `Vue` will create a reactive property (`self.name`) **after** the `__init__` call). But you can use the value of `name` to store it, in the data (like ^^ to keep the original value, for example)

If you use `<comp></comp>` without declaring the prop 'name', `__init__` is called, and `name` will be `undefined` (Note that the reactive property `self.name` will not be created, in this case)

### Access to $attributes

In all component's methods (except `__init__()`), you have access to `$`prefixed things using this syntax:

```python
self["$parent"]
self["$store"].dispatch("myaction",payload)
self["$refs"].btnOk.click()
self["$forceUpdate"]()
```

### Lifecycle events : created & mounted
Currently, there is only 2 lifecyles : but they are the most used IRL apps (But it's very easy to add more, what lifecycle methods do you want to use ??). Just create an uppercase method, with the name of the lifecyle. 

(see `def CREATED(self)` and `def MOUNTED(self)` ^^)

### Computed field
You can create a computed attibute, by declaring an instance method prefixed with "COMPUTED_", the method should return the computed value.

(see `def COMPUTED_ccpt(self)` ^^)

### Watch'ers
You can create a whatcher on a vue attribute, by declaring an instance method prefixed with "WATCH_". This method should have the signature `(self,newVal,oldVal,name="var_to_watch")`.

You should suffix your watch method, to make it unique. The name of the watch'ed attribute should be declared in the `name` argument.

(see `def WATCH_1(...)` and `def WATCH_2(...)` ^^)

Here are valid watchers :
```python
def WATCH_1(self, newVal, oldVal, name="cpt"): pass
def WATCH_2(self, newVal, oldVal, name="$store.state.mylist"): pass
```

You can test that on [vbuild's demo](https://on-the.appspot.com/vbuild/index.html) !

## TODO:

 * add more lifecycle events
 * ability to import things ?
 * use wrapper self._parent -> self["$parent"] ?
 * $store/vuex in python ? ($router/vue-router in python ?)   
