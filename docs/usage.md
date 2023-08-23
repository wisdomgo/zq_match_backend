# 使用说明

## 1. 创建项目

### 1.1. 安装 cookiecutter

```shell
pip install cookiecutter
```

### 1.2. 创建项目

```shell
cookiecutter gh:Nagico/zq-django-template
```

### 1.3. 输入项目信息

- project_name_short: 项目名称，尽量使用一个英文单词描述，比如招新小程序: `recruitment`
- project_name: 后端项目完整名称，根据项目名称自动生成，比如招新小程序: `zq_recruitment_backend`
- project_slug: 无需修改，根据项目名称自动生成
- description: 项目描述，例如 `自强招新小程序后端`
- author_name: 作者名称，例如自己Github的昵称
- author_email: 作者邮箱
- use_celery: 是否使用 Celery 异步任务
- use_wechat: 是否使用微信小程序登录
- use_sentry: 是否使用 Sentry 监控
- use_meilisearch: 是否使用 Meilisearch 搜索后端

最后提示 `[SUCCESS]: Project initialized, keep up the good work!` 即创建成功。

## 2. 项目初始化

### 2.1. 创建虚拟环境

使用 Pycharm 创建 conda 虚拟环境，或者使用以下命令创建虚拟环境：

```shell
conda create -n 项目名称 python=版本号(3.9|3.10|3.11)
```

**注意：** 请使用 Python 3.9+ 版本

### 2.2. 安装依赖

- 安装 Poetry

```shell
pip install poetry
```

