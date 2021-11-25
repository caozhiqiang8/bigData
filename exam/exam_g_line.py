from IPython.core.display import display
from pyecharts import options as opts
from pyecharts.charts import Sankey
import pandas as pd
import numpy as np
from functools import reduce

#打印所以列
pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.width', 180)

exam_name = ['期中', '期末', '一模', '二模']

def examStuG(stu_exam, g_line, exam_name):
    #     print('考试类型：', exam_name)
    subject_name = g_line['学科'].tolist()
    #     print('学科列表：', subject_name)
    g_line_name = list(reversed(g_line.iloc[:, 3:].columns.tolist()))
    #     print('G10列表:', g_line_name)

    g_line_data = []
    # 取考试G10过程线数据
    for i in subject_name:
        # 处理考试数据 - 改成 0
        # stu_exam[i] = stu_exam[i].replace(['-'], [0])

        # 把过程线变成列表,,翻转G10数据，，G10是好学生，，G1是差学生
        g_line_data.append(list(reversed(g_line[(g_line['学科'] == i)].iloc[0:, 3:].values.tolist()[0])))
    #     g_line_data.append((g_line[(g_line['学科'] == i )].iloc[0:,3:].values.tolist()[0]))

    g_line_dict = dict(zip(subject_name, g_line_data))
    #     print('学科过程线字典',g_line_dict)

    exam_g = []
    for subject, gline in g_line_dict.items():
        # 根据学科进行降序排序
        stu_exam = stu_exam.sort_values(by=subject, ascending=False)
        stu_exam.reset_index(drop=True, inplace=True)

        # 学生每个学科G10数据列表
        stu_sub_g = []

        # 计算学生的G10数据
        for i in range(0, 10):
            if i != 0:
                stu_exam_g = stu_exam.iloc[np.sum(gline[:i]): np.sum(gline[:i + 1]):]
                stu_exam_g['{}{}G10'.format(exam_name, subject)] = '{}{}'.format(exam_name, g_line_name[i])
                stu_sub_g.append(stu_exam_g)

            else:
                stu_exam_g = stu_exam.iloc[:gline[i], :]
                stu_exam_g['{}{}G10'.format(exam_name, subject)] = '{}{}'.format(exam_name, g_line_name[i])
                stu_sub_g.append(stu_exam_g)

        # 先合并学生G10数据，然后把每个学科的加到列表中
        exam_g.append(pd.concat(stu_sub_g, axis=0))

    # 合并学生每个学科的G10数据
    exam_sub_merge = reduce(lambda left, right: pd.merge(left, right, on=stu_exam.columns.tolist(), how='left'), exam_g)
    return exam_sub_merge


exam_stu_g_list = []
for i in range(0, len(exam_name)):
    exam_type = exam_name[i]

    # 读取学学生考试数据
    stu_exam = pd.read_excel('C:\\Users\\caozhiqiang\\Desktop\\理工附学生成绩.xlsx', sheet_name='{}'.format(exam_type))
    # 读取考试G10线
    g_line = pd.read_excel('C:\\Users\\caozhiqiang\\Desktop\\理工附G10工作线.xlsx', sheet_name='{}'.format(exam_type))

    exam_stu_g_list.append(examStuG(stu_exam=stu_exam, g_line=g_line, exam_name=exam_type))

exam_stu_g_merge = reduce(lambda left, right: pd.merge(left, right, on=['姓名', '学号', '班级'], how='left'), exam_stu_g_list)
# print(exam_stu_g_merge)

# 导出学生计算后的G10成绩
# exam_stu_g_merge.to_excel('C:\\Users\\caozhiqiang\\Desktop\\初三G110.xlsx')
# print('导出成功')


exam_data = exam_stu_g_merge[['姓名', '学号', '班级', '期中语文G10', '期末语文G10', '一模语文G10', '二模语文G10']]
exam_g_type = exam_data.iloc[:, 3:].columns.tolist()

# 配色
colors = ['#FF0000', '#E84302', '#E87502', '#F1AA00', '#FCED00', '#CCF000', '#91DE00', '#51DE00', '#00B441',
          '#009034', ]

# 节点名称列表
nodes = []
# 数据流量列表
linkes = []
for i in range(0, len(exam_g_type)):

    if i != len(exam_g_type) - 1:

        star = exam_g_type[i]
        end = exam_g_type[i + 1]

        data = pd.DataFrame((exam_data.groupby(by=[star, end]).count())['学号'])
        # 分组后重置索引
        data = data.reset_index().sort_index('columns')
        # 调整列顺序
        data = data[[star, end, '学号']]
        # 修改列名字
        data.columns = [star[:2], end[:2], '人数']
        data_nodes = data.iloc[:, 0].unique()
    #         display(data)

    else:
        star = exam_g_type[i - 1]
        end = exam_g_type[i]

        data = pd.DataFrame((exam_data.groupby(by=[star, end]).count())['学号'])
        # 分组后重置索引
        data = data.reset_index().sort_index('columns')
        # 调整列顺序
        data = data[[star, end, '学号']]
        # 修改列名字
        data.columns = [star[:2], end[:2], '人数']

        # 返回列名唯一值
        data_nodes = data.iloc[:, 1].unique()
    #         display(data)
    #     print(data_nodes)

    # 循环节点名称
    for value in data_nodes:
        dic = {}
        for num in range(11):
            dic['name'] = value
            if value[2:] == 'G{}'.format(num):
                dic['itemStyle'] = {'color': colors[num - 1]}
        nodes.append(dic)

    # 循环节点数据流向
    for value in data.values:
        dic = {}
        dic['source'] = value[0]
        dic['target'] = value[1]
        dic['value'] = value[2]
        linkes.append(dic)


print(exam_g_type)

