---
title: Vue 3.0 笔记
categories:
  - 前端
description: "Patrick Collins-区块链学习笔记"
date: 2024-03-17 14:11:40
excerpt: "Vue3.0的入门笔记，特色的compositionAPI写法，可读性和可维护性得到了大幅的提升，再加上各种组件库的支持，文档齐全，非常便于使用。"
tags:
    - Vue3.0
    - Typescript
---


## 前言

因为我是先前并没有接触Vue3，因此这份笔记很基础很基础，尽量都写成傻瓜式的了，当然也有可能有些地方写的不是很清楚，毕竟最初的目的就是为了写给我自己看的，至于之后会不会再深入学习Typescript和Javascript，这谁又晓得呢？反正我修燃气用是不上这个。

## 工具包

课程链接：【尚硅谷Vue3入门到实战，最新版vue3+TypeScript前端开发教程】 https://www.bilibili.com/video/BV1Za4y1r7KE/?share_source=copy_web&vd_source=d4c8e690ada3240d323ff6b395a76451

## Vue3简介

Vue3，截止至2023年10月，最新公开版本为3.3.4

## Vue创建工程

### 基于vite创建

新的前端构建工具，特点如下：

> - 热重载
> - 对`TS`、`JSX`、`CSS`支持开箱即用
> - 按需编译

webpack与vite构建对比图如下：

<img src="/img/Vue3_note/image-20240105103235439.png" alt="image-20240105103235439"  />

终端创建指令：

```terminal
npm create vue@latest
```

![image-20240423215020646](/img/Vue3_note/image-20240423215020646.png)

![image-20240105104452696](/img/Vue3_note/image-20240105104452696.png)

完成之后记得随手清楚asset目录下的css样式文件

### 工作目录介绍

- /**public**
	用于存放网页顶端的图标

![image-20240105104835729](/img/Vue3_note/image-20240105104835729.png)

- /**src**
	工作目录



- /**node_modules**

	执行`npm i`，下载依赖，会生成`node_modules`这个文件夹
	作用：写了前端常用文件（如.jpg,.txt）等等，再通过`env.d.ts`中的以下代码告诉Vue

```typescript
/// <reference types="vite/client" />
```

- **/index.html**
	入口文件

	

- /**package.json**
	包的声明文件

	

- /**vite.config.ts**
	工程的配置文件，配置插件等等



- **/src/components**
	用于存放组件

![image-20240105120758018](/img/Vue3_note/image-20240105120758018.png)

## 编写一个App组件

在main.ts中

```typescript
import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')
```

`createApp`:一个用于“造花盆”的方法

`App`：从`App.vue`中引用，是一个根组件，可以看作是一朵花，包括之后写的`A.vue`、`B.vue`，其实都是安装在根组件上的组件，类似“花上的叶子”，它们直接或间接下载在`App.vue`上

`createApp(App).mount('#app')`：将app传入`createApp()`中，创建一个名叫App的互联网应用，并且它的根组件叫`App`；`mount`：挂载，将App摆在名为app的容器中。

vue组件中，包含以下内容

```vue
<template>
    <!-- html -->
    <div class="app">
        <hl>你好</hl>
    </div>
</template>
<script lang="ts">
//  JS或者TS
export default{
    name:'App' //组件名
}
</script>

<style>
/* 样式 */
.app{
    background-color: #ddd;
    box-shadow: 0 0 10px;
    border-radius: 10px;
    padding: 20px;
}
</style>
```

之后运行 `npm run dev`，`在 Local:   http://localhost:5173/`中查看

![image-20240105155229131](/img/Vue3_note/image-20240105155229131.png)

## 总结

- `vite`项目中，`index.html`是项目的入口文件，在项目最外层
- 加载`index.html`后，`vite`会解析`<script type="module" src="/src/main.ts"></script>`指向的js
- vue3是通过createApp的函数创建一个应用实例

## OptionAPI

这是Vue2的语法

```html
<!-- Vue2 写法-->
<template>
    <!-- html -->
    <div class="person">
        <h2>姓名:{{ name }}</h2>
        <h2>年龄:{{ age }}</h2>
        <button @click="changeName">修改名字</button>
        <button @click="changeAge">修改年龄</button>
        <button @click="showTel">联系方式</button>
    </div>
</template>
<script lang="ts">
export default {
    name: 'Person',//组件名
    data() {
        return {
            name: '张三',
            age: 18,
            tel: '18019328622'
        }
    },
    methods: {
        showTel() {
            alert(this.tel)
        },
        changeName() {
            this.name = '李四'
        },
        changeAge() {
            this.age += 1
        }
    }
}
</script>
```

在'枝干组件'`App.vue`中导入并引用

```typescript
import Person from './components/Person.vue'
export default {
    name: 'App',//组件名
    components: { Person }//注册组件
}
```

```html
<template>
    <!-- html -->
    <div class="app">
        <hl>你好啊！</hl>
        <Person />
    </div>
</template>
```

效果如下

![image-20240108173531398](/img/Vue3_note/image-20240108173531398.png)

### 弊端

optionAPI的语法弊端不难看出，数据、方法、计算属性都是分散在data、methods、computed中，想要新增功能就需要对上述进行修改，这显然是不便于维护和复用的。

## compositionAPI

### setup概述

与optionalAPI不同，compositionAPI将组件的数据、方法、计算属性集中在一个名为setup()的方法中，写法如下：

```typescript
<script lang="ts">
export default {
    name: 'Person',//组件名
    setup() {
        //setup中的this是undefined，vue3中已经开始弱化this了
        //数据
        //此时的name，age，tel不是响应式的
        let name = '张三'
        let age = 18
        let tel = '18019328622'
        //方法
        function changeName() {
            name = '李四'  //name确实修改了，但不是响应式的
        }
        function changeAge() {
            age += 1
        }
        function showTel() {
            alert(tel)
        }
        //必须要给予一个返回值，否则外部接收不到这些数据
        return { name, age, changeName, changeAge, showTel }
    }
}
</script>
```

