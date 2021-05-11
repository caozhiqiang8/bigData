from pyecharts import options as opts
from pyecharts.charts import Line, Bar, Pie


def echarts_bar(x_data, y_data):
    bar = Bar(init_opts=opts.InitOpts(width='1200px'))
    bar.add_xaxis(x_data)
    bar.add_yaxis("开通学校数量", y_data)
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title=""),
        datazoom_opts=opts.DataZoomOpts(is_show=True, type_='slider'),

    )

    bar.set_series_opts(
        label_opts=opts.LabelOpts(is_show=True),
        markline_opts=opts.MarkLineOpts(
            data=[

                opts.MarkLineItem(type_="average", name="平均值"),
            ]
        ),
        markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_="min", name="最小值"),
                opts.MarkPointItem(type_="max", name="最大值"),
            ]
        ),
    )
    return bar


def echarts_lin(x_data_list, y_name, y_data_list):
    # 渲染图大小
    line = Line(init_opts=opts.InitOpts(width='1000px'))

    # X轴数据
    line.add_xaxis(x_data_list)

    # Y轴名称和
    for i_name, i_reslut in zip(y_name, y_data_list):
        if i_name  not in ('学资源', '讨论', '单题',  '微课程', '一般任务', '直播课', '个性化', '先声'):
            line.add_yaxis('{}'.format(i_name), i_reslut, is_selected=True)
        else:
            line.add_yaxis('{}'.format(i_name), i_reslut, is_selected=False)

    # 全局配置
    line.set_global_opts(
        # 主标题
        title_opts=opts.TitleOpts(title=""),
        # 缩放功能
        datazoom_opts=opts.DataZoomOpts(is_show=True, type_='slider', range_start=90, range_end=100),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        xaxis_opts=opts.AxisOpts(
            axislabel_opts={"interval": "0", "rotate": 45},
        ),

    )

    # 系统配置
    line.set_series_opts(
        # 图中显示数值
        label_opts=opts.LabelOpts(is_show=True),

        # 线装图，平均线
        markline_opts=opts.MarkLineOpts(
            data=[opts.MarkLineItem(type_="average", name="平均值"), ]
        ),
        # 点装图，最大值最小值
        markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_="min", name="最小值"),
                opts.MarkPointItem(type_="max", name="最大值"),
            ]
        ),
    )

    return line
