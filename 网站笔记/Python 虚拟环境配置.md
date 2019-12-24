环境：Windows 版 Python

Python 3.6.8可以用自带的命令建立虚拟环境，不用安装另外的如 **virtualenv**、**virtualenvwrapper等工具。**

```
python -m venv MyApp
```

当这样建立了虚拟环境后，在其中安装的包很多，也很费时间，你想将这个MyApp放到其他电脑上去开发，是不是直接复制MyApp文件夹就可以了呢? 不行！因为在建立虚拟环境时，虚拟环境中的python.exe, pip.exe......等一些文件会“硬编码”，记录的是绝对路径，放到其他电脑后，因为路径不同会出错！

所以采用的方法是导出安装的包，在另一台电脑新建虚拟环境，再将包导入到新建的虚拟环境。

1、输出虚拟环境中已安装包的名称及版本号并记录到 requirements.txt 文件中：

```
 (MyApp)xxx> pip freeze > requirements.txt
```

2、将安装的包保存到文件夹(名字任意起，如packages)里：

```
(MyApp) xxx>  pip download -r requirements.txt -d packages   
```

3、在另一台电脑新建虚拟环境 ：

```
python -m venv MyApp
```

将 **requirements.txt** 和 **packages** 复制到虚拟环境里，激活虚拟环境后安装包：

```
(MyApp) yyy> pip install --no-index --find-links=packages -r requirements.txt  
```

