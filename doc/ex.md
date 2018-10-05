```html
<template>
    <div>
        {{name}} : {{cpt}} <button @click="inc()">+1</button>
    </div>
</template>
<script lang="python">

class Component:
    def __init__(self, name):   # name is a props !
        self.cpt=0
    def inc(self):
        self.cpt+=1

</script>
<style scoped>
:scope {background:yellow}
</style>
```

```html
<template>
    <div>
        {{name}} : {{cpt}} <button @click="inc()">+1</button>
    </div>
</template>
<script>
    
export default {
  props: ["name"],
  data: function() {
    return { cpt: 0 };
  },
  methods: {
    inc: function() {
      this.cpt+=1;
    }
  }
}
    
</script>
<style scoped>
:scope {background:yellow}
</style>
```
