import sqlite3
from functools import reduce
import datetime
from Public.sqlDB import mysqlDB, mysqlSqlite, SqliteDB
import  pandas as pd

b_time = datetime.datetime.now()

# school_course_task
school_course_task_sql = '''
         SELECT fr.school_id,fr.name,tc.course_id,tc.course_name ,g.grade_name,s.subject_name ,tt.task_id,tt.task_full_name,tt.c_user_id ,t.teacher_name ,tt.task_type ,tt.c_time,tt.correct_model
        FROM tp_task_info tt ,tp_course_info tc,franchised_school_info fr,teacher_info t,tp_j_course_class tjc,subject_info s,grade_info g 
        WHERE tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0 and tt.c_time  >'2020-7-15 0:00:00'  and tc.LOCAL_STATUS = 1 
        and fr.school_type in (3,4) and tt.C_USER_ID = t.user_id and tjc.course_id = tc.course_id  and tjc.subject_id = s.subject_id and tjc.grade_id = g.grade_id 
        '''

# j_task_class
task_class_sql = '''
   SELECT task_id ,user_type_id as task_class_count FROM tp_task_allot_info where user_type = 0   and c_time  >'2020-7-15 0:00:00'

'''

# j_task_group
task_group_sql = '''
    SELECT tta.task_id ,tg.class_id   
    FROM tp_task_allot_info tta LEFT JOIN  tp_group_info tg on  tg.group_id = tta.user_type_id 
    where tta.user_type = 2  
    and tta.c_time  >'2020-7-15 0:00:00'

'''

# every_day_task
every_day_task_sql = '''
SELECT DATE_FORMAT(tt.c_time,'%Y-%m-%d') as time,tt.TASK_TYPE,count(tt.task_id) as task_count
FROM tp_task_info tt ,tp_course_info tc,franchised_school_info fr
WHERE tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0 and tt.c_time  >'2020-7-15 0:00:00'  and tc.LOCAL_STATUS = 1 
and fr.school_type in (3,4)
GROUP BY time ,tt.TASK_TYPE
ORDER BY time DESC
'''

# every_day_axptask
every_day_axptask_sql = '''
SELECT DATE_FORMAT(tt.c_time,'%Y-%m-%d') as time,tt.TASK_TYPE,count(tt.task_id) as axp_task_count
FROM tp_task_info tt ,tp_course_info tc
WHERE tc.course_id = tt.COURSE_ID   and tt.c_time  >'2020-7-15 0:00:00'  and tc.LOCAL_STATUS = 1 
and tc.DC_SCHOOL_ID in ( 
SELECT distinct (fr.school_id)
from  class_info c, franchised_school_info fr  
where  c.axp_end_time >NOW()  and fr.school_type in (3,4) and fr.school_id =c.DC_SCHOOL_ID  and c.year = '2020~2021' and fr.school_id >50000 and fr.enable = 0 
)
GROUP BY time ,tt.TASK_TYPE
ORDER BY time DESC
'''

task_dfs = [mysqlDB(every_day_task_sql),
           mysqlDB(every_day_axptask_sql)]
df_merge = reduce(lambda left, right: pd.merge(left, right, on=['time', 'TASK_TYPE'], how='left'), task_dfs)

# 填充空缺数据为0
task_count = df_merge.fillna(0)


# every_day_course
every_day_course_sql = '''
SELECT DATE_FORMAT(tt.c_time,'%Y-%m-%d') as time,tt.TASK_TYPE,count(tt.task_id) as task_count
FROM tp_task_info tt ,tp_course_info tc,franchised_school_info fr
WHERE tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0 and tt.c_time  >'2020-7-15 0:00:00'  and tc.LOCAL_STATUS = 1 
and fr.school_type in (3,4)
GROUP BY time ,tt.TASK_TYPE
ORDER BY time DESC
'''

# every_day_axpcourse
every_day_axpcourse_sql = '''
SELECT DATE_FORMAT(tt.c_time,'%Y-%m-%d') as time,tt.TASK_TYPE,count(tt.task_id) as axp_task_count
FROM tp_task_info tt ,tp_course_info tc
WHERE tc.course_id = tt.COURSE_ID   and tt.c_time  >'2020-7-15 0:00:00'  and tc.LOCAL_STATUS = 1 
and tc.DC_SCHOOL_ID in ( 
SELECT distinct (fr.school_id)
from  class_info c, franchised_school_info fr  
where  c.axp_end_time >NOW()  and fr.school_type in (3,4) and fr.school_id =c.DC_SCHOOL_ID  and c.year = '2020~2021' and fr.school_id >50000 and fr.enable = 0 
)
GROUP BY time ,tt.TASK_TYPE
ORDER BY time DESC
'''

