import requests
import json
from pyecharts.charts import Bar
from pyecharts import options as opts

# %%
# 四中考试
# 初一：9093649086778  初二：9151259628052   初三：9173900194585

# 十五中考试
# 高一：3153806314730  高二：3183950500193

exam_id = 3183950500193

# 对比考试的列表
compareExamArray = ''

# 对比类型  1=区域四率  2=区域百分位  3=学校四率  4=学校百分位
compareType = '4'

# -1=区域  0=本校  1=行政班  2=行政班群  3=分层班  4=分层班群
objectTypes = '0,2'

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXRhaWwiOnsidXNlcklkIjoyOTUxNjM1LCJ1c2VyTmFtZSI6IuWkp-i_nua1i-ivlTAwMSIsInBhc3N3b3JkIjoiIiwidXNlcklkZW50aXR5IjoxLCJlbmFibGUiOjEsInNjaG9vbFVzZXJJZCI6MzY3Njg2LCJzY2hvb2xJZCI6NTAwNDMsInNjaG9vbFVzZXJSZWYiOiJmYzI4Y2IwYi1lMDRmLTQ0ODUtOTQ4Yi02M2Q0NTU2ZmNlNGEiLCJzY2hvb2xHcm91cElkIjo3LCJyb2xlcyI6WzE2LDE3LDIsMjEsNiw5LDEzLDE1XSwidXJsTGlzdCI6bnVsbH0sImV4cCI6MTYyMDY0NjgwOSwidXNlcl9uYW1lIjoi5aSn6L-e5rWL6K-VMDAxIiwianRpIjoiM2MzYTBmYzEtNGIwYi00ODllLWI2YTYtNjg4ZDM5OGI5MGUwIiwiY2xpZW50X2lkIjoiRkE5RTIxNUJFNTY2RUU5MjYxNEZCQzExQUJFREY5NjgiLCJzY29wZSI6WyJhbGwiLCJ3ZWIiLCJtb2JpbGUiXX0.3-ey4CzNjlU4QsYEIWFoZI5vfaXf2V6unmzSU6K2Exk'

# ("全科",0),("三科",-1),("语文",1),("数学",2),("英语",3),("物理",4),("化学",5),("历史",6),("生物",7),("地理",8),("政治",9),("科学",10)
# subject_id_list = [-2,-1,0,1,2,3,4,5,6,7,8,9,10,11]
subject_id_dict = {'全科': 0,
                   '三科': -1,
                   '语文': 1,
                   '数学': 2,
                   '英语': 3,
                   '物理': 4,
                   '化学': 5,
                   '历史': 6,
                   '生物': 7,
                   '地理': 8,
                   '政治': 9,
                   '科学': 10,
                   '体育': 11}
# %%
for subject in subject_id_dict:
    get_url = 'https://school-cloud.etiantian.com/school-statistics/exam-analysis/school-area-score-multiple-line?examId={}&compareType={}&compareExamArray=&objectTypes={}&r=0.2526140433758095&examSubjectId={}&token={}'.format(
        exam_id, compareType, objectTypes, subject_id_dict[subject], token)
    ret = requests.get(url=get_url)
    text = json.loads(ret.text)

    print('----------')
    print('学科：', subject)

    # X轴数据
    x_list = []
    for x in text['data']['pointXList']:
        x_list.append(x)
    print('X轴分段：', x_list)

    # Y轴人数
    for i in text['data']['polyLines']:
        #     print(i)
        name_list = []
        value_list = []
        for p in i['pointArray']:
            name_list.append(p['name'])
        #         value_list.append(p['value'])
        print('{}：'.format(i['objectName']), name_list)

# %%
    # 绘制eycharts
    bar = Bar(init_opts=opts.InitOpts(width='1500px', height='600px'))
    bar.set_global_opts(xaxis_opts=opts.AxisOpts(
        axislabel_opts={"interval": "0", "rotate": 45},
    ), )

    bar.add_xaxis(
        x_list

    )
    bar.add_yaxis(subject,
                  name_list
                  )

    bar.render(r'F:\PythonObject\jupyter\十五中高二2分段柱状图\{}.html'.format(subject))
