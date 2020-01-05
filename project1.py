import re
import os
import json
import time
import logger
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line, Scatter, Geo, Map, Timeline, Page
from pyecharts.faker import Collector, Faker
from pyecharts.globals import ChartType
from flask import Flask, render_template, request


 
log = logger.Logger("debug")    # 日志初始化

country_ls = ['Australia', 'Canada', 'Switzerland', 'United Kingdom', 'Japan',
              'Netherlands', 'Norway', 'Singapore', 'Sweden', 'United States']


def getCsvData(filePath, rowName):
    """
    获取csv文件数据
    :Param filePath: 文件路径名称
    :Param rowName: csv表格列名
    :return: 返回国家名称，csv数据信息，年份信息
    """
    csv_data = {}
    years = []
    countries = []
    try:
        df = pd.read_csv(filePath)
        df.fillna(0, inplace=True)
        countries = df[rowName].tolist()
        years = df.columns.tolist()
        del years[0]
        del years[0]
        del years[-1]
        del years[-1]
        for year in years:
            csv_data[year] = df[year].tolist()
        log.info("{0} read success".format(filePath))
    except Exception as ex:
        log.error("{0} get failed：{1}".format(filePath, str(ex)))
    return countries, csv_data, years


def readCsvData(filePath, rowName):
    """
    提取csv文件数据
    :Param filePath: 文件路径名称
    :Param rowName: csv表格列名
    :return: csv数据信息，年份信息
    """
    csv_data = {}
    years = []
    try:
        df = pd.read_csv(filePath)
        df.fillna(0, inplace=True)
        years = df.columns.tolist()
        del years[0]
        del years[0]
        del years[-1]
        del years[-1]
        for year in years:
            csv_data[year] = []
            for i in range(len(df)):
                country = df[rowName].loc[i]
                value = df[year].loc[i]
                if country in country_ls:
                    csv_data[year].append(value)
        log.info("{0} read success".format(filePath))
    except Exception as ex:
        log.error("{0} get failed：{1}".format(filePath, str(ex)))
    return csv_data, years


def map_data(data, tableName, titleName) -> Map:
    """
    地图数据生成函数
    :Param data: 地图填充数据
    """
    try:
        name, value = data[0], data[1]
        new_name, new_value = [], []
        for index, temp in enumerate(data[1]):
            if temp > 0:
                new_name.append(name[index])
                new_value.append(value[index])
        name, value = new_name, new_value
        c = (
            Map(init_opts=opts.InitOpts(page_title="Luwei"))
                .add(tableName, [list(z) for z in zip(name, value)], "world", is_map_symbol_show=False)
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(title_opts=opts.TitleOpts(title=titleName),
                visualmap_opts=opts.VisualMapOpts(),
                toolbox_opts=opts.ToolboxOpts(),
            )
        )
        return c
    except Exception as ex:
        log.error("Map create failed：{0}".format(str(ex)))
        return None



def bar_gdp(data):
    """柱状图"""
    try:
        x_data = data[0]
        c = (
            Bar().add_xaxis(x_data)
                .add_yaxis("增长率(%)", list(map(lambda x: round(x, 1), data[1])), category_gap="20%", color="#675bba")
                .set_global_opts(
                    title_opts=opts.TitleOpts(title="人均GDP年增长率"),
                    toolbox_opts=opts.ToolboxOpts(),
                    yaxis_opts=opts.AxisOpts(offset=0),
                    xaxis_opts=opts.AxisOpts(
                        type_="category", 
                        offset=int(min(data[1]) * 15),
                        axislabel_opts=opts.LabelOpts(
                            rotate=30, font_weight="bold", interval=0, font_size=12, border_width=5
                        ),
                    ),
                )
            )
        log.info("柱状图创建成功")
        return c
    except Exception as ex:
        log.error("柱状图创建失败: {0}".format(str(ex)))
        return None



def grid_mutil_yaxis(data, info):
    """折线图与柱状图"""
    try:
        x_data = data[0]
        bar = (
            Bar().add_xaxis(x_data)
                .add_yaxis(info[0], list(map(lambda x: round(x, 1), data[1])), yaxis_index=0, color="#5793f3",)
                .extend_axis(
                    yaxis=opts.AxisOpts(
                        name=info[1], type_="value", 
                        min_=0, max_=max(data[2])*1.2, position="right",
                        axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#d14a61")),
                        axislabel_opts=opts.LabelOpts(formatter="{value}"),
                        splitline_opts=opts.SplitLineOpts(is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)),
                    )
                )
                .set_global_opts(
                    xaxis_opts=opts.AxisOpts(
                        type_="category",
                        axislabel_opts=opts.LabelOpts(rotate=30, interval=0, font_size=10, font_weight="bold")),
                    yaxis_opts=opts.AxisOpts(
                        name=info[0], max_=8, position="left", 
                        axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#5793f3")),
                    axislabel_opts=opts.LabelOpts(formatter="{value}"),),
                    title_opts=opts.TitleOpts(title="生育率与GDP增长率对比图"),
                    tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
                )
            )
        line = (
            Line()
                .add_xaxis(x_data)
                .add_yaxis("生育率", data[2], yaxis_index=1, color="#675bba",
                    label_opts=opts.LabelOpts(is_show=False),
                    linestyle_opts=opts.LineStyleOpts(width=4, opacity=1))
            )
        bar.overlap(line)
        log.info("折线图与柱状图创建成功")
        return Grid().add(bar, opts.GridOpts(pos_left="5%", pos_right="20%"), is_control_axis_index=True)
    except Exception as ex:
        log.error("折线图与柱状图创建失败: {0}".format(str(ex)))
        return None


app = Flask(__name__)

countries, data1, years1 = getCsvData("pregrant.csv", "Country")
countries, data2, years2 = getCsvData("literacy.csv", "Country Name")
data3, years3 = readCsvData("GDP per person.csv", "Country Name")
data4, years4 = readCsvData("literacy.csv", "Country Name")
regions_available = years4


@app.route('/', methods=['GET'])
def hu_run_2019():
    try:
        df = pd.read_csv("GDP per person.csv")
        data_str = df.to_html()
        return render_template('results2.html',
                            the_res=data_str,
                            the_select_region=regions_available)
    except Exception as ex:
        log.error("页面初始化失败: {0}".format(str(ex)))
        return None


@app.route('/hurun', methods=['POST'])
def hu_run_select() -> 'html':
    try:
        df = pd.read_csv("GDP per person.csv")
        the_region = request.form["the_region_selected"]    # 年份勾选
        log.info("勾选年份为{0}".format(the_region))
        fig5 = bar_gdp([country_ls, data3[the_region]])
        fig6 = grid_mutil_yaxis([country_ls, data3[the_region], data4[the_region]], ["GDP增长率(%)", "生育率(%)"])
        fig7 = map_data([countries, data2[the_region]], "识字率", "1990-2017女性识字率世界地图")
        fig8 = map_data([countries, data1[the_region]], "生育率", "1990-2017青春期女性生育率世界地图")

        page = Page(layout=Page.SimplePageLayout)
        page.add(fig5, fig6, fig7, fig8)
        page.render("task2.html")
        with open("task2.html", encoding="utf8", mode="r") as f:
            plot_all = "".join(f.readlines())
            
        data_str = df.to_html()
        return render_template('results2.html', the_plot_all=plot_all, the_res=data_str, the_select_region=regions_available,)
    except Exception as ex:
        log.error("页面数据请求失败: {0}".format(str(ex)))
        return None


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8888)   # 端口设置为8888 可进行修改配置
