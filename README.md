
部署基于`Python3`,`nginx`,`gunicorn`

比如项目部署在`/www`目录

第一步：克隆代码

    git clone https://github.com/zhujp/flask_blog.git app_name
    
第二步：创建数据库
    
    create database app_name charset=utf8;
    
进入项目的目录`cd /www/app_name`

第三步：基础环境搭建

安装扩展
    
    pip3 install -r requirements.txt
    
配置文件新增修改
    
    cp DefaultConfig.py config.py
    
编辑配置文件`ProductionConfig`数据库连接部分uri
    
第四步：修改启动文件
    
    vi manage.py
    
修改
    app = create_app(os.getenv('FLASK_CONFIG') or 'production')  # default改为production
    
第五步：执行数据库迁移
    
    python3 manage.py db init
    python3 manage.py db migrate
    python3 manage.py db upgrade
    
第六步：项目部署

nginx配置：
    
    server {
            listen       80;
            server_name  domain_name; #你的域名
            include /etc/nginx/default.d/*.conf;
            location / {
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
            proxy_redirect off;
          proxy_pass http://127.0.0.1:123456;  #注意端口，后面有使用到，自己定义一个可用的端口
            }
            location /static/ {
                alias /www/app_name/app/static/;  # 项目静态资源文件地址
            }
    }
    
    
gunicorn的安装
    
    pip3 install gunicorn
    
启动
    
    gunicorn -b 127.0.0.1:123456 manage:app
    
`端口号要与nginx中的一致，manage是启动文件的名称，app是里面应用的名称`
 
    
第七步：后台新增管理员，否则无法登录
    
    python3 manage.py shell

然后依次输入代码
    
    u = User(username='abc',email='333@33.com',password='abc',enabled=1)
    db.session.add(u)
    db.session.commit()
    exit()
    
前台地址：`http://domain_name`

后台地址：`http://domain_name/backend/login`

博客地址：`https://www.bdelay.com`
    
