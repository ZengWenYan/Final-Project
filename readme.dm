# python期末项目
***
### 项目名称：青春期女性生育率与经济环境和识字率的关系
### 项目成员：17级何畅、18级曾雯燕
### 项目要求：实现交互功能和部署pythonanywhere
***
### [github链接](https://github.com/ZengWenYan/Final-Project)
### [pythonanywhere链接](http://zwy.pythonanywhere.com)
***
## 项目介绍
* 本项目具有2个URL
* 基于全球范围内人均GDP年增长率，探究青春期女性生育率与经济环境和识字率（15-24岁）是否有明显关联。
***

## 三个文档描述
###Web App动作描述：
1. "/": 响应GET请求，返回 GDP per person.csv 文件内容数据并在界面展示
2. "/hurun": 响应POST请求，读取 pregrant.csv、literacy.csv、GDP per person.csv、literacy.csv 文件内容并生成 柱状图、折线图、Map图数据返回页面
							
###Python 函数介绍:
1. getCsvData: 通过传入不同文件名称，并返回pandas数据对象
2. readCsvData: 通过传入不同文件名称，返回pandas数据对象
3. bar_gdp：接入传输数据 并将数据生成柱状图 展示人均GDP年增长率
4. grid_mutil_yaxis：将数据通过 bar line方法 生成折线图与柱状图并展示生育率与GDP增长率对比图
5. map_data：根据参数生成 识字率&生育率 Map图信息
6. hu_run_2019() 通过flask "/"路由，指定GET请求方法，读取GDP per person.csv 文件数据内容 并以results2.html文件作为模板以响应返回 
7. hu_run_select() 通过 "/hurun"路由，指定POST请求方式， 调用gbar_gdp、 grid_mutil_yaxis、 map_data函数将结果返回web界面
8. logger封装 日志模块 记录日志信息 并将日志数据存储；log文件夹下
	
###HTML文档：
1. html使用jinjia2 模板语言+html+JavaScript制作。其中模板语言主要使用了循环和判断，用于自动生成表格和翻页按钮。
2. 页面中使用了 echart 库进行绘制，echart是JavaScript的一个第三方库。除此之外还通过html的<select>标签的onchange属性配合
3. JavaScript函数实现了页面刷新，通过<button>标签的onclick熟悉配合JavaScript实现翻页功能
***