值得一提的是，vue2中的选项式语法和vue3中的新语法是可以同时出现的，并且由于setup的执行优先级高于optionalAPI中的内容，这导致optinalAPI中的内容可以访问到setup中的数据变量，但setup不能访问到optionalAPI中的数据变量，用例如下：

```typescript
<script lang="ts">
export default {
    name: 'Person',//组件名
    beforeCreate() {
        console.log('beforeCreate')
    },
    data() {
        return {
            a: this.name
        }
    },
    setup() {
        //setup中的this是undefined，vue3中已经开始弱化this了
        //数据
        //此时的name，age，tel不是响应式的
        let name = '张三'
        let age = 18
        let tel = '18019328622'
        //方法
        function changeName() {
            name = '李四'  //name确实修改了，但不是响应式的
        }
        function changeAge() {
            age += 1
        }
        function showTel() {
            alert(tel)
        }
        return { name, age, changeName, changeAge, showTel }
    }
}
</script>
```

![image-20240108233851273](/img/Vue3_note/image-20240108233851273.png)

### setup的语法糖

```typescript
<script lang="ts">
export default {
    name: 'Person',//组件名
}
</script>

<script lang="ts" setup>
let name = '张三'
let age = 18
let tel = '18019328622'
//方法
function changeName() {
    name = '李四'  //name确实修改了，但不是响应式的
}
function changeAge() {
    age += 1
}
function showTel() {
    alert(tel)
}
</script>
```

像这样编写可以不用写setup的返回值

#### 插件配置方法

如果想将上述合二为一，可以下载插件，指令 `npm i vite-plugin-vue-setup-extend -D`

在`vite.config.ts`中进行配置插件，**其他插件方法也是类似**

```typescript
 import VueSetupExtend from 'vite-plugin-vue-setup-extend'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    VueSetupExtend()
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})

```

最后对上述两个script合二为一

```typescript
<script lang="ts" setup name="Person123">
let name = '张三'
let age = 18
let tel = '18019328622'
//方法
function changeName() {
    name = '李四'  //name确实修改了，但不是响应式的
}
function changeAge() {
    age += 1
}
function showTel() {
    alert(tel)
}
</script>
```

效果如下：

![image-20240109132721613](/img/Vue3_note/image-20240109132721613.png)

## 响应式

响应式:能够实时变化的数据

### 响应式数据

```typescript
//引用
import { ref } from 'vue'
//包裹
let name = ref('张三')
let age = ref(18)
let tel = '18019328622'
//方法
function changeName() {
    name.value = '李四'
}
function changeAge() {
    age.value += 1
}
function showTel() {
    alert(tel)
}
```

> 觉得频繁写.value很麻烦？不妨试试volar
>
> <img src = "/img/Vue3_note/image-20240128222423403.png" align="left">

### 响应式对象

响应式对象:被`reactive`包裹过后的对象

```typescript
import {reactive} from 'vue'
    //data
    let car = reactive({ brand: '奔驰', price: 100 })
    let games = reactive([
        {id:'0000001',name:'AAA1'},
        {id:'0000001',name:'AAA1'},
        {id:'0000001',name:'AAA1'}
    ])
    let obj =reactive({
        a:{
            b:{
                c:666
            }
        }
    })
    function changePrice(){
        car.price +=10
    }
    function changeName(){
        games[0].name = 'BBB1'
    }
    function changeObj(){
        obj.a.b.c = 999
    }

```

### 使用ref定义对象类型的响应数据

```typescript
import { ref } from 'vue'
//data
let car = ref({ brand: '奔驰', price: 100 })
let games = ref([
    { id: '0000001', name: 'AAA1' },
    { id: '0000001', name: 'AAA1' },
    { id: '0000001', name: 'AAA1' }
])
function changePrice() {
    car.value.price += 10
    console.log(car.value.price)
}
function changeName() {
    games.value[0].name = 'BBB1'
}
```

结果：

![image-20240128220343854](/img/Vue3_note/image-20240128220343854.png)

可以看出表面是`ref`包裹的对象，但是实际还是使用`reactive`包裹实现的

### ref和reactive的区别

|   名称   |                           可以定义                           |
| :------: | :----------------------------------------------------------: |
|   ref    |           基本类型、对象类型的响应式数据[层级不深]           |
| reactive | 可以定义：对象类型的响应式数据[层级深] <br />重新分配会丢失响应式的属性[^1] |

> [^1]: 对已经用`reactive`分配好的响应式对象，重新覆写一个对象会使新的对象失去响应式
>
> ```typescript
> import { ref } from 'vue'
> //data
> let car = ref({ brand: '奔驰', price: 100 })
> //method
> function changeCar(){
>     car.value={brand:'BYD',price:20}
> }
> ```
>
> 此时一旦使用changeCar()这个方法，那么奔驰就会被BYD覆盖并且覆盖它的BYD不具备响应式
>
> 可以使用Object.assign(obj1,obj2)来解决，如下：
>
> ```typescript
> let car = reactive({ brand: '奔驰', price: 100 })
> //method
> function changeCar(){
>     Object.assign(car,{ brand: 'BYD',price: 20})
> }
> ```
>
> ref不需要这么写
>
> ```typescript
> let car = ref({ brand: '奔驰', price: 100 })
> let games = ref([
>     { id: '0000001', name: 'AAA1' },
>     { id: '0000001', name: 'AAA1' },
>     { id: '0000001', name: 'AAA1' }
> ])
> //method
> function changePrice() {
>     car.value.price += 10
>     console.log(car.value.brand)
> }
> function changeName() {
>     games.value[0].name='BBB1'
> }
> function changeCar(){
>     // Object.assign(car,{ brand: 'BYD',price: 20})
>     car.value = { brand: 'BYD',price: 20}
> }
> ```
>
> 原因是ref的对象覆盖是发生在car.value上的

