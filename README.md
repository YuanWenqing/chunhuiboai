# 环境准备

安装`python2`

***只需要安装一次！***

## Mac

自带python2，无需安装

## Windows

参考：https://www.jianshu.com/p/edf7679d4aab

# 执行统计脚本

***每次需要统计时进行这一步***

## 命令行

执行

~~~python
python /path/to/stat-chba.py /path/to/month-data-directory
~~~

比如

~~~python
python /path/to/stat-chba.py /path/to/6月
~~~

## 从每月数据的目录下启动（Windows）

将 `stat-chba.py` 拷贝到相应目录中，然后双击执行

# 输入和输出

这里对输入和输出进行一下说明

## 输入

* 每月数据在一个目录
* 每日的明细数据作为一个目录放在每月数据目录中
* 每日的明细数据目录中包含一个明细文件，文件格式为 .csv

## 输出

* 输出到每月数据目录下的子目录 `summary`
* `summary` 包含三个文件
* `months.csv`：按月统计
* `dates.csv`：按日统计
* `persons.csv`：按人统计

