---
title: Gin 笔记
categories:
  - 后端
description: "Patrick Collins-区块链学习笔记"
date: 2024-04-01 14:11:40
tags:
  - Gin
  - Golang
---

​	Gin 是 Golang 常用的一种轻量型框架，可以快速部署且可以自定义项目结构，可塑性和操作性很强，搭配各种库可以实现非常不错的效果，精简的同时性能也丝毫不落下风，可以说是兼顾了性能和轻便程度，学习和开发难度较低于 Springboot 那种航空母舰型框架，但是想要使用的得心应手还需要对后端和 Golang 原生有一定的熟悉程度。

<!-- more -->

> - Created by Typora
> - Author: LRay-iu
> - createTime: 2024-03-28 13:36
> - updateTime: 2024-04-01 10:43

## 前言

这也不知道是我开的第几份笔记了，主打的是记录 Gin 后端的**搭建**，内容应该不会很多，毕竟 Gin 和 Flask 一样，是一个轻量型的框架，主打的是快速开发，但是 Gin 的响应速度上比 Flask 快的不是一点点，语言原生支持上 Golang 不需要额外的库也能完成协程，管道，映射等等功能。但是和 Goframe、SpringBoot 那些航空母舰级的框架不太一样，Gin 本身像个光杆司令，有不少功能是需要引入其他模块来实现的，比如 Gorm，godotenv 等等；

至于 Goframe，原先确实萌生过好好学习它的想法，不过现在情况特殊，一来是原先投的岗位貌似莫得了，二来是毕设老师催挺急的，没时间开新坑了，抓紧写完抓紧 Gap。

## 工具包

Gin 快速搭建教程[来自 B 站'慕课网']：https://www.bilibili.com/video/BV1Jy4y1F7RG/

