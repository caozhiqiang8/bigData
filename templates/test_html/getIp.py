import json
from Public.sqlDB import mysqlDB
from functools import reduce
import pandas as pd


pd.set_option('display.max_columns',1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth',1000)
#
# sql = '''
# SELECT  GROUP_CONCAT(a.task_id ) as task_id  from
# (SELECT   DISTINCT(tt.task_id ) as task_id
# from tp_task_info  tt, school_info s ,as_answer_sheet_info aa
# where    s.school_id =53950  and s.SCHOOL_ID = aa.dc_school_id and tt.task_value_id = aa.paper_id  and aa.workbook_paper = 1) a
# '''
# task_list = mysqlDB(sql)
# task_list = json.loads(task_list.to_json(orient='records'))
# task_list = task_list[0]['task_id']
# print(task_list)
#
# task_sql = '''
# SELECT DISTINCT(tt.task_id ) as task_id,tt.c_user_id  ,tt.task_full_name,aa.grade_id,aa.subject_id  ,tt.c_time,t.teacher_name,u.ett_user_id
# from tp_task_info  tt, as_answer_sheet_info aa,teacher_info t,user_info u
# where   tt.task_value_id = aa.paper_id  and aa.workbook_paper = 1 and tt.task_id in({})
# and t.user_id = tt.c_user_id  and u.ref  = tt.C_USER_ID
# GROUP BY task_id
# '''.format(task_list)
#
# c_sql = '''
#
#         SELECT tta.task_id ,count(DISTINCT jc.user_id ) as fm ,count(DISTINCT ttp.user_id) as fz FROM tp_task_allot_info tta, j_class_user jc,tp_task_performance ttp
#         WHERE  tta.task_id in ({})
#         and jc.class_id = tta.user_type_id and jc.RELATION_TYPE = '学生'  and tta.task_id = ttp.task_id
#         GROUP BY tta.task_id
# '''.format(task_list)
#
# g_sql = '''
#       SELECT tta.task_id ,count(DISTINCT tjg.user_id ) as fm,count(DISTINCT ttp.user_id) as fz FROM tp_task_allot_info tta, tp_j_group_student tjg,tp_task_performance ttp
#         WHERE  tta.task_id in({})
#         and   tta.task_id = ttp.task_id  and tta.user_type_id = tjg.group_id
#         GROUP BY tta.task_id
# '''.format(task_list)
#
# stu_sql = '''
#  SELECT aa.task_id , aa.fm ,bb.fz FROM (
#     SELECT tta.task_id ,count(DISTINCT tjt.user_id ) as fm from tp_task_allot_info tta, tp_j_task_user tjt  WHERE  tta.task_id in ({0})
#     and  tta.task_id = tjt.task_id
#     GROUP BY tta.task_id )aa
#     LEFT JOIN
#     (SELECT ttp.task_id ,count(DISTINCT ttp.user_id) as fz  from tp_task_performance ttp  WHERE ttp.task_id in ({0})
#     GROUP by  ttp.task_id
#     ) bb  on aa.task_id = bb.task_id
# '''.format(task_list)
#
# pg_sql ='''
# SELECT task_id ,count(DISTINCT user_id ) as pg from as_stu_as_logs asa  where asa.task_id in ({0}) and is_marking = 1 and marking_count > 0
# GROUP BY task_id
# '''.format(task_list)
#
# df = pd.concat([mysqlDB(c_sql), mysqlDB(g_sql),mysqlDB(stu_sql)])
#
# task_dfs = [
#     mysqlDB(task_sql),
#     df,
# mysqlDB(pg_sql)]
# df_merge = reduce(lambda left, right: pd.merge(left, right, on=['task_id'], how='left'), task_dfs)
# df_merge = df_merge.fillna(0)
# df_merge_json = json.loads(df_merge.to_json(orient='records',force_ascii=False))
#
# # print(df_merge_json)
# print(df_merge_json)

# school_sql = '''
# SELECT GROUP_CONCAT(distinct s.school_id  ) as school_id
# from tp_task_info  tt, school_info s ,as_answer_sheet_info aa
# where    s.school_id not in ( 50043,51613,50041,53741,50068,53535)  and s.SCHOOL_ID = aa.dc_school_id and tt.task_value_id = aa.paper_id  and aa.workbook_paper = 1
# '''


every_sql = '''
SELECT DATE_FORMAT(tt.c_time,'%Y-%m-%d ') as vevry_day ,count(tt.task_id) as task_count
        from tp_task_info  tt, as_answer_sheet_info aa
        where   tt.task_value_id = aa.paper_id   and aa.workbook_paper=1 and aa.dc_school_id  not in ( 50043,51613,50041,53741,50068,53535)
        GROUP BY vevry_day
		ORDER BY vevry_day DESC
'''
every_day = mysqlDB(every_sql)


belong_school_sql = '''
SELECT distinct fr.belong_school_id ,os.name
from tp_task_info  tt, franchised_school_info fr ,as_answer_sheet_info aa ,oracle2utf.school_info os
where    fr.school_id not in ( 50043,51613,50041,53741,50068,53535)  and fr.SCHOOL_ID = aa.dc_school_id and tt.task_value_id = aa.paper_id  and aa.workbook_paper = 1 and os.school_id = fr.belong_school_id
GROUP BY fr.belong_school_id
'''
school = mysqlDB(belong_school_sql)
school_list = school['belong_school_id'].tolist()
# print(school_list)

df = [every_day,]
for i in school_list:
    school_sql = '''
    SELECT DATE_FORMAT(tt.c_time,'%Y-%m-%d ') as vevry_day ,count(tt.task_id) as task_count
        from tp_task_info  tt, as_answer_sheet_info aa ,franchised_school_info fr 
        where   tt.task_value_id = aa.paper_id   and aa.workbook_paper=1 and aa.dc_school_id  not in ( 50043,51613,50041,53741,50068,53535) and aa.DC_SCHOOL_ID = fr.school_id  and fr.belong_school_id = {}
        GROUP BY vevry_day
		ORDER BY vevry_day DESC
    '''.format(i)
    beschool = mysqlDB(school_sql)
    beschool.columns = ['vevry_day','{}'.format(i)]
    df.append(beschool)

every_count = reduce(lambda left, right: pd.merge(left, right, on=['vevry_day'], how='left'), df)
every_count = every_count.fillna(0)

column = ['vevry_day','task_count']
for i in school['name'].tolist():
    column.append(i)
every_count.columns = column
every_count_json = json.loads(every_count.to_json(orient='records', force_ascii=False))

every_count.loc['sum'] = every_count.iloc[:,1:].apply(lambda x:x.sum())


print(every_count)


# every_count.to_excel(r'C:\Users\caozhiqiang\Desktop\数据.xlsx')
# print('导出成功')