Poetry 是 Python 的包管理工具，用于管理项目依赖。详细使用方法请参考 [poetry 官方文档](https://python-poetry.org/docs/)。

项目根目录下 `pyproject.toml` 文件包含了项目依赖，其作用和 `requirements.txt` 类似。

而一旦进行依赖安装后，会生成 `poetry.lock` 文件。其则包含了项目依赖的具体版本，用于保证项目依赖的一致性。建议将其一同提交到 Git 仓库。

- 安装项目依赖

```shell
poetry install --with dev
```

`--with dev` 表示将安装开发依赖一同安装，便于开发使用


### 2.3. 初始化 Git 仓库

```shell
git init
pre-commit install
pre-commit install --hook-type commit-msg
```

其中 `pre-commit install` 用于安装 git 提交规范与代码检查。

### 2.4. 初始化环境配置

使用 PyCharm 打开项目，在 `config` 文件夹下有一个 `.env` 文件，用于存储项目的环境配置。
`config` 下的 `env.example` 文件是一个配置示例，会被提交到 Git 仓库，用于新成员参考。当 `.env` 内修改了配置后，请将配置的说明添加到 `env.example` 中。

默认配置文件包括

- DJANGO_ENV: 项目环境，可选值为 `development`、`production`。不同的项目环境会使用不同的 settings 文件
- DJANGO_SECRET_KEY: 项目密钥，会自动随机生成
- CACHE_URL: 缓存地址，可以根据格式填写。当注释到这一行时，会使用默认的本地缓存
- DATABASE_URL: 数据库地址，可以根据格式填写。当注释到这一行时，会使用默认的本地 SQLite 数据库

#### Celery
- CELERY_BROKER_URL: Celery 任务队列地址，推荐与 `CACHE_URL` 使用同一 redis 后端。但最后要以 `/0` 或者其他数字结尾，表示使用 redis 的第几个数据库
- CELERY_FLOWER_USER: Celery Flower 用户名
- CELERY_FLOWER_PASSWORD: Celery Flower 密码

#### 微信
- WECHAT_APP_ID: 小程序 AppID
- WECHAT_APP_SECRET: 小程序 AppSecret

#### Sentry
- SENTRY_ENABLE: 是否启用 Sentry
- SENTRY_DSN: Sentry DSN

#### OSS
- ALIYUN_OSS_ACCESS_KEY_ID: OSS Access Key ID
- ALIYUN_OSS_ACCESS_KEY_SECRET: OSS Access Key Secret
- ALIYUN_OSS_BUCKET_NAME: OSS Bucket

其中 Endpoint 默认为杭州，如需修改可在配置文件中更改

#### MeiliSearch
- MEILI_URL: 搜索服务地址
- MEILI_MASTER_KEY: 搜索服务密码(若无密码则可删除该项)

#### Ziqiang Auth
接入自强 Auth 需要手动向管理员申请，并提供必要信息注册 APP，获取 APPID 和 SECRET

- ZQAUTH_APPID: APPID
- ZQAUTH_SECRET: SECRET


## 3. 项目运行

在 PyCharm 中内置了一些运行配置，可直接使用。

![run config](img/usage/run_config.png)

- Local Server: 生产/本地/测试 服务器，使用 development 配置
- Prod Server: 生产服务器，使用 production 配置
- Beat: Celery Beat，用于定时任务
- Worker: Celery Worker，用于执行异步任务
- Flower: Celery Flower，用于监控 Celery
- Makemigrations: 生成迁移文件，使用 development 配置
- Migrate: 执行迁移，使用 development 配置
- Shell: 进入 Django Shell，使用 development 配置
- Test All with pytest: 运行所有测试，使用 development 配置

选择 `Local Server` 运行后，会在 `http://localhost:8000` 启动一个 Django 服务器。打开网站后会看到测试 ViewSet。

### 3.1. Services 方式运行

当使用 Celery 时会运行多个程序，不便于管理。在 PyCharm 中双击 Shift，搜索 `Services`，打开 Services 窗口。

并依次添加 `Django Server`、`Python` 这两类 Configuration Type。

![services](img/usage/services.png)

可以在指定项目或者文件夹上右键进行启动

## 4. 项目结构与说明

项目主要结构如下：

```
zq_xxx_backend/  项目根目录
  | .github/  Github 设置
  |  | workflows/  Github Actions 配置
  |
  | config/  项目配置（不会上传至 Git 仓库）
  | | .env  环境配置（不会上传至 Git 仓库）
  | | .env.example 环境配置示例，请勿在此文件中填写真实配置
  |
  | docker/  docker 配置
  | logs/  日志（不会上传至 Git 仓库）
  | server/  项目代码
  |  | apps/  应用，创建新应用时需要进入到 apps 目录下执行 `python ..\..\manage.py startapp <app_name>`
  |  |  | async_tasks/  异步任务（示例）
  |  |  |  | management/  用于添加 runcelery 命令，可以快速启动 celery 用于调试
  |  |  |
  |  |  | files/  OSS 文件（示例）服务器上传 + OSS 直传
  |  |  | oauth/  登录与 jwt 认证（示例）包括微信登录、openid 登录（测试）、账号密码登录、zq_auth统一认证
  |  |  | users/  用户（示例）可仿照 models.py 进行自定义字段
  |  |
  |  | settings/  项目配置
  |  |  | components/  各个子配置文件
  |  |  | environments/  各个环境配置文件
  |  |  | __init__.py  进行配置文件的组合以及根据 DJANGO_ENV 自动选择环境
  |  |
  |  | templates/  模板文件，几乎没有用
  |  | utils/  工具函数
  |  |  | choices/  公共的枚举类
  |  |  |  | status.py  状态
  |  |  |  | types.py  类型
  |  |  |
  |  |  | logging_handler.py  loguru 日志处理器
  |  |  | permissions.py  权限控制
  |  |  | serializers.py  可公用的序列化器
  |  |
  |  | celery.py  celery 配置
  |  | urls.py  路由配置
  |
  | business/  第三方服务
  |  | wechat/  微信服务
  |  | ziqiang/ 自强服务
  |
  | tests/  测试
  |  | apps/  应用测试
  |  | business/  第三方服务测试
  |  | .coveragerc  测试覆盖率配置
  |  | conftest.py  pytest 配置与公用 fixture
  |
  | .dockerignore  docker 忽略文件
  | .editorconfig  编辑器配置
  | .gitattributes  git 配置
  | .gitignore  git 忽略文件
  | .pre-commit-config.yaml  pre-commit 配置
  | manage.py  Django 管理脚本
  | poetry.lock  项目依赖锁定文件
  | pyproject.toml  项目配置+依赖
  | README.md  项目说明
  | runtests.py  手动测试脚本
```

### 4.1. .github/workflows/

GitHub Actions 配置文件，用于自动化构建与部署，包括：

- prod.yml 生产环境自动构建（production 分支自动触发）
- prod-deploy.yml 生产环境自动部署（手动触发）
- test.yml 测试服务器自动构建与部署（master、main 分支自动触发）

### 4.2. docker/

docker 配置文件

#### 4.2.1. caddy/

Caddy 配置，用于静态资源文件部署与后端反向代理

- static/  静态资源文件

`python manage.py collectstatic` 会将静态文件收集到此处

- Caddyfile  Caddy 配置文件

其中配置了 static 文件服务、Django 反向代理、Flower反向代理

- ci.sh  Caddy 自动测试
- compress.sh  static 静态文件压缩
- Dockerfile  镜像构建文件

#### 4.2.2. django/

Django 配置

- celery/  Celery 相关启动脚本
- Dockerfile  镜像构建文件
- gunicorn_config.py  Gunicorn 配置文件
- start.sh  生产环境启动脚本
- start-debug.sh  开发环境启动脚本


#### 4.2.3. docker-compose-prod.yml

docker-compose 配置文件（生产环境），使用 `zq_xxx_backend:image` 镜像

其中的容器有：

- caddy: 静态资源文件部署与后端反向代理
- django: Django 后端
- redis: Redis 缓存
- celeryworker: Celery Worker
- celerybeat: Celery Beat
- flower: Celery Flower

使用了两个网络：

- app-net

用于后端服务内部通信，使用容器名字可表示该容器的内部 ip，比如 `redis://redis` 可连接到 redis 容器的 Redis 服务；`http://django` 可访问 django 容器的 80 端口。

- traefik

用于后端服务与外部通信，使用 [Traefik](https://doc.traefik.io/traefik/) 服务发现自动化配置域名反向代理与 https

**在 caddy 容器下有 labels 配置**，用于配置 Traefik 服务发现。

需要修改 `traefik.http.routers.template.rule` 的内容，将 `Host` 内的域名改为服务部署的域名。

比如：

```yaml
traefik.http.routers.template.rule: Host(`api.recruitment.ziqiang.net.cn`)  # 生产环境
traefik.http.routers.template.rule: Host(`test.api.recruitment.ziqiang.net.cn`)  # 测试环境
```


#### 4.2.4. docker-compose-test.yml

docker-compose 配置文件（开发环境），使用 `zq_xxx_backend:image-test` 镜像

其他说明见 `docker-compose-prod.yml`

### 4.3. server/settings/utils.py

一些和 django 配置相关的工具

- BASE_DIR: 项目代码的根目录，即 `server` 文件夹
- config: 用于获取 `config/.env` 或者环境变量，其中环境变量优先级最高
- _ENV: 当前环境，`production` 或者 `development`

### 4.4. server/settings/components

由于配置文件过于繁多，把其拆分为若干个子配置文件

#### 4.4.1. \_\_init\_\_.py

通过 `from .xxx import *` 导入 xxx 子配置文件

#### 4.4.2. caches.py

缓存配置，调用 `CacheConfig` 生成缓存配置，基本上不需要修改

#### 4.4.3. celery.py

Celery 配置，添加了时区、django 支持等参数

`CELERY_BROKER_URL` 自动获取自环境变量

#### 4.4.4. common.py

基础配置

- SECRET_KEY: 项目密钥，自动从环境变量获取
- CORS_ORIGIN_WHITELIST: CORS 白名单，用于配置**跨域访问**
- SIMPLE_JWT: JWT 配置，一般不用修改
- AUTH_USER_MODEL: **用户模型**，一般不用修改，可以直接修改 users 应用下的 `models.py` 文件
- USER_ID_FIELD: 用户模型的主键字段，一般不用修改

#### 4.4.5. apps.py

应用配置

- DJANGO_APPS: Django 自带的应用，一般不用添加
- THIRD_PARTY_APPS: 第三方应用，安装第三方应用时需要添加到这里
- LOCAL_APPS: 本地应用，添加本地应用时需要添加到这里
- MIDDLEWARE: 中间件

#### 4.4.6. configs.py

**数据库**、**缓存**、日志等配置类，用于生成 django 配置

- DatabaseConfig: 根据 `DATABASES` 下的字段与给定的 `DATABASE_URL` 生成数据库配置
- CacheConfig: 根据 `CACHES` 下的字段与给定的 `CACHE_URL` 生成缓存配置
- LogConfig: 使用 loguru 代替默认的日志框架，一般无需修改

#### 4.4.7. databases.py

数据库配置，调用 `DatabaseConfig` 生成数据库配置，基本上不需要修改

#### 4.4.8. django_utils.py

zq-django-util 配置

- EXCEPTION_UNKNOWN_HANDLE: 是否处理未知异常，默认与 DEBUG 的值相反（不处理未知异常时会由 django 进行默认的处理，并返回详细的 debug 页面）
- EXCEPTION_HANDLER_CLASS: 异常处理类，若需要自定义异常处理流程可以修改此处

详细内容可参考 [zq-django-util](https://zq-django-util.readthedocs.io/en/latest/usage/exception_response_log/)

#### 4.4.9. drf.py

drf 配置

- DEFAULT_PERMISSION_CLASSES: 默认权限类，可根据实际需要修改

#### 4.4.10. logging.py

日志配置，调用 `LogConfig` 生成日志配置，基本上不需要修改

`DRF_LOGGER` 请参考 [zq-django-util](https://zq-django-util.readthedocs.io/en/latest/usage/exception_response_log/)

#### 4.4.11. sentry.py

sentry 配置，可根据 [sentry](https://docs.sentry.io/platforms/python/django/) 文档进行配置

其中 `debug`、`dsn`、`environment`、`traces_sample_rate` 会自动配置

#### 4.4.12. server_url.py

服务器地址配置，目前仅用于微信小程序二维码生成时判断 `release` 或 `trial` 环境

- SERVER_URL: 当前服务器地址，自动从环境变量获取
- PRODUCTION_SERVER_LIST: 生产环境服务器地址列表，用于判断当前环境是否为生产环境
- DEVELOPMENT_SERVER_LIST: 开发环境服务器地址列表，用于判断当前环境是否为开发环境

#### 4.4.13. simpleui.py

admin 界面配置，可根据 [simpleui](https://simpleui.72wo.com/docs/simpleui/QUICK.html#%E8%8F%9C%E5%8D%95) 进行自定义菜单配置

#### 4.4.14. storage.py

OSS 文件存储配置

`ACCESS_KEY_ID`、`ACCESS_KEY_SECRET`、`BUCKET_NAME` 会自动从环境变量获取

其余配置需要根据实际情况进行修改，详细内容可参考 [zq-django-util OSS](https://zq-django-util.readthedocs.io/en/latest/usage/oss_storage/)

#### 4.4.15. wechat.py

微信配置，`WECHAT_APPID` 与 `WECHAT_APPID` 会自动从环境变量获取，并在 `utils/wechat.py` 中使用

### 4.5. server/settings/environments

环境配置，根据环境变量 `DJANGO_ENV` 的值加载对应的配置

- development.py: 开发环境配置
- production.py: 生产环境配置
- local.py: 本地环境配置，不会被 git 追踪，可根据实际情况进行配置

其中优先级为：`local.py` > `development.py`/`production.py` > `components/*.py`，
即：`local.py` 中的配置会覆盖 `development.py`/`production.py` 中的配置，`development.py`/`production.py` 中的配置会覆盖 `components/*.py` 中的配置

`local.py` 不会上传到 Git 仓库

**注意：**

1. 覆盖配置会将原配置中的所有内容覆盖：

```SERVER = "foo"```型的配置项，可直接重新修改为```SERVER="bar"```。

```SERVER = {URL: "foo", PROTOCAL: "http"}```型的字典配置项，如果直接覆盖为 ```SERVER = { "URL": "bar"}```，则 `SERVER["PROTOCAL"]` 会被清空，如需只修改 `SERVER["URL"]` 的值，可直接导入 `SERVER` 后重新赋值 ```SERVER["URL"] = "bar"```。

2. 覆盖时只会修改当前修改的那个变量，其他相关的变量不会自动重新赋值

比如：

在 `components/url.py` 中有以下配置
```python
URL = "http://localhost:8080"

SERVER = {
    "URL": URL,
    "PROTOCAL": "http"
}
```

在 `development.py` 中覆盖：
```python
URL = "https://test.nagico.cn"
```

此时仅 `settings.URL` 会被修改，而 `settings.SERVER["URL"]` 仍为原来的值

如需更新必须再对 `SERVER["URL"]` 进行赋值覆盖：
```python
from server.settings.components.url import SERVER

SERVER["URL"] = URL
```

3. 为方便使用，在 `components/configs.py` 中有 `DatabaseConfig`、`CacheConfig` 配置类

这些配置类中可以自定义额外的配置，比如：
- DatabaseConfig: 定义数据库的名字（默认的就是 `default`）、额外配置 `OPTIONS`
- CacheConfig: 定义缓存的名字和对应的数据库

通过指定对应的 `URL` ，并使用类的 `get()` 方法，可以获得对应的配置字典，并将其赋给 `DATABASES` 或 `CACHES`，即可完成数据库或缓存的配置

- 当需要修改数据库或缓存配置时，只需修改 `components/configs.py` 中的配置类即可

- 当需要修改连接数据库或缓存的 URL 时，可以在 `environment/*.py` 中进行覆盖：
```python
from server.settings.components.configs import DatabaseConfig

DATABASES = DatabaseConfig.get("mysql://user:password@localhost/test")

# 或者
DatabaseConfig.URL = "mysql://user:password@localhost/test"
DATABASES = DatabaseConfig.get()
```

也可以在 `config/.env` 中修改对应的环境变量

## 5. 项目开发

### 5.1. 创建新应用

开发过程中请进入 `server/apps` 文件夹下创建新应用：
```shell
cd server/apps
python ../../manage.py startapp <app_name>
```

并修改 `server/settings/components/common.py` 添加新应用

应用的目录结构可以包括：
```
<app_name>\  apps下的文件夹
├── migrations\  数据库迁移（需要上传至 Git 仓库）
├── admin.py  管理后台
├── apps.py  应用配置（一般不做修改）
├── models.py  数据库模型
├── serializers.py  序列化器
├── tasks.py  Celery 任务（自动被 celery 识别）
├── urls.py  路由
└── views.py  视图
```

**注意：**
1. Python 不同于 Java。Java 中一个文件就是一个类，而 Python 中一个文件可以包含多个类。所以在 Python 中可以把多个序列化器类放入 `serializers.py` 一个文件中，但数量过多时也可以将 `serializers.py` 替换为 `serializers` 文件夹，并在下面放入多个文件，每个文件表示一类相关联的序列化器类。

2. 单元测试建议统一放在 `server/tests/apps/<app_name>` 文件夹下。

3. 需要在设置中注册新应用，在根 `urls.py` 中注册子路由

### 5.2. 添加新依赖

本项目使用 `poetry` 管理依赖，如果需要添加新依赖，请在项目根目录下执行：
```shell
poetry add <package_name>
```

添加开发依赖：
```shell
poetry add --group dev <package_name>
```

删除依赖：
```shell
poetry remove <package_name>
```

### 5.3. 提交代码

git commit 时，会自动检查代码格式与 commit 规范

- 代码格式检查：使用 `black`、`isort` 格式化代码，使用 `flake8` 检查代码格式
- commit 规范检查：使用 `commitlint` 检查 commit 规范

当 Commit 时，可以在 `Git` - `Console` 处查看检查结果

![pre commit](img/usage/precommit.png)

**注意**

1. 第一次 Commit 时会比较慢，因为在下载相关格式检查程序，可以在 `Git` - `Console` 处查看进度

2. 有些时候 Commit 会失败，是因为进行了自动格式化，可再次 Commit 重新提交。若还存在失败，请打开 `Git` - `Console` 查看具体错误信息

## 6. 项目部署

### 6.1. 部署前准备

1. 部署前请确认项目在本地使用 `Prod Server` 可正常运行

2. 运行 `python manage.py collectstatic` 收集静态文件

3. 准备好用于部署的 `.env` 文件

4. 确保 `docker/docker-compose-*.yml` 中 `caddy` 容器的 `traefik.http.routers.template.entrypoints` 已经修改为正确的 URL，并且 `ping <URL>` 指向正确的 IP

### 6.2. Github Actions 配置

在项目 Secrets 中添加 Actions Secrets：

- DOCKER_USERNAME: 阿里云容器镜像服务用户名
- DOCKER_PASSWORD: 阿里云容器镜像服务密码
- TEST_SSH_HOST、TEST_SSH_USERNAME、TEST_SSH_PASSWORD: 测试、开发服务器 SSH 信息
- SSH_HOST、SSH_USERNAME、SSH_PASSWORD: 生产服务器 SSH 信息

### 6.3. 服务器配置

1. 使用指定的 SSH 信息登入服务器，创建项目名称文件夹（需要与 `test.yml` 或 `prod.yml` 中 `cd ~/xxx` 的文件夹一致）
```shell
cd ~
mkdir <project_name>
```

2. 在文件夹内创建 `docker-compose.yml` 文件
```shell
cd <project_name>
touch docker-compose.yml
```

3. 将 `docker/docker-compose-*.yml` 中的内容复制到 `docker-compose.yml` 中

可选择 `vim` 或者 `nano` 进行编辑

4. 创建并编辑 `.env` 文件，将准备好的 `.env` 文件内容复制到 `.env` 中
```shell
vim .env
```

其中
- `CACHE_URL` 可设置为 `redis://redis/`
- `CELERY_BROKER_URL` 可设置为 `redis://redis/0`

### 6.4. 部署

1. 将 `.github/workflows/test.yml` 或 `.github/workflows/prod.yml` 中的 `on: push: branches` 下的字段取消注释，开启自动部署
2. 将项目推送至 Github 仓库，等待 Github Actions 自动部署

等待部署成功后，可在服务器上查看部署情况

```shell
docker-compose ps
```