Gin 中文开发文档：[快速入门 | Gin Web Framework (gin-gonic.com)](https://gin-gonic.com/zh-cn/docs/quickstart/)

Gorm 中文开发文档：[GORM 指南 | GORM - The fantastic ORM library for Golang, aims to be developer friendly.](https://gorm.io/zh_CN/docs/)

## 开发报错

> - 如果开发过程中出现`404-not-found`，请先检查请求模式是`GET`还是`POST`
>
> - 如果 gorm 查询结果为空且数据库查询正常，请检查 gorm 标签是否正确`gorm:"column:publicKey"`
>
> - 如果开发过程中，在数据库`Mysql`中设置了默认值，但是不会启用，可能是 gorm 给覆盖了，需要在`gorm`这重新定义
>
>   ```go
>   Isvisual       int     `gorm:"column:isvisual;default:1"`
>   Status         int     `gorm:"column:status;default:1"`
>   ```
>
> - 如果 json 绑定失败，请检查结构体定义的变量头是否小写（被定义成私有变量了）
>
> - `sqlx` 在把`timestamp`转为`go`的`time.Time`报错`Scan error on column index 6: unsupported Scan, storing driver.Value type []uint8 into type *time.Time`,需要在数据库配置时加上`parseTime=true`，即:
>
>   ```go
>   Mysqldb = fmt.Sprintf("%s:%s@tcp(127.0.0.1:3306)/minato_sys?charset=utf8mb4&parseTime=true", name, password)
>   ```
>
>   不过，这一点我已经在数据库配置那一环修改过了，按着笔记走应该碰不到这个错误。
>
> -

## Gin 创建工程

```terminal
# 初始化项目
$ go mod init gin-Minato

# 安装Gin框架
$ go get github.com/gin-gonic/gin@latest

# 安装热加载插件fresh
$ go install github.com/pilu/fresh@latest
$ go get github.com/pilu/fresh
$ fresh

# 安装godotenv插件
$ go get github.com/joho/godotenv

# 安装Gorm
$ go get -u gorm.io/gorm
$ go get -u gorm.io/driver/mysql  #你用什么就下什么，这边以mysql为例

# 安装session和redis
$ go get github.com/gin-contrib/sessions
$ go get github.com/gin-contrib/sessions/redis

# 安装JWT-go
$ go get github.com/dgrijalva/jwt-go

```

### 测试代码

```go
package main

import (
	"github.com/gin-gonic/gin"
	"net/http"
)

func main() {
	r := gin.Default()
	r.GET("/", func(ctx *gin.Context) {
		ctx.String(http.StatusOK, "hello world!")
	})
	//r.Run(":8080")
	r.Run()
}
```

运行：

```terminal
# 启动
$ go run main.go
# 如果安装过fresh，则可以
$ fresh
```

## 路由分配

步骤：在`router.go`中创建`gin引擎`，在`main.go`里调用

```go
//routers.go
package router

import (
	"github.com/gin-gonic/gin"
	"net/http"
)

func Router() *gin.Engine {
	r := gin.Default()

	user := r.Group("/user")
	{
		user.GET("/", func(ctx *gin.Context) {
			ctx.String(http.StatusOK, "hello world1!")
		})
		user.PUT("/add", func(ctx *gin.Context) {
			ctx.String(http.StatusOK, "hello world2!")
		})
		user.POST("/post", func(ctx *gin.Context) {
			ctx.String(http.StatusOK, "hello world3!")
		})
		user.DELETE("/delete", func(ctx *gin.Context) {
			ctx.String(http.StatusOK, "hello world4!")
		})
	}
	return r
}

```

在`main.go`中调用

```go
package main

import "gin-Minato/router"

func main() {
	r := router.Router()
	//r.Run(":8080")
	r.Run()
}

```

OK 完成，终于不用全写在 main 文件里了，不过这个写法还是不够简洁，并不符合官方文档

## 将处理方法外置到其他包裹

这是我个人对它的叫法，就是提一嘴，没什么技术含量，但是能够让项目更加简洁清晰，易于维护。

定义控制器中常用的方法和数据结构

```go
//controller/commen.go
package controller

import "github.com/gin-gonic/gin"

type JsonStruct struct {
	Code  int         `json:"code"`  //返回状态码
	Msg   interface{} `json:"msg"`   //返回的提示语
	Data  interface{} `json:"data"`  //返回数据
	Count interface{} `json:"count"` //返回条数
}

type JsonErrStruct struct {
	Code int         `json:"code"` //返回状态码
	Msg  interface{} `json:"msg"`  //返回的提示语
}

func ReturnSuccess(c *gin.Context, code int, msg interface{}, data interface{}, count int64) {
	json := &JsonStruct{Code: code, Msg: msg, Data: data, Count: count}
	c.JSON(200, json)
}
func ReturnFalse(c *gin.Context, code int, msg interface{}) {
	json := &JsonErrStruct{Code: code, Msg: msg}
	c.JSON(200, json)
}
```

在角色控制器中使用

```go
//controller/user.go
package controller

import "github.com/gin-gonic/gin"

type UserController struct {
}

//将其归进结构体中，避免与同一个包下的其他方法名字冲突。就是引用的时候稍微麻烦些
func (u UserController) GetUserInfo(c *gin.Context) {
	ReturnSuccess(c, 0, "success", "user info", 1)
}
```

在`main.go`中引用

```go
//main.go
user.GET("/info", controller.UserController{}.GetUserInfo)
user.GET("/err", controller.UserController{}.GetUserList)
```

ok 完成，已经有一个项目的雏形了

## 从上下文获取数据

`*c gin.context`显然不是吃干饭的，每回写方法都把它带上是有原因的

```go
func (U UserController) GetUserList(c *gin.Context) {
	cid := c.PostForm("cid")
	name := c.DefaultPostForm("name", "李大壮")//提供默认值
	ReturnSuccess(c, 0, cid, name, 1)
}
```

这是一个简单的接受数据的方法

这里使用 Apifox（免费的，好使 👍）向它发送请求

<img src="./Gin_note/image-20240329131341634.png" alt="image-20240329131341634" style="zoom: 67%;" />

ok 完成，效果显著

## 将请求获取的数据绑定到结构体

上述方法不适合读取 json 数据报文

第一种,以赋值的形式读过来

```go
func (U UserController) GetUserList(c *gin.Context) {
	//cid := c.PostForm("cid")
	//name := c.DefaultPostForm("name", "李大壮") //提供默认值
	param := make(map[string]interface{})
	err := c.BindJSON(&param)
	if err == nil {
		ReturnSuccess(c, 0, "success",param, 1)
		return
	} else {
		ReturnFalse(c, 4001, gin.H{"err": err})
	}
}
```

第二种，绑定到结构体

```go
type Search struct {
	Name string `json:name`   //必须要json匹配上，否则可能读不到
	Cid  int    `json:cid`
}

func (U UserController) GetUserList(c *gin.Context) {
	search := &Search{}
	err := c.BindJSON(&search)
	if err == nil {
		ReturnSuccess(c, 0, search.Name, search.Cid, 1)
		return
	} else {
		ReturnFalse(c, 4001, gin.H{"err": err})
	}
}
```

## defer 延迟捕获异常

```go
	defer func() {
		if err := recover(); err != nil {
			fmt.Println("捕获异常", err)
		}
	}()
```

自动运行，塞在方法里面就行，但是前端得不到报错情况。

## Gorm

这是一个 SQL 映射库

### 配置

创建文件`config/dbconnect.go`

```go
/*
初始化数据库链接
*/
package config

import (
	"fmt"
	_ "github.com/joho/godotenv/autoload"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"os"
	"time"
)

var (
	Db      *gorm.DB
	err     error
	Mysqldb string
)

func init() {
	//初始化数据库的钥匙
	name := os.Getenv("name")
	password := os.Getenv("password")
	if name == "" || password == "" {
		panic("缺少必要的环境变量 name 或 password")
	}
	Mysqldb = fmt.Sprintf("%s:%s@tcp(127.0.0.1:3306)/minato_sys?charset=utf8mb4&parseTime=true", name, password)
	//链接数据库
	Db, err = gorm.Open(mysql.Open(Mysqldb), &gorm.Config{})
	if err != nil {
		fmt.Println("mysql connect error:", err.Error())
	}
	if Db.Error != nil {
		fmt.Println("mysql connect error:", Db.Error)
	}
	//设置连接池
	sqlDB, _ := Db.DB()
	// SetMaxIdleConns sets the maximum number of connections in the idle connection pool.
	sqlDB.SetMaxIdleConns(10)

	// SetMaxOpenConns sets the maximum number of open connections to the database.
	sqlDB.SetMaxOpenConns(100)

	// SetConnMaxLifetime sets the maximum amount of time a connection may be reused.
	sqlDB.SetConnMaxLifetime(time.Hour)
}
```

后续可以根据自己需要，分别写在自己想要的文件里

注：此处用到了 godotenv 插件，可以从环境变量中读取数据，使用时可以参考这位老哥写的：[Go 每日一库之 godotenv - 大俊的博客 (darjun.github.io)](https://darjun.github.io/2020/02/12/godailylib/godotenv/)

```env
#这是一个示例的env文件
name = root
password = 88888888
```

### 测试数据库是否链接

注：以下代码仅是测试使用，不可直接粘贴【直接粘贴和伪代码没啥区别】，根据需求进行改动

```go
//定义路由
user.GET("/info/:cid", controller.UserController{}.GetUserInfo)
//执行方法
func (u UserController) GetUserInfo(c *gin.Context) {
	defer func() {
		if err := recover(); err != nil {
			fmt.Println("捕获异常", err)
		}
	}()
	cid := c.Param("cid")
	id, err := strconv.Atoi(cid)
	if err != nil {
		fmt.Println(err)
	}
	user, _ := model.GetUserTest(id)
	ReturnSuccess(c, 0, "success", user, 1)
}
//定义数据库模型
type User struct {
	Id   int
	Name string
}

var DB = config.Db

func (User) TableName() string {
	return "user"
}
func GetUserTest(id int) (User, error) {
	var user User
	err := DB.Where("id=?", id).First(&user).Error
	return user, err
}
```

且测试前，数据库需要建立好测试表

<img src="./Gin_note/image-20240330175545744.png" alt="image-20240330175545744" style="zoom: 80%;" />

最终结果：

<img src="./Gin_note/image-20240330175639344.png" alt="image-20240330175639344" style="zoom: 80%;" />

ok 完成，这下项目基本结构就搭建好了

### 基础 crud

这个讲道理没啥好说的，官方文档写的蛮清晰的

贴点样例

```go
func GetUserTest(id int) (User, error) {
	var user User
	err := DB.Where("id=?", id).First(&user).Error
	return user, err
}

func AddUser(id int, name string) (int, error) {
	user := User{Id: id, Name: name}
	err := DB.Create(&user).Error
	return user.Id, err
}

func EditUser(id int, name string) {
	user := User{
		Id:   id,
		Name: name,
	}
	//传对象修改
    DB.Model(&User{}).Updates(&user)
	//修改单独的列
	//DB.Model(&User{}).Where("id=?", id).Update("name", name)

}

func Delete(id int) {
	DB.Delete(&User{}, 10)
}

```

### 登录功能（附带使用 redis 存取 session）

`Redis`部署进项目

```go
package router

import (
	"gin-Minato/config"
	"gin-Minato/controller"
	"github.com/gin-contrib/sessions"
	session_redis "github.com/gin-contrib/sessions/redis"
	"github.com/gin-gonic/gin"
)

func Router() *gin.Engine {
	r := gin.Default()
	//配置redis
	store, _ := session_redis.NewStore(10, "tcp", config.RedisAddress, "", []byte("secret"))
	r.Use(sessions.Sessions("mysession", store))
	user := r.Group("/user")
	{
		user.POST("/login", controller.UserController{}.Login)
		user.POST("/register", controller.UserController{}.Register)
	}
	return r
}
```

`redis.go`

```go
package config

const (
	RedisAddress = "localhost:6379"
)

```

`controller/user.go`

```go
func (u UserController) Login(c *gin.Context) {
	username := c.DefaultPostForm("username", "")
	password := c.DefaultPostForm("password", "")
	if username == "" || password == "" {
		ReturnFalse(c, 4001, "请输入账号和密码")
	}
	user, err := model.GetUserInfoByUsername(username)
	if user.Id == 0 {
		ReturnFalse(c, 4002, "用户名或密码不正确")
		return
	}
	if user.Password != EncryMd5(password) {
		ReturnFalse(c, 4002, "用户名或密码不正确")
		return
	}
	session := sessions.Default(c)
	session.set("login"+strconv.Itoa(user.Id), user.Id)
	session.Save()
	data := UserApi{Id: user.id, Username: user.Username}
	ReturnSuccess(c, 0, "登陆成功", data, 1)
}
```

## JWT-go

可以限制令牌持有者能访问的资源

```go
import (
	"fmt"
	"github.com/dgrijalva/jwt-go"
	_ "github.com/joho/godotenv/autoload"
	"os"
	"time"
)

// 弄个简单一点的token
type Konoha struct {
	Username string `json:"username"`
	jwt.StandardClaims
}

// 从env文件中读取密钥
var salt = os.Getenv("salt")
var mySignkey = []byte(salt)

func Tokencreate(username string) string {
	c := Konoha{
		Username: username,
		StandardClaims: jwt.StandardClaims{
			NotBefore: time.Now().Unix() - 60,
			//设置过期时间在5秒后
			ExpiresAt: time.Now().Unix() + 5,
			Issuer:    "Minato",
		},
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, c)
	tokenString, err := token.SignedString(mySignkey)
	if err != nil {
		fmt.Println("token加密出错", err.Error)
	}
	fmt.Println(tokenString)
	return tokenString
}

func ParseToken(tokenString string) {
	token, err := jwt.ParseWithClaims(tokenString, &Konoha{}, func(token *jwt.Token) (interface{}, error) {
		return mySignkey, nil
	})
	if err != nil {
		fmt.Println(err.Error())
		return
	}
	fmt.Println(token.Claims.(*Konoha))
}

func main() {
    //制作token
	s := Tokencreate("minato")
    //等token过期
	fmt.Println("等六秒")
	time.Sleep(6 * time.Second)
	ParseToken(s)
}
```

结果：

```terminal
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1pbmF0byIsImV4cCI6MTcxMjAzNDY5NywiaXNzIjoiTWluYXRvIiwibmJmIjoxNzEyMDM0NjMyfQ.rUsDMCOgP4-Tvq09UO0YWXVcfaetFtqhWejSszb2DCc
等六秒
token is expired by 1s

```

将它写成中间件的形式：

```go
package middleware

import (
	"fmt"
	"gin-Minato/controller"
	"github.com/dgrijalva/jwt-go"
	"github.com/gin-gonic/gin"
	_ "github.com/joho/godotenv/autoload"
	"os"
	"time"
)

// 弄个简单一点的token
type Konoha struct {
	Username string `json:"username"`
	jwt.StandardClaims
}

// 从env文件中读取密钥
var salt = os.Getenv("salt")
var mySignkey = []byte(salt)

func Tokencreate(username string) string {
	c := Konoha{
		Username: username,
		StandardClaims: jwt.StandardClaims{
			NotBefore: time.Now().Unix() - 60,
			//设置过期时间在60秒后
			ExpiresAt: time.Now().Unix() + 60,
			Issuer:    "Minato",
		},
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, c)
	konohaToken, err := token.SignedString(mySignkey)
	if err != nil {
		fmt.Println("token加密出错", err.Error())
	}
	fmt.Println(konohaToken)
	return konohaToken
}
//-----------------------------------------在这呢，中间件解析token------------------------------------
func ParseToken(konohaToken string) string {
	token, err := jwt.ParseWithClaims(konohaToken, &Konoha{}, func(token *jwt.Token) (interface{}, error) {
		return mySignkey, nil
	})
	if err != nil {
		fmt.Println(err.Error())
		return "1001"
	}
	if !token.Valid {
		fmt.Println("token无效")
		return "1002" // 返回无效token的错误码
	}
	claims, ok := token.Claims.(*Konoha)
	if !ok {
		fmt.Println("token claims类型错误")
		return "1003" // 返回token claims类型错误的错误码
	}
	if claims.Username != "Minato" {
		return "1004"
	}
	return "200"
}
func JWTAuth() gin.HandlerFunc {
	return func(c *gin.Context) {
		tokenStr := c.Request.Header.Get("konohaToken")
		if tokenStr == "" {
			controller.ReturnFalse(c, 1000, "token缺失")
		}
		status := ParseToken(tokenStr)
		switch status {
		case "1000":
			controller.ReturnFalse(c, 1001, "token过期")
		case "1001":
			controller.ReturnFalse(c, 1002, "token签发人不正确")
		case "1002":
			controller.ReturnFalse(c, 1003, "token claims类型错误")
		case "1003":
			controller.ReturnFalse(c, 1004, "token无效")
		case "200":
			// token验证通过
			fmt.Println(200)
			return
		default:
			// 处理其他未知错误
			controller.ReturnFalse(c, 1999, "未知错误")
		}
	}
}

```

## 跨域请求 CORS

安装 CORS

```terminal
$ go get github.com/gin-contrib/cors
```

`main.go`中进行配置

```go
package main

import (
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()

	// 使用 CORS 中间件，默认配置，谁都能访问
	r.Use(cors.Default())

    // 使用CORS中间件，并只允许来自5173端口的请求（和上面不能同时出现）
    router.Use(cors.New(cors.Config{
        AllowOrigins:     []string{"http://localhost:5173"},
        AllowMethods:     []string{"GET", "POST", "PUT", "DELETE"},
        AllowHeaders:     []string{"Origin", "Content-Type"},
        ExposeHeaders:    []string{"Content-Length"},
        AllowCredentials: true,
        MaxAge:           12,
    }))
	// 其他路由处理逻辑
	// ...

	r.Run(":8080")
}
```
