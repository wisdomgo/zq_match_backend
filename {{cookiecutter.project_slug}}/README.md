<div align="center">

# {{cookiecutter.description}}

<!-- markdownlint-disable-next-line MD036 -->
_✨ Author: {{cookiecutter.author_name}} ✨_
</div>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9|3.10|3.11-blue" alt="python">
  <img src="https://img.shields.io/badge/Django-4.0-blue" alt="django">
  <img src="https://img.shields.io/badge/Docker%20Build-automated-blue" alt="docker">、
  <br />
  <a href="https://github.com/ZiqiangStudio/{{ cookiecutter.project_slug }}/actions/workflows/prod.yml">
    <img src="https://github.com/ZiqiangStudio/{{ cookiecutter.project_slug }}/actions/workflows/prod.yml/badge.svg?branch=production" alt="Production Server CI/CD">
  </a>
  <a href="https://github.com/ZiqiangStudio/{{ cookiecutter.project_slug }}/actions/workflows/test.yml">
    <img src="https://github.com/ZiqiangStudio/{{ cookiecutter.project_slug }}/actions/workflows/test.yml/badge.svg?branch=master" alt="Test Server CI/CD">
  </a>
</p>
<!-- markdownlint-enable MD033 -->

## 项目地址

- 生产环境: [api.{{ cookiecutter.project_name }}.ziqiang.net.cn](https://api.{{ cookiecutter.project_name }}.ziqiang.net.cn)
- 测试环境: [api.test.{{ cookiecutter.project_name }}.ziqiang.net.cn](https://api.test.{{ cookiecutter.project_name }}.ziqiang.net.cn)

## 开发

1. 克隆项目

```bash
git clone https://github.com/ZiqiangStudio/{{ cookiecutter.project_slug }}.git
```

2. 创建 conda 环境（推荐）

```bash
conda create -n {{ cookiecutter.project_name }} python=3.11
conda activate {{ cookiecutter.project_name }}
```

3. 安装依赖

```bash
pip install poetry
poetry install --with dev
```

4. 更新配置文件

将实际配置写入 `config/.env` 文件中

5. 使用 Pycharm 打开项目

在右下角选择 <No Interpreter>, Add New Interpreter, Add Local Interpreter, Conda Environment。在 Use existing environment 中选择 {{ cookiecutter.project_name }} 环境

6. 运行项目

选择 Local Server 作为运行项目，并启动

7. 运行测试

选择 Test All with pytest 作为运行项目，并启动