course_dfs = [mysqlDB(every_day_course_sql),
           mysqlDB(every_day_axpcourse_sql)]
course_df_merge = reduce(lambda left, right: pd.merge(left, right, on=['time', 'TASK_TYPE'], how='left'), course_dfs)

# 填充空缺数据为0
course_count = course_df_merge.fillna(0)


# school_class_user
school_class_user_sql = '''
SELECT fr.school_id,fr.name, class_count, axp_class_count, tea.tea_count as tea_count,stu.stu_count as  stu_count
from  (SELECT fr.school_id,fr.name from franchised_school_info fr  where fr.school_type in (3,4) and fr.school_id  >50000 and fr.enable = 0  and fr.validity_time >=NOW() )fr
LEFT JOIN (SELECT DC_SCHOOL_ID,count(distinct class_id) as class_count from  class_info  where year = '2021~2022' GROUP BY DC_SCHOOL_ID )c on fr.school_id = c.dc_school_id 
LEFT JOIN ( SELECT c.DC_SCHOOL_ID , count(DISTINCT jc.user_id ) as 'tea_count' from j_class_user jc ,class_info c  where c.year = '2021~2022' and c.class_id = jc.class_id and jc.RELATION_TYPE = '任课老师' GROUP BY c.DC_SCHOOL_ID  ) tea  on tea.DC_SCHOOL_ID = fr.school_id
LEFT JOIN ( SELECT c.DC_SCHOOL_ID , count(DISTINCT jc.user_id ) as 'stu_count' from j_class_user jc ,class_info c  where c.year = '2021~2022'and c.class_id = jc.class_id and jc.RELATION_TYPE = '学生' GROUP BY c.DC_SCHOOL_ID  ) stu on stu.DC_SCHOOL_ID = fr.school_id
LEFT JOIN (SELECT DC_SCHOOL_ID,count(distinct class_id) as axp_class_count from class_info where year = '2021~2022'  and axp_end_time >NOW()  GROUP BY DC_SCHOOL_ID) axp on axp.DC_SCHOOL_ID = fr.school_id
group by fr.school_id


'''

# paper_online_info
paper_online_sql = '''
SELECT ot.grade_id,g.grade_name,ot.subject_id,s.subject_name ,p.wisdom_exam,p.paper_id,p.paper_name,p.c_time,u.user_id,t.teacher_name,fr.school_id,fr.name
from paper_info p,online_test_paper_info ot,subject_info s,grade_info g ,user_info u,teacher_info t,(SELECT distinct (school_id),name from   franchised_school_info   where   school_type in (3,4)   and school_id >50000 and enable = 0 ) fr
where  p.wisdom_exam in (1,2) and  p.paper_id = ot.paper_id  and ot.enable = 1  and ot.grade_id = g.grade_id and ot.subject_id = s.subject_id and u.user_id = p.c_user_id and u.DC_SCHOOL_ID = fr.school_id and t.user_id = u.ref
GROUP BY  p.paper_id
ORDER BY fr.school_id
'''



if __name__ == '__main__':
    con = sqlite3.connect('F:\\PythonObject\\SchoolObject\\db.sqlite3')
    # mysqlSqlite(sql=school_course_task_sql, db_name='school_course_task')
    # mysqlSqlite(sql=every_day_task_sql, db_name='every_day_task')
    mysqlSqlite(sql=school_class_user_sql, db_name='school_class_user')
    mysqlSqlite(sql=paper_online_sql, db_name='paper_online_info')
    # mysqlSqlite(sql=task_class_sql, db_name='j_task_class')
    # mysqlSqlite(sql=task_group_sql, db_name='j_task_group')
    task_count.to_sql(name='every_day_task',con=con, if_exists='replace', index=False)
    # course_count.to_sql(name='every_day_course',con=con, if_exists='replace', index=False)
    e_time = datetime.datetime.now()
    lenth_time = (e_time - b_time)
    print('开始时间：', b_time.strftime('%Y-%m-%d %H:%M:%S'))
    print('结束时间：', e_time.strftime('%Y-%m-%d %H:%M:%S'))
    print('同步时长：', lenth_time)

    course_update_sql = '''
             UPDATE updata_table SET c_time = '{}' WHERE table_name in ( 'every_day_course','every_day_task','school_class_user','paper_online_info')
        '''.format(e_time.strftime('%Y-%m-%d %H:%M:%S'))
    print(SqliteDB(course_update_sql).updatedb())


