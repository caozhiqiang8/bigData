import sqlite3
from functools import reduce
import  datetime
import  pandas as pd
from Public.sqlDB import mysqlDB, mysqlSqlite, sqliteDB, SqliteDB

b_time = datetime.datetime.now()
# 课件
word_grade_subject_sql = ('''
        SELECT g.grade_name,s.subject_name,COUNT(DISTINCT r.res_id) "word_count"
        FROM 
        rs_resource_info r,tp_j_course_resource_info tr,
        tp_course_info tc,`tp_j_course_teaching_material` ttm
        ,`teaching_material_info` tm
        ,`teach_version_info` tv
        ,grade_info g
        ,subject_info s
        WHERE tr.`course_id` = ttm.`course_id`
        AND r.res_id  = tr.`res_id`
        AND tc.`COURSE_ID` > 0 
        AND tc.`COURSE_ID` = tr.`course_id`
        AND ttm.`teaching_material_id` = tm.`material_id` AND tm.`version_id` =  tv.`version_id`
        AND tm.`grade_id` = g.`GRADE_ID` AND tm.`subject_id` = s.`SUBJECT_ID`
        AND tc.`LOCAL_STATUS` = 1
        AND r.`diff_type` = 0
        AND r.res_id > 0 
        AND r.`RES_STATUS` = 1
        GROUP BY g.grade_id,s.subject_id
        ORDER BY g.grade_id,s.subject_id
             ''')
word_grade_subject_count = mysqlDB(word_grade_subject_sql)

# 关联学案的微课
mp4_word_grade_subject_sql = ('''
        SELECT g.grade_name,s.subject_name,COUNT(DISTINCT r.res_id) as 'mp4_word_count'
        FROM 
        rs_resource_info r,tp_j_course_resource_info tr,
        tp_course_info tc,`tp_j_course_teaching_material` ttm
        ,`teaching_material_info` tm
        ,`teach_version_info` tv
        ,grade_info g
        ,subject_info s
        ,tp_study_j_module_resource aaa
        , j_mic_video_paper bbb
        WHERE tr.`course_id` = ttm.`course_id`
        AND r.res_id  = tr.`res_id`
        AND tc.`COURSE_ID` > 0 
        AND tc.`COURSE_ID` = tr.`course_id`
        AND ttm.`teaching_material_id` = tm.`material_id` AND tm.`version_id` =  tv.`version_id`
        AND tm.`grade_id` = g.`GRADE_ID` AND tm.`subject_id` = s.`SUBJECT_ID`
        AND tc.`LOCAL_STATUS` = 1
        AND aaa.resource_id = r.res_id
        AND aaa.resource_type = 32
        AND r.`diff_type` = 1
        AND r.res_id > 0 
        AND r.`RES_STATUS` = 1
        AND bbb.`mic_video_id` = r.res_id
        AND EXISTS(
          SELECT 1 FROM tp_study_j_module_resource ppp
           WHERE aaa.module_id=ppp.module_id
        AND  ppp.resource_type=33
        )
        GROUP BY g.grade_id,s.subject_id
        ORDER BY g.grade_id,s.subject_id
             ''')
mp4_word_grade_subject_count = mysqlDB(mp4_word_grade_subject_sql)

# 微课关联的学案
word_mp4_grade_subject_sql = ('''
        SELECT g.grade_name,s.subject_name, COUNT(DISTINCT r.res_id) as 'word_mp4_count'
        FROM 
        rs_resource_info r,tp_j_course_resource_info tr,
        tp_course_info tc,`tp_j_course_teaching_material` ttm
        ,`teaching_material_info` tm
        ,`teach_version_info` tv
        ,grade_info g
        ,subject_info s
        ,tp_study_j_module_resource aaa
        WHERE tr.`course_id` = ttm.`course_id`
        AND r.res_id  = tr.`res_id`
        AND tc.`COURSE_ID` > 0 
        AND tc.`COURSE_ID` = tr.`course_id`
        AND ttm.`teaching_material_id` = tm.`material_id` AND tm.`version_id` =  tv.`version_id`
        AND tm.`grade_id` = g.`GRADE_ID` AND tm.`subject_id` = s.`SUBJECT_ID`
        AND tc.`LOCAL_STATUS` = 1
        AND aaa.resource_id = r.res_id
        AND aaa.resource_type = 33
        AND r.`diff_type` = 0
        AND r.res_id > 0 
        AND r.`RES_STATUS` = 1
        AND EXISTS(
          SELECT 1 FROM tp_study_j_module_resource ppp
           WHERE aaa.module_id=ppp.module_id
        AND  ppp.resource_type=32
        )
        GROUP BY g.grade_id,s.subject_id
        ORDER BY g.grade_id,s.subject_id
                     ''')
word_mp4_grade_subject_count = mysqlDB(word_mp4_grade_subject_sql)