### toRefs和toRef

```typescript
import { ref,reactive,toRefs,toRef } from 'vue'
//data
let person = reactive({
    name:"张三",
    age:18
})
let {name,age} = toRefs(person)
let age_2 = toRef(person,'age')
//method
function changeName(){
    name.value+='~'
}   
function changeAge(){
    age.value+=1
}
```

toRefs会接收一组由reactive构成的对象，然后把对象中的每一组key,value都拎出来，形成一个新的对象（依然具备响应式的属性）;

toRef只会接受由reactive构成的对象当中的一个元素

## computed计算属性

```vue
<template>
<!-- html -->
<div class="person">
    <!-- 这样↓写是单向绑定 -->
    <!-- 姓：<input type="text" :value="firstName"><br>  -->
    姓：<input type="text" v-model="firstName"><br>
    名：<input type="text" v-model="lastName"><br>
    全名：<span>{{ fullName }}</span><br>
    <button @click="changeFullName">修改全名</button>
    </div>
</template>

<script lang="ts" setup name="Person123">
    import { ref, computed } from 'vue'
    let firstName = ref('张')
    let lastName = ref('三')
    //如此定义的计算属性是只读的
    // let fullName = computed(()=>{
    //     return firstName.value.slice(0,1).toUpperCase()+firstName.value.slice(1)+'-'+lastName.value.slice(0,1).toUpperCase()+lastName.value.slice(1)
    // })
    //如此定义的计算属性可读可写
    let fullName = computed({
        get() {
            return firstName.value.slice(0, 1).toUpperCase() + firstName.value.slice(1) + '-' + lastName.value.slice(0, 1).toUpperCase() + lastName.value.slice(1)
        },
        set(val) {
            const [str1, str2] = val.split('-')
            firstName.value = str1
            lastName.value = str2
        }
    })
    //method
    function changeFullName() {
        fullName.value = 'li-si'
    }
</script>
```

上面代码段`let fullName = computed({//略})`相比于function(){ }，具备了缓存，只有计算属性依赖的数据发生变化时才会重新计算，数据不变即便是重复调用也不会反复执行computed中的内容;

## Watch监视

watch基本格式：

```txt
import { watch } from 'vue'
watch(obj,func,config) //(被监视的数据，监视的回调，监视的配置)
```

它能够监视：

```txt
一个有返回值的函数，ref，reactive响应式对象，或者由以上组成的数组
```

### 监视【ref】定义的【基本类型】数据

```vue
<template>
    <!-- html -->
    <div class="person">
       <h1>情况一，监视[ref]定义的[基本类型]数据</h1>
       <h2>当前求和为:{{ sum }}</h2>
       <button @click="changeNum">sum++</button>
    </div>
</template>

<script lang="ts" setup name="Person123">
import { ref, watch } from 'vue'
//data
let sum = ref(0);
//method
function changeNum(){
    sum.value+=1;
}
watch(sum,(newValue,oldValue)=>{
    console.log('sum变化了',newValue,oldValue)
})
</script>
```

关于停止监视以及箭头函数的补充：

```typescript
const stopWatch =watch(sum,function(newValue,oldValue){
    console.log('sum变化了',newValue,oldValue)
    if (newValue>=10){
        stopWatch()
    }
    return 0
})
```

箭头函数就是**不需要**返回值(但是可以有)的function

### 监视【ref】定义的【对象类型】数据

```vue
<template>
    <!-- html -->
    <div class="person">
       <h1>情况二，监视[ref]定义的[对象类型]数据</h1>
       <h2>姓名：{{ person.name }}</h2>
       <h2>年龄：{{ person.age }}</h2>
       <br>
       <button @click="changeName">修改名字</button>
       <button @click="changeAge">修改年龄</button>
       <button @click="changePerson">修改人</button>
    </div>
</template>

<script lang="ts" setup name="Person123">
import { ref, watch } from 'vue'
//data
let person =ref({
    name:"张三",
    age:18,
})
//method
function changeName(){
    person.value.name+="~"
}
function changeAge(){
    person.value.age+=1
}
function changePerson(){
    person.value={name:"李四",age:22}
}
//watch
watch(person,(newValue,oldValue)=>{
    console.log('person变化了',newValue,oldValue)
},{deep:true})
</script>
```

如上，但是和监视基础类型相比，代码变化不大

注意到，ref的替换对象是新旧替换，地址发生变化

![image-20240201213743914](/img/Vue3_note/image-20240201213743914.png)

### 监视【reactive】定义的【对象类型】数据

```vue
<template>
    <!-- html -->
    <div class="person">
       <h1>情况三，监视[reactive]定义的[对象类型]数据</h1>
       <h2>姓名：{{ person.name }}</h2>
       <h2>年龄：{{ person.age }}</h2>
       <br>
       <button @click="changeName">修改名字</button>
       <button @click="changeAge">修改年龄</button>
       <button @click="changePerson">修改人</button>
    </div>
</template>

<script lang="ts" setup name="Person123">
import { reactive, watch } from 'vue'
//data
let person =reactive({
    name:"张三",
    age:18,
})
//method
function changeName(){
    person.name+="~"
}
function changeAge(){
    person.age+=1
}
function changePerson(){
    Object.assign(person,{name:"李四",age:22})
}
//watch
//监视reactive定义的对象，会默认开启深度监视，且无法手动关闭
watch(person,(newValue,oldValue)=>{
    console.log('person变化了',newValue,oldValue)
})
</script>
```

效果：

![image-20240201212634644](/img/Vue3_note/image-20240201212634644.png)

可以注意到reactive替换对象是值覆盖，地址没有发生变化

