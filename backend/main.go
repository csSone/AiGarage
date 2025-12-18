package main

import (
	"log"
	"os"

	"github.com/gin-gonic/gin"
)

func main() {
	// 创建日志文件
	logFile, err := os.Create("app.log")
	if err != nil {
		log.Fatal("无法创建日志文件:", err)
	}

	// 设置Gin模式为发布模式，减少默认日志输出
	gin.SetMode(gin.ReleaseMode)

	// 创建自定义日志记录器
	logger := log.New(logFile, "[Gin] ", log.LstdFlags)

	// 创建路由器并添加自定义日志中间件
	router := gin.New()

	// 添加日志中间件
	router.Use(gin.LoggerWithFormatter(func(param gin.LogFormatterParams) string {
		logger.Printf("%s - [%s] \"%s %s %s %d %s \"%s\" %s\"\n",
			param.ClientIP,
			param.TimeStamp.Format("02/Jan/2006:15:04:05 -0700"),
			param.Method,
			param.Path,
			param.Request.Proto,
			param.StatusCode,
			param.Latency,
			param.Request.UserAgent(),
			param.ErrorMessage,
		)
		return ""
	}))

	// 添加恢复中间件
	router.Use(gin.Recovery())

	router.GET("/ping", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"message": "pong",
		})
	})

	router.Run() // listens on 0.0.0.0:8080 by default
}
