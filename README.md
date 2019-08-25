# Tu

[![Build Status](https://travis-ci.org/gggxbbb/tujian_python.svg?branch=master)](https://travis-ci.org/gggxbbb/tujian_python)  
  
一个使用 Python3 编写的 Tujian 的简易工具。  
A simple tool for Tujian written by Python3.  
  
图片保存于当前目录下的 `Tujian` 文件夹。  
The all pictures are saved in a folder called `Tujian` where you use the tool.  
  
如果你无法理解，你可以使用 `python3 -m tu path` 来打印存储图片的路径。  
If you cannot understand,you can use `python3 -m tu path` to print the path to save the all pictures.  
  
请使用 `Python3` 运行此工具。  
Please run the tool with `Python3` .  
  
此工具仅支持简体中文。  
The tool only supports **Simplified Chinese**.

# 如何使用 Usage 

```bash
pip3 instal tu
python3 -m tu
```

# 投稿 Submission

使用以下命令来进行投稿:  
```bash
python3 -m tu upload xxx.yml
```
需要提供参数: 一个 `YAML` 文件  

## YAML 文件

`YAML` 是什么请自行百度  

此处提供一个完整的示例文件:  

```yaml
name: Gadgetry
mail: 2331490629@qq.com
pics:
  - title: 示例图片1
    sort: e5771003-b4ed-11e8-a8ea-0202761b0892
    content: |-
      示例图片1
    path: F:\Pictures\001.png
  - title: 示例图片2
    sort: e5771003-b4ed-11e8-a8ea-0202761b0892
    content: |-
      示例图片2
    link: http://example.com/001.png
```

### Profile 用户数据

作为投稿者,你需要提供你的部分信息:  

```yaml
name: 你的昵称
mail: 你的邮箱地址
```

### Pictures 图片

作为投稿者,你需要提供需投稿的图片.  

所有的图片作为一个 `list`:

```yaml
pics:
  - title: 示例图片1
    sort: e5771003-b4ed-11e8-a8ea-0202761b0892
    content: |-
      示例图片1
    path: F:\Pictures\001.png
  - title: 示例图片2
    sort: e5771003-b4ed-11e8-a8ea-0202761b0892
    content: |-
      示例图片2
    path: http://example.com/001.png
```

对于单张图片:  

```yaml
  - title: 图片名称
    sort: 图片分类 PID
    content: |-
      图片简介
      图片简介
      图片简介
    path: 图片本地地址
    link: 图片网络地址
```

`path` 和 `link` 仅需提供其中一个,  

如果使用单行的 `content` ,仅需这样:

```yaml
    ...
    content: 图片简介
    ...
```

如果使用多行的 `content` ,请这样:

```yaml
    ...
    content: |-
      图片简介
      图片简介
      图片简介
    ...
```