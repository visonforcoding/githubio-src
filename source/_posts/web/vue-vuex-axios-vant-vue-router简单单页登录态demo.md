---
title: vue+vuex+axios+vant+vue-router简单单页登录态demo
date: 2020-09-15 18:12:12
tags: web
---

![](http://img.rc5j.cn/blog20200915182645.png)

<!--more-->

## 创建vant项目

```shell
# 安装 Vue Cli
npm install -g @vue/cli

# 创建一个项目
vue create hello-world

# 创建完成后，可以通过命令打开图形化界面，如下图所示
vue ui

# 或者 通过 yarn 安装

yarn add vant
```
![](http://img.rc5j.cn/blog20200915181419.png)

在图形化界面中，点击`依赖` -> `安装依赖`，然后将 `vant` 添加到依赖中即可。

## vue-router

```shell
yarn add vue-router
```

```html
<template>
  <div id="app">
    <van-nav-bar
    title="标题"
    left-text="返回"
    right-text="按钮"
    left-arrow
    @click-left="onClickLeft"
    @click-right="onClickRight"
      />
    <router-view></router-view>
    <van-tabbar v-model="active">
      <van-tabbar-item icon="home-o" to="/">主页</van-tabbar-item>
      <van-tabbar-item icon="search">标签</van-tabbar-item>
      <van-tabbar-item icon="friends-o">标签</van-tabbar-item>
      <van-tabbar-item icon="user-o" to="/user/detail">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template><template>
  <div id="app">
    <van-nav-bar
    title="标题"
    left-text="返回"
    right-text="按钮"
    left-arrow
    @click-left="onClickLeft"
    @click-right="onClickRight"
      />
    <router-view></router-view>
    <van-tabbar v-model="active">
      <van-tabbar-item icon="home-o" to="/">主页</van-tabbar-item>
      <van-tabbar-item icon="search">标签</van-tabbar-item>
      <van-tabbar-item icon="friends-o">标签</van-tabbar-item>
      <van-tabbar-item icon="user-o" to="/user/detail">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template>
```

路由配置和登录态控制

```js
import Vue from 'vue'
import VueRouter from 'vue-router'
// import store from '@/store'
// import layout from '@/layout/layout'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import("@/views/Home")
  },
  {
    path: '/user/detail',
    name: 'user_detail',
    meta:{
      requireLogin:true
    },
    component: () => import("@/views/User/detail.vue")
  },
  {
    path: '/login',
    name: 'login',
    meta:{
      requireLogin:false
    },
    component: () => import("@/views/Login/login.vue")
  },

]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  const token = sessionStorage.getItem('token');
  // store.getters('isLogin')
  if (to.meta.requireLogin) {
    //需要检测登录
    if (token) {
      next();
    } else {
      console.log('前往登录...')
      next({
        path: '/login'
      });
    }
  } else {
 
    next();
  }
})

export default router


```
![](http://img.rc5j.cn/blog20200915181827.png)



## 登录

引入`axios`

```
yarn add axios
```

```js
import { login } from "@/api/loginReq";
export default {
    data() {
    return {
      loading: false,
      loginInfo:{
          username:"",
          pwd:""
      }
    };
  },
  methods: {
    onSubmit(values) {
      this.loading = true;
      login(this.loginInfo).then((response) => {
        console.log(response);
        if(response.code===0){
            sessionStorage.setItem('token',response.data.username);
        }
        this.$router.push('/')
      });
      this.loading = false;
    },
  }
}
```

