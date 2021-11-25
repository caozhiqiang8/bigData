import datetime
from Public.sqlDB import  mysqlSqlite, SqliteDB,mysqlDB
from functools import reduce
import sqlite3
import  pandas as pd


def paperOnlineInfo():
    b_time = datetime.datetime.now()
    # paper_online_info
    paper_online_sql = '''
    SELECT ot.grade_id,g.grade_name,ot.subject_id,s.subject_name ,p.wisdom_exam,p.paper_id,p.paper_name,p.c_time,u.user_id,t.teacher_name,fr.school_id,fr.name
    from paper_info p,online_test_paper_info ot,subject_info s,grade_info g ,user_info u,teacher_info t,(SELECT distinct (school_id),name from   franchised_school_info   where   school_type in (3,4)   and school_id >50000 and enable = 0 ) fr
    where  p.wisdom_exam in (1,2) and  p.paper_id = ot.paper_id  and ot.enable = 1  and ot.grade_id = g.grade_id and ot.subject_id = s.subject_id and u.user_id = p.c_user_id and u.DC_SCHOOL_ID = fr.school_id and t.user_id = u.ref
    GROUP BY  p.paper_id
    ORDER BY fr.school_id
    '''
    mysqlSqlite(sql=paper_online_sql, db_name='paper_online_info')
    e_time = datetime.datetime.now()
    lenth_time = (e_time - b_time)
    course_update_sql = '''
             UPDATE updata_table SET c_time = '{}' WHERE table_name in ('paper_online_info')
        '''.format(e_time.strftime('%Y-%m-%d %H:%M:%S'))
    SqliteDB(course_update_sql).updatedb()

    data = {
        'b_time':b_time.strftime('%Y-%m-%d %H:%M:%S'),
        'e_time':e_time.strftime('%Y-%m-%d %H:%M:%S'),
        'lenth_time':lenth_time

    }

    return data

def everyDayTask():
    b_time = datetime.datetime.now()

    # every_day_task
    every_day_task_sql = '''
 		SELECT DATE_FORMAT(tt.c_time,'%Y-%m-%d') as time,tt.TASK_TYPE,count(tt.task_id) as task_count
    FROM tp_task_info tt ,tp_course_info tc,franchised_school_info fr
    WHERE tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0 and tt.c_time  >'2021-7-15 0:00:00'  and tc.LOCAL_STATUS = 1 
    and fr.school_type in (3,4)
    GROUP BY time ,tt.TASK_TYPE
    ORDER BY time DESC
    '''

    # every_day_axptask
    every_day_axptask_sql = '''
    SELECT DATE_FORMAT(tt.c_time,'%Y-%m-%d') as time,tt.TASK_TYPE,count(tt.task_id) as axp_task_count
    FROM tp_task_info tt ,tp_course_info tc
    WHERE tc.course_id = tt.COURSE_ID   and tt.c_time  >'2021-7-15 0:00:00'  and tc.LOCAL_STATUS = 1 
    and tc.DC_SCHOOL_ID in ( 
    SELECT distinct (fr.school_id)
    from  class_info c, franchised_school_info fr  
    where  fr.school_type in (3,4) and fr.school_id =c.DC_SCHOOL_ID   and fr.school_id >50000 and fr.enable = 0  and c.axp_begin_time is not null
    )
    GROUP BY time ,tt.TASK_TYPE
    ORDER BY time DESC
		
    '''

    task_dfs = [mysqlDB(every_day_task_sql),
                mysqlDB(every_day_axptask_sql)]
    df_merge = reduce(lambda left, right: pd.merge(left, right, on=['time', 'TASK_TYPE'], how='left'), task_dfs)

    # 填充空缺数据为0
    task_count = df_merge.fillna(0)
    con = sqlite3.connect('F:\\PythonObject\\SchoolObject\\db.sqlite3')

    task_count.to_sql(name='every_day_task',con=con, if_exists='replace', index=False)

    e_time = datetime.datetime.now()
    lenth_time = (e_time - b_time)
    course_update_sql = '''
             UPDATE updata_table SET c_time = '{}' WHERE table_name in ('every_day_task')
        '''.format(e_time.strftime('%Y-%m-%d %H:%M:%S'))
    SqliteDB(course_update_sql).updatedb()

    data = {
        'b_time':b_time.strftime('%Y-%m-%d %H:%M:%S'),
        'e_time':e_time.strftime('%Y-%m-%d %H:%M:%S'),
        'lenth_time':lenth_time
    }
    return data


if __name__ == '__main__':
    print(everyDayTask())
    print(paperOnlineInfo())