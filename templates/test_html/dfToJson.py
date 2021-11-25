from Public.sqlDB import MysqlDB, SqliteDB, SqliteDB1,mysqlDB



task_sql = '''
            SELECT DISTINCT(a.task_id) ,a.task_full_name,a.grade_id,a.subject_id,a.ett_user_id,a.teacher_name ,DATE_FORMAT(a.c_time,'%Y-%m-%d %H:%i:%s') as c_time   ,b.fz,sum(b.fm ) as fm  from
(SELECT DISTINCT(tt.task_id ) as task_id,tt.c_user_id  ,tt.task_full_name,aa.grade_id,aa.subject_id  ,tt.c_time,t.teacher_name,u.ett_user_id
from tp_task_info  tt, as_answer_sheet_info aa,teacher_info t,user_info u
where   tt.task_value_id = aa.paper_id  and aa.workbook_paper = 1 and tt.task_id in(-8741902140044,-3768746069475,-7683667653596,-6175349928972,-9422387613539,-114856040140,-8715068772681,-5200029367471)
and t.user_id = tt.c_user_id  and u.ref  = tt.C_USER_ID
GROUP BY task_id ) a
LEFT JOIN
(
SELECT * from (
SELECT tta.task_id ,count(DISTINCT jc.user_id ) as fm ,count(DISTINCT ttp.user_id) as fz FROM tp_task_allot_info tta, j_class_user jc,tp_task_performance ttp   
WHERE  tta.task_id in (-8741902140044,-3768746069475,-7683667653596,-6175349928972,-9422387613539,-114856040140,-8715068772681,-5200029367471)
and jc.class_id = tta.user_type_id and jc.RELATION_TYPE = '学生'  and tta.task_id = ttp.task_id
GROUP BY tta.task_id
)a
union all
SELECT * from (
SELECT aa.task_id , aa.fm ,bb.fz FROM (
SELECT tta.task_id ,count(DISTINCT tjt.user_id ) as fm from tp_task_allot_info tta, tp_j_task_user tjt  WHERE  tta.task_id in  (-8741902140044,-3768746069475,-7683667653596,-6175349928972,-9422387613539,-114856040140,-8715068772681,-5200029367471)
and  tta.task_id = tjt.task_id
GROUP BY tta.task_id )aa
LEFT JOIN
(SELECT ttp.task_id ,count(DISTINCT ttp.user_id) as fz  from tp_task_performance ttp  WHERE ttp.task_id in (-8741902140044,-3768746069475,-7683667653596,-6175349928972,-9422387613539,-114856040140,-8715068772681,-5200029367471)
GROUP by  ttp.task_id
) bb  on aa.task_id = bb.task_id
) b
union all
SELECT * from
(
SELECT tta.task_id ,count(DISTINCT tjg.user_id ) as fm,count(DISTINCT ttp.user_id) as fz FROM tp_task_allot_info tta, tp_j_group_student tjg,tp_task_performance ttp   
WHERE  tta.task_id in(-8741902140044,-3768746069475,-7683667653596,-6175349928972,-9422387613539,-114856040140,-8715068772681,-5200029367471)
and   tta.task_id = ttp.task_id  and tta.user_type_id = tjg.group_id
GROUP BY tta.task_id
) c
) b  on a.task_id = b.task_id
GROUP BY a.task_id
ORDER BY  a.c_time  desc
            '''

data= mysqlDB(task_sql)
data_json = data.to_json(orient='records')
print(data)
print(data_json)