### 监视【ref】或【reactive】定义的对象当中的属性

```vue
<template>
    <!-- html -->
    <div class="person">
        <h1>情况四，监视[ref,reactive]定义的[对象类型]数据中的某个属性</h1>
        <h2>姓名:{{ person.name}}</h2>
        <h2>年龄:{{ person.age}}</h2>
        <h2>汽车:{{ person.car.c1}}\{{ person.car.c2 }}</h2>
        <button @click="changeName">修改名字</button>
        <button @click="changeAge">修改年龄</button>
        <button @click="changeCar1">修改第一台车</button>
        <button @click="changeCar2">修改第二台车</button>
        <button @click="changeCar">修改全部车</button>
    </div>
</template>

<script lang="ts" setup name="Person123">
import {reactive,watch} from 'vue'
//data
let person  =reactive({
    name:"张三",
    age:18,
    car:{
        c1:"奔驰",
        c2:"宝马",
    }
})
//method
function changeName(){
    person.name+='~'
}
function changeAge(){
    person.age+=1
}
function changeCar1(){
    person.car.c1='雅迪'
}
function changeCar2(){
    person.car.c2='爱玛'
}
function changeCar(){
    person.car={c1:'五菱',c2:'BYD'}
}
//watch
watch (()=>{return person.name},(newValue,oldValue)=>{
    console.log('person.name变化了',newValue,oldValue)
})
watch (()=>person.car,(newValue,oldValue)=>{
    console.log('person.car变化了',newValue,oldValue)
},{deep:true})
</script>
```

监视基本类型数据的时候，需要将其写成函数式；

监视对象类型的时候，**最好**将其写成函数式（可以不写，但是有局限性）

### 监视上述多个数据

```typescript
watch ([()=>person.name,person.car],(newValue,oldValue)=>{
    console.log('person.car变化了',newValue,oldValue)
},{deep:true})
```

拿个数组包起来就行，数组里面不一定一定要是程式，也可以是对象，看需求

### watchEffect

watchEffect可以自动执行监听，不需要指出监听对象

而watch需要指明监听对象

```typescript
watchEffect(()=>{
    if(person.age>=20||其他条件){
        console.log("发送请求")
    }
})
```

## ref的标签属性

```vue
<!-- 
Person.vue 
-->
<template>
    <!-- html -->
    <div class="person">
        <h1>标签的ref属性</h1>
        <h2 ref="title2">北京</h2>
        <button @click="showlog">点我输出</button>
    </div>
</template>

<script lang="ts" setup name="Person123">
import {ref} from 'vue'
//data
let title2 = ref()
let a = ref(0)
let b = ref(1)
let c = ref(2)
//method
function showlog(){
    console.log(title2.value)
}
defineExpose({a,b})//穿过保护性机制让外界可以看到
</script>
```

```vue
<!-- 
App.vue 
-->
<template>
    <!-- html -->
    <div class="app">
        <button @click="showlog">测试</button>
        <Person ref ="ren"/>
    </div>
</template>
<script lang="ts" setup name="App">
//  JS或者TS
import Person from './components/Person.vue'
import {ref} from 'vue'
//data
let ren = ref()
//method
function showlog(){
    console.log(ren.value)
}
</script>
```

点击测试按钮，会输出`Person`的组件对象，如果没有`defineExpose()`那么输出的组件对象里是看不到`Person`组件中定义的a，b，c，这也是防止多人开发的时候，命名冲突。

ref组件输出的特点一方面是收到保护性机制（这是使用id所不具备的），另一方面也是具有响应式的特性，就是可以数据变化的时候相互传递并且快速更新。

## 回顾TS中的接口和泛型

```typescript
//types/index.ts
//定义一个接口用于限制person对象的具体属性
export interface PersonInter{
    id:string,
    name:string,
    age:number
}
export interface Personouter{
    id:string,
    name:string,
    age:number
}
export type Persons =PersonInter[]
```

可以用它来约束变量

```vue
<!-- Person.vue -->
<script lang="ts" setup name="Person123">
import { type PersonInter, type Persons } from '@/types'
let person: Persons|PersonInter = [
    { id: '123', name: "zhangsan", age: 60 },
    { id: '123', name: "zhangsan", age: 60 },
]
let person2: Persons|PersonInter|Personouter = 
    { id: '123', name: "zhangsan", age: 60 },
</script>
```

## props的使用

简而言之就是**爸爸给儿子传话**

```vue
<!-- App.vue -->
<template>
    <!-- html -->
	<!-- 爸爸给儿子传参 -->
    <Person  a="hello" :list = "person"/>

</template>
<script lang="ts" setup name="App">
//  JS或者TS
import Person from './components/Person.vue'
import { type PersonInter, type Personouter, type Persons } from '@/types'
import { reactive } from 'vue'
let person: Persons | PersonInter = [
    { id: '123', name: "zhangsan", age: 60 },
    { id: '123', name: "zhangsan", age: 60 },
]
</script>
```

```vue
<!-- Person.vue -->
<template>
    <!-- html -->
    <div class="person">
        <ul>
            <!-- v-for遍历 -->
            <li v-for="personObj in list" :key="personObj.id">
                {{ personObj.name }} -- {{ personObj.age }}
            </li>
        </ul>
    </div>
</template>

<script lang="ts" setup name="Person123">
import { defineProps, withDefaults } from 'vue';
import { type Persons } from '@/types';
//接收
// defineProps(['a', 'list'])

//接收a，同时将props保存起来
// let x = defineProps(['a'])
// console.log(x.a)

//接收加限制类型
// defineProps<{ list: Persons }>()

//接收list+限制类悉尼港+限制必要性+指定默认值
//withDefaults(defineProps(),{})
withDefaults(defineProps<{ list?: Persons }>(), {//第二个参数只接收函数返回值类型
    list: () => [
        { id: '123', name: "zhangsan", age: 60 },
        { id: '123', name: "zhangsan", age: 60 },
    ]
})

</script>
```

