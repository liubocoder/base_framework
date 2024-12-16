1. django基础配置  ok
2. sqlite配置     ok
3. redis连接      ok
4. module创建: app.api.demo        ok
5. 自定义django指令 demo.showm      ok
6. 日志配置        ok
7. celery配置     ok
8. 各种drf 接口示例   ok
9. 工具类          ok

10. 多app的数据库路由   ok

11. model关联关系、事务等  ok

12. 单元测试            ok

13. 自定义用户          ok
14. 自定义权限          ok
15. 自定义session管理？
16. websocket示例      ok
17. 自定义channel tcp服务器   ok
18. 使用event队列的tcp服务器 asyncio.start_server

19. 分表方案？ 参考以下方案，实现日期分库
https://github.com/iTraceur/django_table_sharding_example.git

20. template模板？

21. celery-beat调度器？
https://blog.csdn.net/qq_36441027/article/details/123851915

22. swagger拦截
- drf_spectacular
    redoc.html
    swagger_ui.html
    swagger_ui.js  # 修改这里的js代码完成拦截，可以用于登录token的注入等
- 替换drf_spectacular.views中的资源目录 
- 路由添加swagger的页面地址

23. 部署
- migration 管理、钩子事件  ok
- supervisord celery  ok
- supervisord daphne  ok
- supervisord nginx   ok
- supervisord redis ok
- supervisord mysql   ok

24. fastcgi 进程的管理 fcgi-program
https://www.cnblogs.com/-lee/p/12650298.html

25. pyInstaller 打包可执行文件 ?


