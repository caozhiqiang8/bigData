from Public.sqlDB import mysqlDB
from functools import reduce
import pandas as pd

up_sql = '''
SELECT
  o.download_time "时间",
  o.GRADE_NAME "年级",
  o.subject_name "学科",
  count(if(o.diff_type= 1,1,null)) "微课下载数",
  count(if(o.diff_type= 0,1,null)) "课件下载数"
FROM
  (
    SELECT
      DATE_FORMAT(r.c_time, '%Y-%m') AS download_time,
      (
        SELECT
          g.GRADE_NAME
        FROM
          `tp_j_course_resource_info` AS j,
          `tp_j_course_teaching_material` AS t,
          `teaching_material_info` AS m,
          `grade_info` as g
        WHERE
          r.res_id = j.res_id
        AND j.course_id = t.course_id
        AND j.course_id > 0
        AND m.material_id = t.teaching_material_id
        and m.grade_id = g.GRADE_ID
        LIMIT 1
      ) AS GRADE_NAME,
      (
        SELECT
          s.subject_name
        FROM
          `tp_j_course_resource_info` AS j,
          `tp_j_course_teaching_material` AS t,
          `teaching_material_info` AS m,
          `subject_info` as s
        WHERE
          r.res_id = j.res_id
        AND j.course_id = t.course_id
        AND j.course_id > 0
        AND m.material_id = t.teaching_material_id
        and m.subject_id = s.subject_id
        LIMIT 1
      ) AS subject_name,
      r.res_id ,
      rs.diff_type
    FROM
      `yc_resource_access_records` AS r,`rs_resource_info` as rs
    WHERE
      r.r_type = 2 and r.res_id = rs.res_id
  ) AS o
WHERE
  o.GRADE_NAME IN ("高三年级","高二年级","高一年级")
GROUP BY
  o.download_time,
  o.GRADE_NAME,
  o.subject_name;
'''

click_sql = '''
SELECT
    o.download_time "时间",
    o.GRADE_NAME "年级",
    o.subject_name "学科",
    count(if(o.diff_type= 1,1,null)) "微课浏览数",
    count(if(o.diff_type= 0,1,null)) "课件浏览数"
FROM
    (
        SELECT
            DATE_FORMAT(r.c_time, '%Y-%m') AS download_time,
            (
                SELECT
                    g.GRADE_NAME
                FROM
                    `tp_j_course_resource_info` AS j,
                    `tp_j_course_teaching_material` AS t,
                    `teaching_material_info` AS m,
                    `grade_info` as g
                WHERE
                    r.res_id = j.res_id
                AND j.course_id = t.course_id
                AND j.course_id > 0
                AND m.material_id = t.teaching_material_id
                and m.grade_id = g.GRADE_ID
                LIMIT 1
            ) AS GRADE_NAME,
            (
                SELECT
                    s.subject_name
                FROM
                    `tp_j_course_resource_info` AS j,
                    `tp_j_course_teaching_material` AS t,
                    `teaching_material_info` AS m,
                    `subject_info` as s
                WHERE
                    r.res_id = j.res_id
                AND j.course_id = t.course_id
                AND j.course_id > 0
                AND m.material_id = t.teaching_material_id
                and m.subject_id = s.subject_id
                LIMIT 1
            ) AS subject_name,
            r.res_id ,
            rs.diff_type
        FROM
            `yc_resource_access_records` AS r,`rs_resource_info` as rs
        WHERE
            r.r_type = 1 and r.res_id = rs.res_id
    ) AS o
WHERE
    o.GRADE_NAME IN ("高三年级","高二年级","高一年级")
GROUP BY
    o.download_time,
    o.GRADE_NAME,
    o.subject_name;
'''
df = [
    mysqlDB(up_sql),
    mysqlDB(click_sql)
]
every_count = reduce(lambda left, right: pd.merge(left, right, on=['时间','年级','学科'], how='left'), df)
every_count = every_count.fillna(0)
# print(every_count)
every_count.to_excel(r'C:\Users\caozhiqiang\Desktop\运城资源数据.xlsx')
print('导出成功')