效果：

![image-20240310184451213](/img/Vue3_note/image-20240310184451213.png)

## 生命周期

组件的生命周期

> - **时刻**[调用特定的函数]
> - **创建**[setup自动执行]
> - **挂载**[挂载前`onBeforeMount()`，挂载完毕`onMounted(`)]
> - **更新**[更新前`onBeforeUpdate()`，更新完毕`onUpdated()`]
> - **卸载**[销毁前`onBeforeUnmount()`，销毁完毕`onUnmounted()`]

生命周期、生命周期函数、生命周期钩子

```vue
<!-- Person.vue -->
<template>
    <!-- html -->
    <div class="person">
        <ul>{{ sum }}</ul>
        <button @click="add">点我sum+1</button>
    </div>
</template>
<!-- Person.vue -->
<script lang="ts" setup name="Person123">
import { onBeforeMount, onBeforeUnmount, onBeforeUpdate, onMounted, onUnmounted, onUpdated, ref } from "vue"
let sum = ref(0)
function add() {
    sum.value = sum.value + 1
}
//创建
console.log('创建')
//挂载
onBeforeMount(() => {
    console.log("挂载前")
})
//挂载完毕
onMounted(() => {
    console.log("挂载完毕")
})
//更新前
onBeforeUpdate(() => {
    console.log("更新前")
})
//更新完毕
onUpdated(() => {
    console.log("更新完毕")
})
// 卸载
onBeforeUnmount(()=>{
    console.log("卸载前")
})
//卸载完毕
onUnmounted(() => {
    console.log("卸载完毕")
})
</script>
```

生命周期流程图[来自官网]

<img src="/img/Vue3_note/lifecycle_zh-CN.FtDDVyNA.png" alt="组件生命周期图示" style="zoom:50%;" />

## 自定义hook

```terminal
# 安装axios，非必要，只是此处样例用到了
$ npm i axios
```

```vue
<!-- Person.vue -->
<template>
    <!-- html -->
    <div class="person">
        <h2>{{ sum }}</h2>
        <button @click="add">点我sum+1</button>
        <hr>
        <img v-for="(dog, index) in doglist" :src="dog" :key="index">
        <button @click="getDog">获取dog</button>
    </div>
</template>
<!-- Person.vue -->
<script lang="ts" setup name="Person123">
import useDog from '@/hooks/useDog';
import useSum from '@/hooks/useSum';
const { sum, add } = useSum()
const { doglist, getDog } = useDog()
</script>
```

在`src/hooks`中

```typescript
//useSum.ts
import { ref } from "vue";
export default function () {
  let sum = ref(0);
  function add() {
    sum.value = sum.value + 1;
  }
  return { sum, add };
}
```

```typescript
//useDog.ts
import { reactive } from "vue";
import axios from "axios";
export default function () {
  let doglist = reactive([
    "https://images.dog.ceo/breeds/pembroke/n02113023_4373.jpg",
  ]);
  async function getDog() {
    try {
      let result = await axios.get(
        "https://dog.ceo/api/breed/pembroke/images/random"
      );
      doglist.push(result.data.message);
      console.log(result.data.message);
    } catch (error) {
      alert(error);
    }
  }
  //向外部提供东西
  return { doglist, getDog };
}

```

作用是啥？vue里看着干净些吧，俺也不知道还有没有别的用途了？

## 路由

### 安装和使用

```terminal
#安装vue-router最新版
$npm i vue-router
```

对App.vue稍作调整

```vue
<!-- 
App.vue 
-->
<template>
    <!-- html -->
    <h2>Vue路由测试</h2>
    <!-- 导航区 -->
    <div class="navigate">
        <RouterLink to="/home">首页 </RouterLink>
        <RouterLink to="/news">新闻 </RouterLink>
        <RouterLink to="/about">关于 </RouterLink>
    </div>
    <hr>
    <!-- 展示区 -->
    <div class="main-content" style="border: 1px solid red;height: 300px;width:300px">
        <RouterView></RouterView>
    </div>
</template>
<script lang="ts" setup name="App">
import { RouterView } from 'vue-router';
</script>
```

配置路由配置项`index.ts`

```typescript
//写一个路由器并暴露出去
import { createRouter, createWebHistory } from "vue-router";
import Home from "@/components/Home.vue";
import News from "@/components/News.vue";
import About from "@/components/About.vue";
//创建路由器
const router = createRouter({
  //路由器工作模式,很重要👇👇👇
  history: createWebHistory(),
  routes: [
    // {
    //     path:'路径',
    //     component:组件
    // }
    {
      path: "/home",
      component: Home,
    },
    {
      path: "/news",
      component: News,
    },
    {
      path: "/about",
      component: About,
    },
  ],
});

export default router;

```

在`main.ts`中使用路由器

```typescript
//引入createApp用于创建应用
import { createApp } from "vue";
//引用App根组件
import App from "./App.vue";
import router from "./router";

//创建一个应用
const app = createApp(App);
//使用路由器
app.use(router);
//挂载整个应用到app容器中
app.mount("#app");

```

效果：

![image-20240314224306984](/img/Vue3_note/image-20240314224306984.png)

路由组件：

靠路由的规则渲染出来的：

```typescript
routes: [
    {
        path: '/demo',
        component: demo
    }
]
```

一般组件：

亲手写标签出来的

```html
<demo/>
```

### 路由器工作模式

##### history模式

```typescript
const router = createRouter({
    history: createWebHistory(),
    {
    	path:XXX,
    	component:XXX
	}
})
```

优点：`URL`更加美观，不带有`#`，更接近传统`URL`