# 微课
mp4_grade_subject_sql = ('''
        SELECT g.grade_name,s.subject_name,COUNT(DISTINCT r.res_id) "mp4_count"
        FROM 
        rs_resource_info r,tp_j_course_resource_info tr,
        tp_course_info tc,`tp_j_course_teaching_material` ttm
        ,`teaching_material_info` tm
        ,`teach_version_info` tv
        ,grade_info g
        ,subject_info s
        WHERE tr.`course_id` = ttm.`course_id`
        AND r.res_id  = tr.`res_id`
        AND tc.`COURSE_ID` > 0 
        AND tc.`COURSE_ID` = tr.`course_id`
        AND ttm.`teaching_material_id` = tm.`material_id` AND tm.`version_id` =  tv.`version_id`
        AND tm.`grade_id` = g.`GRADE_ID` AND tm.`subject_id` = s.`SUBJECT_ID`
        AND tc.`LOCAL_STATUS` = 1
        AND r.`diff_type` = 1
        AND r.res_id > 0 
        AND r.`RES_STATUS` = 1
        GROUP BY g.grade_id,s.subject_id
        ORDER BY g.grade_id,s.subject_id
             ''')
mp4_grade_subject_count = mysqlDB(mp4_grade_subject_sql)

# 成卷
cpaper_grade_subject_sql = ('''
        SELECT g.grade_name,s.subject_name,COUNT(DISTINCT p.paper_id) "cpaper_count" FROM `online_test_paper_info` p,subject_info s,grade_info g 
        WHERE paper_id > 0
        AND g.grade_id = p.grade_id
        AND s.subject_id= p.subject_id
        AND paper_status = 1
        GROUP BY g.grade_id,s.subject_id
        ORDER BY g.grade_id,s.subject_id
             ''')
cpaper_grade_subject_count = mysqlDB(cpaper_grade_subject_sql)

# AB卷
paper_grade_subject_sql = ('''
        SELECT g.grade_name,s.subject_name,COUNT(DISTINCT p.paper_id) "paper_count"
        FROM paper_info p
        ,tp_j_course_paper tr
        ,tp_course_info tc
        ,tp_j_course_teaching_material ttm
        ,teach_version_info tv
        ,teaching_material_info tm
        ,grade_info g
        ,subject_info s
        WHERE tr.`course_id` = ttm.`course_id`
        AND p.paper_id = tr.`paper_id`
        AND tc.`COURSE_ID` > 0
        AND tc.`COURSE_ID` = tr.`course_id`
        AND ttm.`teaching_material_id` = tm.`material_id`
        AND tm.`version_id` = tv.`version_id`
        AND tm.`grade_id` = g.`GRADE_ID`
        AND tm.`subject_id` = s.`SUBJECT_ID`
        AND tc.`LOCAL_STATUS` = 1
        AND p.paper_id > 0 
        AND p.`paper_type` IN (1,2)
        GROUP BY g.grade_id,s.subject_id
        ORDER BY g.grade_id,s.subject_id
             ''')
paper_grade_subject_count = mysqlDB(paper_grade_subject_sql)

# 试题
ques_grade_subject_sql = ('''
        SELECT g.grade_name,s.subject_name,COUNT(DISTINCT q.question_id) "question_count"
        FROM question_info q
        ,tp_j_course_question_info tr
        ,tp_course_info tc
        ,tp_j_course_teaching_material ttm
        ,teach_version_info tv
        ,teaching_material_info tm
        ,grade_info g
        ,subject_info s
        WHERE tr.`course_id` = ttm.`course_id`
        AND q.question_id = tr.`question_id`
        AND tc.`COURSE_ID` > 0
        AND tc.`COURSE_ID` = tr.`course_id`
        AND ttm.`teaching_material_id` = tm.`material_id`
        AND tm.`version_id` = tv.`version_id`
        AND tm.`grade_id` = g.`GRADE_ID`
        AND tm.`subject_id` = s.`SUBJECT_ID`
        AND tc.`LOCAL_STATUS` = 1
        AND q.`question_id` > 0 
        GROUP BY g.grade_id,s.subject_id
        ORDER BY g.grade_id,s.subject_id
             ''')
ques_grade_subject_count = mysqlDB(ques_grade_subject_sql)

# 合并表格
# word_grade_subject_count - 课件
# word_mp4_grade_subject_count - 微课关联的学案
# mp4_grade_subject_count - 微课
# mp4_word_grade_subject_count - 关联学案的微课
# cpaper_grade_subject_count - 成卷
# paper_grade_subject_count - AB卷
# ques_grade_subject_count - 试题

res_dfs = [word_grade_subject_count,
           word_mp4_grade_subject_count,
           mp4_grade_subject_count,
           mp4_word_grade_subject_count,
           cpaper_grade_subject_count,
           paper_grade_subject_count,
           ques_grade_subject_count]
df_merge = reduce(lambda left, right: pd.merge(left, right, on=['grade_name', 'subject_name'], how='left'), res_dfs)

# 填充空缺数据为0
res_count = df_merge.fillna(0)


if __name__ == '__main__':
    con = sqlite3.connect('F:\\PythonObject\\SchoolObject\\db.sqlite3')

    res_count.to_sql(name='resource_info', con=con, if_exists='replace', index=False)
    e_time = datetime.datetime.now()
    lenth_time = (e_time - b_time)
    print('开始时间：',b_time.strftime('%Y-%m-%d %H:%M:%S'))
    print('结束时间：',e_time.strftime('%Y-%m-%d %H:%M:%S'))
    print('同步时长：',lenth_time)
    res_update_sql = '''
             UPDATE updata_table SET c_time = '{}' WHERE table_name in ( 'resource_info')
        '''.format(e_time.strftime('%Y-%m-%d %H:%M:%S'))
    print(SqliteDB(res_update_sql).updatedb())