缺点：后期项目上线，需要服务端配合处理路径问题，否则刷新会有**404错误**

##### hash模式

```typescript
const router = createRouter({
    history: createWebHashHistory(),
    {
    	path:XXX,
    	component:XXX
	}
})
```

优点：兼容性好，因为不需要服务器端处理路径

缺点：`URL`带有`#`不太美观，**且在`SEO`优化方面相对较差**

### 命名路由

```typescript
  routes: [
    // {
    //     name:'路由名'
    //     path:'路径',
    //     component:组件
    // }
    {
      name: "HOME",
      path: "/home",
      component: Home,
    },
    {
      name: "NEWS",
      path: "/news",
      component: News,
    },
    {
      name: "ABOUT",
      path: "/about",
      component: About,
    },
  ],
```

```vue
    <div class="navigate">
        <!--三种路由跳转方式 -->
        <RouterLink to="/home">首页 </RouterLink>
         <!--注意感叹号 -->
        <RouterLink :to="{ name: 'NEWS' }">新闻 </RouterLink>
        <RouterLink :to="{ path: '/about' }">关于 </RouterLink>
    </div>
```

### 嵌套路由

P.S 路由页面要有`<router-view/>`来承载

子路由

```typescript
  routes: [
    // {
    //   name: "路由名",
    //   path: "/路径",
    //   component: 组件名,
    //   children: [
    //     {
    //       path: "子路由路径",
    //       component: 子路由组件名,
    //     },
    //   ],
    // },
    {
      name: "NEWS",
      path: "/news",
      component: News,
      children: [
        {
          name: 'Detail'
          path: 'detail',
          component: Detail,
        },
      ],
    },
  ],
```

### 路由传参

#### query

```vue
<!-- News.vue -->
<template>
    <!-- html -->
    <div>
        <ul>
            <li v-for="news in newsList" :key="news.id">
                <RouterLink :to="`/news/detail?id=${news.id}&title=${news.title}&content=${news.content}`">{{
                news.title }}</RouterLink>
            </li>
        </ul>
        <div class="main-content" style="border: 1px solid red;height: 300px;width:300px">
            <RouterView></RouterView>
        </div>
    </div>
</template>
<script lang="ts" setup name="News">
import { RouterView } from 'vue-router';
import { reactive } from 'vue'
const newsList = reactive([
    { id: '021120230', title: "基于区块链", content: 'solidity' },
    { id: '021120231', title: "信息管理系统", content: 'python' }
])
</script>
```

```vue
<template>
    <!-- html -->
    <ul>
        <li>编号：{{ route.query.id }}</li>
        <li>标题：{{ route.query.title }}</li>
        <li>内容：{{ route.query.content }}</li>
    </ul>
</template>
<script lang="ts" setup name="Detail">
import { useRoute } from 'vue-router'
let route = useRoute()
```

这个不好用，看看得了

下面是**使用对象传参**

```vue
<!-- News.vue -->
<template>
    <!-- html -->
    <div>
        <ul>
            <li v-for="news in newsList" :key="news.id">
                <RouterLink :to="{
                name: 'Detail',
                query: {
                    id: news.id,
                    title: news.title,
                    content: news.content
                }
            }">{{ news.title }}</RouterLink>
            </li>
        </ul>
        <div class="main-content" style="border: 1px solid red;height: 300px;width:300px">
            <RouterView></RouterView>
        </div>
    </div>
</template>
<script lang="ts" setup name="News">
import { RouterView } from 'vue-router';
import { reactive } from 'vue'
const newsList = reactive([
    { id: '021120230', title: "基于区块链", content: 'solidity' },
    { id: '021120231', title: "信息管理系统", content: 'python' }
])
</script>

```

```vue
<!-- detail.vue -->
<template>
    <!-- html -->
    <ul>
        <li>编号：{{ query.id }}</li>
        <li>标题：{{ query.title }}</li>
        <li>内容：{{ query.content }}</li>
    </ul>
</template>
<script lang="ts" setup name="Detail">
import { toRefs } from 'vue';
import { useRoute } from 'vue-router'
let route = useRoute()
// 不使用toRefs会丢失响应式
let { query } = toRefs(route)
</script>
```

#### params参数

在路由规则中占位

```typescript
    {
      name: "NEWS",
      path: "/news",
      component: News,
      children: [
        {
          name: "Detail",
          path: "detail/:id/:title/:content",
          component: Detail,
        },
      ],
    },
```

```vue
<!-- detail.vue -->
<template>
    <!-- html -->
    <ul>
        <li>编号：{{ route.params.id }}</li>
        <li>标题：{{ route.params.title }}</li>
        <li>内容：{{ route.params.content }}</li>
    </ul>
</template>
<script lang="ts" setup name="Detail">
import { useRoute } from 'vue-router';
const route = useRoute()
console.log(route)
</script>
<style>
/* 样式 */
</style>
```

```vue
<!-- News.vue -->
<template>
    <!-- html -->
    <div>
        <ul>
            <li v-for="news in  newsList " :key="news.id">
                <!-- 第一种写法 -->
                <!-- <RouterLink :to="`/news/detail/${news.id}/${news.title}/${news.content}`">{{ news.title }}
                </RouterLink> -->
                <!-- 第二种写法 -->
                <RouterLink :to="{
                name: 'Detail',
                params: {
                    id: news.id,
                    title: news.title,
                    content: news.content
                }
            } as any">{{ news.title }}
                </RouterLink>
            </li>
        </ul>
        <div class="main-content" style="border: 1px solid red;height: 300px;width:300px">
            <RouterView></RouterView>
        </div>
    </div>
</template>
<script lang="ts" setup name="News">
import { RouterView } from 'vue-router';
import { reactive } from 'vue'
const newsList = reactive([
    { id: '021120230', title: "基于区块链", content: 'solidity' },
    { id: '021120231', title: "信息管理系统", content: 'python' }
])
</script>
```

缺点：

对象参数中不可以包含数组

### 路由props配置

路由规则中配置

```typescript
    {
      name: "NEWS",
      path: "/news",
      component: News,
      children: [
        {
          name: "Detail",
          // path: "detail/:id/:title/:content",//params写法
          path: "detail",
          component: Detail,
          // props: true, //params
          // query写法
          props(route) {
            return route.query;
          },
        },
      ],
    },
```

 ```vue
 <!-- detail.vue -->
 <template>
     <!-- html -->
     <ul>
         <li>编号：{{ id }}</li>
         <li>标题：{{ title }}</li>
         <li>内容：{{ content }}</li>
     </ul>
 </template>
 <script lang="ts" setup name="Detail">
 defineProps(['id', 'title', 'content'])
 </script>
 ```

### replace属性

作用：控制路由跳转时操作浏览器历史记录的模式

浏览器历史记录有两种写入方式，分别为`push`和`replace`

- `push`：追加历史记录
- `replace`：替换当前记录，点击过后不能返回

开启`replace`模式

```vue
<RouterLink replace to="/home">首页 </RouterLink>
```

### 编程式路由导航

使用频率很高，远远大于RouterLink

```vue
<script lang="ts" setup name="Home">
//效果是，点击首页三秒后跳转至新闻页
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter()
onMounted(() => {
    setTimeout(() => {
        router.push('/news')
    }, 3000)
})
</script>
```

### 重定向

将指定路径重定向到另一个路径

在规则中进行修改【此规则包含了所有路由配置写法】

```typescript
//写一个路由器并暴露出去
import { createRouter, createWebHistory } from "vue-router";
import Home from "@/pages/Home.vue";
import News from "@/pages/News.vue";
import About from "@/pages/About.vue";
import Detail from "@/pages/detail.vue";
//创建路由器
const router = createRouter({
  //路由器工作模式
  history: createWebHistory(),
  routes: [
    // {
    //   name: "路由名",
    //   path: "/路径",
    //   component: 组件名,
    //   children: [
    //     {
    //       path: "子路由路径",
    //       component: 子路由组件名,
    //     },
    //   ],
    // },
    {
      name: "HOME",
      path: "/home",
      component: Home,
    },
    {
      name: "NEWS",
      path: "/news",
      component: News,
      children: [
        {
          name: "Detail",
          // path: "detail/:id/:title/:content",//params写法
          path: "detail",
          component: Detail,
          // props: true, //params
          // query写法
          props(route) {
            return route.query;
          },
        },
      ],
    },
    {
      name: "ABOUT",
      path: "/about",
      component: About,
    },
    //重定向
    {
      path: "/",
      redirect: "/home",
    },
  ],
});
//把路由规则暴露出去
export default router;
```

## Pinia

### 安装和部署

**安装**

```terminal
#安装pinia
$npm i pinia
```

**搭建环境**

```typescript
//main.ts
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
//引入pinia
import { createPinia } from "pinia";
const app = createApp(App);
//创建pinia
const pinia = createPinia();
app.use(router);
app.mount("#app");
//安装pinia
app.use(pinia);
```

### 使用

其作用相当于前端的仓库

```typescript
//src/store/count.ts
import { defineStore } from "pinia";

export const useContentStore = defineStore("count", {
  //真正存数据的地方
  state() {
    return {
      sum: 6,
    };
  },
});
```

```typescript
//src/store/talk.ts
import { defineStore } from "pinia";

export const useTalkStore = defineStore("talk", {
  //真正存数据的地方
  state() {
    return {
      talkList: [
        { id: "1", title: "qqqqqqqqqqqqqqqqqqq" },
        { id: "2", title: "wwwwwwwwwwwwwww" },
        { id: "3", title: "eeeeeeeeeeeeeeeeeeeee" },
        { id: "4", title: "rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr" },
      ],
    };
  },
});

```

**调用**

```vue
<!-- components/Love.vue -->
<template>
    <div class="talk">
        <button @click="getTalk">获取一句土味情话</button>
        <ul>
            <li v-for="talk in talkStore.talkList" :key="talk.id">{{ talk.title }}</li>
        </ul>
    </div>
</template>

<script lang='ts' setup name='LoveTalk'>
import axios from 'axios';
import { reactive } from 'vue';
import { nanoid } from 'nanoid'
import { useTalkStore } from '@/store/talk'
const talkStore = useTalkStore()
async function getTalk() {
    //发请求,连用两次解构赋值和一次重命名
    let { data: { content: title } } = await axios.get('https://api.uomg.com/api/rand.qinghua?format=json');
    // 把请求回来的字符串，包装成一个对象
    let obj = { id: nanoid(), title: title }
    console.log(obj)
    //放到数组中
    talkStore.talkList.unshift(obj)//最开始
    // talkList.push(obj)//最末尾
}
</script>
```

```vue
<!-- components/Count.vue -->
<template>
    <div class="count">
        <h2>当前求和为:{{ countStore.sum }}</h2>
    </div>
    <select v-model.number="n">
        <option value="1">1</option>
        <option value="2">2</option>
        <option value="3">3</option>
    </select>
    <button @click="add">加</button>
    <button @click="minus">减</button>
</template>

<script lang='ts' setup name="Count">
import { ref } from 'vue'
import { useContentStore } from '@/store/count'
// countStore是一个响应式reactive对象，
// 并且会自动解构它下面的ref类型数据，因此不需要写.value
const countStore = useContentStore()
console.log('@@@', countStore.sum)

//数据
let n = ref(1) //用户选择的数据

function add() {
    countStore.sum += n.value
}
function minus() {
    countStore.sum -= n.value
}
</script>

```

### 修改数据(三种方式)

```typescript
//components/Count.vue
function add() {
    //<----------第一种修改方式------------->
    // countStore.sum += n.value
    // countStore.school = '鸡大'
    //<----------第二种修改方式------------->
    // 适用于修改多个数据
    // countStore.$patch({
    //     sum: 88,
    //     school: '鸡大'
    // })
    //<----------第二种修改方式------------->
    countStore.increment(n.value)

}
```

```typescript
//src/store/count.ts
import { defineStore } from "pinia";

export const useContentStore = defineStore("count", {
  //actions里放置的是一个个方法，用于相应组件中的“动作”
  actions: {
    increment(value: any) {
      this.sum += value;
    },//很麻烦，日常开发用起来不方便，但是可以模块化，复用它
  },
  //真正存数据的地方
  state() {
    return {
      sum: 6,
      school: "SUES",
    };
  },
});

```

### $subscribe的使用

能够在本地浏览器存储数据，使其不会因为浏览器的刷新而导致数据丢失

还是以土味情话为例

```vue
<!--Love.vue-->
<script lang='ts' setup name='LoveTalk'>
import { useTalkStore } from '@/store/talk'
const talkStore = useTalkStore()
async function getTalk() {
    talkStore.getATalk()
    talkStore.$subscribe((mutate, state) => {
        //mutate表示发生变化的内容
        console.log('talkStore内的数据发生了变化', mutate, state)
        localStorage.setItem('talkList', JSON.stringify(state.talkList))
    })
}
</script>
```

```typescript
//src/store/talk.ts
import { defineStore } from "pinia";
import { nanoid } from "nanoid";
import axios from "axios";
export const useTalkStore = defineStore("talk", {
  actions: {
    async getATalk() {
      //发请求,连用两次解构赋值和一次重命名
      let {
        data: { content: title },
      } = await axios.get("https://api.uomg.com/api/rand.qinghua?format=json");
      // 把请求回来的字符串，包装成一个对象
      let obj = { id: nanoid(), title: title };
      console.log(obj);
      //放到数组中
      this.talkList.unshift(obj); //最开始
      // talkList.push(obj)//最末尾
    },
  },
  //真正存数据的地方
  state() {
    return {
      talkList: JSON.parse(localStorage.getItem("talkList") as string) || [],
    };
  },
});

```

**效果：**

![image-20240317151105751](/img/Vue3_note/image-20240317151105751.png)

### 组合式写法

```typescript
//src/store/talk.ts
import { reactive } from "vue";
export const useTalkStore = defineStore("talk", function a() {
  const talkList = reactive(
    JSON.parse(localStorage.getItem("talkList") as string) || []
  );
  async function getATalk() {
    //发请求,连用两次解构赋值和一次重命名
    let {
      data: { content: title },
    } = await axios.get("https://api.uomg.com/api/rand.qinghua?format=json");
    // 把请求回来的字符串，包装成一个对象
    let obj = { id: nanoid(), title: title };
    console.log(obj);
    //放到数组中
    talkList.talkList.unshift(obj); //最开始
    // talkList.push(obj)//最末尾
  }
  return { talkList, getATalk };
});
```

## 向后端发起请求

核心语句，当然后端要做好跨域访问

```typescript
import axios from "axios"; 
async function Login() {
	let loginMessage = {
        user_id: userid.value,
        password: password.value
    }
 	const response = await axios.post('http://localhost:8080/login', loginMessage);
}
```

写个样例，向后端发送登录请求，并将返回的token存入Pinia中,同时在浏览器也做好存储，避免服务器重启以及刷新浏览器会丢失数据

先新建仓库

```typescript
//store/loginStore.ts
import { defineStore } from "pinia"
import { type LoginResult } from "@/interface/loginResult"
import { ref } from "vue"
export const useLoginStore = defineStore("login", function login() {
    //真正存数据的地方
    const userid = ref(localStorage.getItem("userid") || "")
    const username = ref(localStorage.getItem("username") || "")
    const publicKey = ref(localStorage.getItem("publicKey") || "")
    const konohaToken = ref(localStorage.getItem("konohaToken") || "")
    function Login(loginResult: LoginResult) {
        userid.value = loginResult.user_id
        username.value = loginResult.username
        publicKey.value = loginResult.publicKey
        konohaToken.value = loginResult.konohaToken
    }

    return { userid, username, publicKey, konohaToken, Login }
})

```

`login.vue`中

```typescript
import { useLoginStore } from '@/store/loginStore'
import { ElMessage } from 'element-plus'
const loginStore = useLoginStore()
async function Login() {
    let loginMessage = {
        user_id: userid.value,
        password: password.value
    }
    try {
        const response = await axios.post('http://localhost:8080/login', loginMessage);
        // console.log(loginMessage)
        console.log('send successful:', response.data.data);
        switch (response.data.code) {
            case 200:
                // 登录成功后的处理
                loginStore.Login(response.data.data)
                loginStore.$subscribe((mutate, state) => {
                    //mutate表示发生变化的内容，同时更新浏览器存储
                    console.log('loginStore内的数据发生了变化', mutate, state)
                    localStorage.setItem('userid', state.userid)
                    localStorage.setItem('username', state.username)
                    localStorage.setItem('publicKey', state.publicKey)
                    localStorage.setItem('konohaToken', state.konohaToken)
                })
                ElMessage({
                    message: response.data.msg,
                    type: 'success',
                })
                break
            default:
                //登陆失败或者异常时的处理
                ElMessage({
                    message: response.data.msg,
                    type: 'error',
                })
                //同时清空输入框，这里可以说是非常简单粗暴了
                userid.value =''
                password.value = ''
                break
        }
    } catch (error) {
        console.error('Login failed:', error);
        // 登录失败的处理
    }
}
```

P.S `get`请求要写完整，最后的斜杠不能少

```typescript
const response = await axios.get("http://localhost:8080/showclaims/")
```



