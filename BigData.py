import json, os, settings
from datetime import timedelta
from functools import wraps
from flask import Flask, render_template, request, redirect, session
from elasticsearch import Elasticsearch
from Public.ocr import imgOcr
from Public.token import token
from Public.sqlDB import MysqlDB, SqliteDB, SqliteDB1, mysqlDB
from Public.updateData import paperOnlineInfo
from Public.echarts import  echarts_lin
import pandas as pd
from functools import reduce

Config = settings.Config
app = Flask(__name__)
app.config.from_object(Config)
app.config["SECRET_KEY"] = "akjsdhkjashdkjhaksk120191101asd"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60 * 8)

basedir = os.path.abspath(os.path.dirname(__file__))


# 登录vue
@app.route("/")
@app.route("/login", methods=['get', 'post'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        data = request.get_json()
        # print(data)

        if data['username'] == 'admin' and data['password'] == '1111':
            masg = {
                'code': '0',
            }
            user_token = token()
            print(user_token)
            session['user_token'] = user_token
            session['username'] = 'admin'
            session['password'] = '1111'
            return masg
        else:
            masg = {
                'code': '1',
                'masg': '帐号密码错误'

            }
            return masg


# 数据更新时间
@app.route('/update', methods=['get'])
def update():
    # 更新时间

    update_sql = '''
                    SELECT strftime('%Y-%m-%d %H:%M:%S',C_TIME) as c_time  from updata_table where table_name = 'paper_online_info'
                                  '''
    update_time = SqliteDB(sql=update_sql).connectdb()[0]['c_time']
    data = {
        'code': '0',
        'update_time': update_time
    }
    return data


@app.route('/updatedata', methods=['get'])
def updatedata():
    data = paperOnlineInfo()
    print(data)
    return data


# session 验证装饰器
def singOut(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if not session.get('username'):
            return redirect('/login')
        return func(*args, **kwargs)

    return inner


# 首页路由
@app.route('/index', methods=['get'])
@singOut
def maptemp():
    return render_template('index.html')


# 首页api
@app.route('/mapdata', methods=['get'])
@singOut
def mapdata():
    sql = '''
    SELECT s.province as 'name',count(DISTINCT fr.SCHOOL_ID) as 'value'  from franchised_school_info fr,school_info s where fr.school_type in (3,4)   
    and fr.school_id  >50000 and fr.enable = 0  and s.school_id = fr.school_id and fr.validity_time >=NOW()
    GROUP BY s.province
            '''
    school_list = MysqlDB(sql).connectdb()

    # print(school_list)

    return {
        'map': school_list
    }


# 用户查询
@app.route('/user', methods=['get', 'post'])
@singOut
def user():
    if request.method == 'GET':
        return render_template('user.html')
    if request.method == 'POST':
        user_tea_name = request.form.get('user_tea_name')
        user_tea_id = request.form.get('user_tea_id')
        user_stu_name = request.form.get('user_stu_name')
        user_stu_id = request.form.get('user_stu_id')

        if user_tea_name:
            sql = ('''SELECT s.name,s.school_id ,u.ETT_USER_ID,oc.user_name , oc.password,t.TEACHER_NAME ,u.state_id,u.C_TIME
            from  oracle2utf.coschuser_info oc,user_info u,school_info s,teacher_info t
            where  oc.jid = u.ETT_USER_ID and u.DC_SCHOOL_ID = s.school_id and u.ref = t.user_id  
            and oc.user_name ='{}'
                '''.format(user_tea_name))
            data = MysqlDB(sql)
            tea_data = data.connectdb()
            # tea_data = tea_data.to_dict('records')

            return render_template('user.html', tea_data=tea_data)

        if user_tea_id:
            sql = ('''SELECT s.name,s.school_id ,u.ETT_USER_ID,oc.user_name , oc.password,t.TEACHER_NAME ,u.state_id,u.C_TIME
            from  oracle2utf.coschuser_info oc,user_info u,school_info s,teacher_info t
            where  oc.jid = u.ETT_USER_ID and u.DC_SCHOOL_ID = s.school_id and u.ref = t.user_id  
            and oc.jid ={}
            GROUP BY s.school_id ,u.ETT_USER_ID
            '''.format(user_tea_id))
            data = MysqlDB(sql)
            tea_data = data.connectdb()
            # tea_data = tea_data.to_dict('records')

            return render_template('user.html', tea_data=tea_data)

        if user_stu_name:
            sql = ('''SELECT s.name,s.school_id ,u.ETT_USER_ID,oc.user_name , oc.password,t.STU_NAME ,u.state_id,u.C_TIME
                    from  oracle2utf.user_info oc,user_info u,school_info s,student_info t 
                    where  oc.user_id = u.ETT_USER_ID and u.DC_SCHOOL_ID = s.school_id and u.ref = t.user_id 
                    and oc.user_name ='{}'				
                  '''.format(user_stu_name))
            data = MysqlDB(sql)
            stu_data = data.connectdb()
            # stu_data = stu_data.to_dict('records')
            return render_template('user.html', stu_data=stu_data)

        if user_stu_id:
            sql = ('''   SELECT s.name,s.school_id ,u.ETT_USER_ID,oc.user_name , oc.password,t.STU_NAME ,u.state_id,.uC_TIME
                        from  oracle2utf.user_info oc,user_info u,school_info s,student_info t 
                        where  oc.user_id = u.ETT_USER_ID and u.DC_SCHOOL_ID = s.school_id and u.ref = t.user_id 
                        and oc.user_id = {}
                  '''.format(user_stu_id))
            data = MysqlDB(sql)
            stu_data = data.connectdb()
            # stu_data = stu_data.to_dict('records')

            return render_template('user.html', stu_data=stu_data)


# 资源查询
@app.route('/resource', methods=['get'])
@singOut
def resource():
    if request.method == 'GET':
        sql = ''' 
                    SELECT * FROM "resource_info"
                '''
        res_data = SqliteDB(sql=sql).connectdb()
        # print(res_data)
        # 更新时间
        update_sql = ''' 
                    SELECT c_time from updata_table where table_name = 'resource_info'
                '''
        update_time = SqliteDB(sql=update_sql).connectdb()

        return render_template('resource.html', res_data=res_data, update_time=update_time)


# 组卷分布路由
@app.route('/papercount', methods=['get'])
@singOut
def papercount():
    if request.method == 'GET':
        return render_template('papercount.html')


# 年级学科分布路由
@app.route('/papergroup', methods=['get'])
@singOut
def papergroup():
    if request.method == 'GET':
        return render_template('papergroup.html')


# 组卷明细路由
@app.route('/paperlist', methods=['get'])
@singOut
def paperlist():
    if request.method == 'GET':
        return render_template('paperlist.html')


# 智能组卷api
@app.route('/paper', methods=['post'])
@singOut
def paper():
    code = request.get_json()
    # 类型分布
    update_sql = '''
                      SELECT strftime('%Y-%m-%d %H:%M:%S',C_TIME) as c_time  from updata_table where table_name = 'paper_online_info'
                                    '''
    update_time = SqliteDB(sql=update_sql).connectdb()[0]['c_time']

    if code['code'] == '0':

        sql = '''
                                SELECT wisdom_exam,COUNT( DISTINCT paper_id) as paper_count FROM "paper_online_info"
                                GROUP BY wisdom_exam

                                        '''
        paper_data = SqliteDB(sql=sql).connectdb()
        datas = {
            'masg': '成功',
            'paper_data': paper_data,
            'update_time': update_time
        }
        return datas
    # 年级学科分布
    elif code['code'] == '1':
        sql = '''    
        SELECT grade_name,subject_name,COUNT( DISTINCT paper_id)as paper_count FROM "paper_online_info"
        GROUP BY grade_id,subject_id
                                       '''

        paper_data = SqliteDB(sql=sql).connectdb()
        datas = {
            'masg': '成功',
            'paper_data': paper_data,
        }

        return datas
    # 组卷明细
    elif code['code'] == '2':
        sql = '''    
                    select grade_name,subject_name,wisdom_exam,paper_name,strftime('%Y-%m-%d %H:%M:%S',C_TIME) as c_time,teacher_name,school_id,name from paper_online_info
                    ORDER BY school_id
                    limit 0,1000
                               '''

        paper_data = SqliteDB(sql=sql).connectdb()

        datas = {
            'masg': '成功',
            'paper_data': paper_data,
        }

        return datas

    else:
        datas = {
            'masg': '失败',
        }
        return datas


# 学校基础数据 路由
@app.route('/school', methods=['get'])
@singOut
def school():
    return render_template('school.html')


# 学校基础数据 api
@app.route('/schooldata', methods=['post'])
@singOut
def schooldata():
    code = request.get_json()
    if code['code'] == '0':
        sql = '''
SELECT fr.school_id,fr.name, IFNULL(class_count,0) as class_count, IFNULL(axp_class_count,0) as axp_class_count , IFNULL(tea.tea_count,0) as tea_count,IFNULL(stu.stu_count,0) as  stu_count
from  (SELECT fr.school_id,fr.name from franchised_school_info fr  where fr.school_type in (3,4) and fr.school_id  >50000 and fr.enable = 0  and fr.validity_time >=NOW() )fr
LEFT JOIN (SELECT DC_SCHOOL_ID,count(distinct class_id) as class_count from  class_info  where year = '2021~2022' GROUP BY DC_SCHOOL_ID )c on fr.school_id = c.dc_school_id 
LEFT JOIN ( SELECT c.DC_SCHOOL_ID , count(DISTINCT jc.user_id ) as 'tea_count' from j_class_user jc ,class_info c  where c.year = '2021~2022' and c.class_id = jc.class_id and jc.RELATION_TYPE = '任课老师' GROUP BY c.DC_SCHOOL_ID  ) tea  on tea.DC_SCHOOL_ID = fr.school_id
LEFT JOIN ( SELECT c.DC_SCHOOL_ID , count(DISTINCT jc.user_id ) as 'stu_count' from j_class_user jc ,class_info c  where c.year = '2021~2022'and c.class_id = jc.class_id and jc.RELATION_TYPE = '学生' GROUP BY c.DC_SCHOOL_ID  ) stu on stu.DC_SCHOOL_ID = fr.school_id
LEFT JOIN (SELECT DC_SCHOOL_ID,count(distinct class_id) as axp_class_count from class_info where year = '2021~2022'  and axp_end_time >NOW()  GROUP BY DC_SCHOOL_ID) axp on axp.DC_SCHOOL_ID = fr.school_id
where class_count>0
group by fr.school_id

        '''
        school_data = MysqlDB(sql).connectdb()
        data = {
            'school_data': school_data,
            'masg': '成功'
        }
        return data


# 任务数据查询
@app.route('/task', methods=['get'])
@singOut
def task():
    if request.method == 'GET':
        # 更新时间
        update_sql = ''' 
                            SELECT c_time from updata_table where table_name = 'every_day_task'
                        '''
        update_time = SqliteDB(sql=update_sql).connectdb()

        # 任务分布
        sql_list = []
        for i in range(1, 16):
            if i == 7:
                sql_list.append(
                    ' 	SELECT sum(task_count) as  "任务总数"  from every_day_task   where task_type in (7,8,9)')

            elif i not in (5, 8, 9, 11, 12):
                sql_list.append(
                    ' 	SELECT sum(task_count) as  "任务总数"  from every_day_task   where task_type = {}'.format(i))

        reslut_list = []
        reslut_name = ['学资源', '讨论', '单题', '测验', '微课程', '一般任务', '直播课', '答题卡', '个性化', '先声']
        for i in sql_list:
            reslut_list.append(SqliteDB(i).connectdb()[0].get('任务总数'))

        task_data_list = []
        for i1, i2 in zip(reslut_name, reslut_list):
            task_data_list.append({'name': i1, 'value': i2})

        # 任务总数趋势
        task_day_sql = '''SELECT time as day,sum(task_count) as task_count from every_day_task  
                        GROUP BY time
                        '''
        axp_task_day_sql = '''SELECT time as day,sum(axp_task_count) as axp_task_count from every_day_task  
                        GROUP BY time
                        '''
        task_day = SqliteDB1(sql=task_day_sql).connectdb()
        axp_task_day = SqliteDB1(sql=axp_task_day_sql).connectdb()
        x_task_count_data = task_day['day'].tolist()
        y_task_data_list = [task_day['task_count'].tolist(), axp_task_day['axp_task_count'].tolist()]

        task_count_line = echarts_lin(x_data_list=x_task_count_data, y_name=['任务总数', '爱学派学校任务总数'],
                                      y_data_list=y_task_data_list)

        # 任务分类趋势
        task_type_sql_list = []
        for i in range(1, 16):
            if i == 7:
                task_type_sql_list.append(
                    ''' 	SELECT  a.time,b.task_count  from  (SELECT time from every_day_task  where task_type = 1 )a  LEFT JOIN  every_day_task b  
                            on a.time = b.time  and  b.TASK_TYPE  in (7,8,9)
                            ORDER BY a.time ''')

            elif i not in (5, 8, 9, 11, 12):
                task_type_sql_list.append(
                    ''' 	SELECT  a.time,b.task_count  from  (SELECT time from every_day_task  where task_type = 1 )a  LEFT JOIN  every_day_task b  
                            on a.time = b.time  and  b.TASK_TYPE  = {}
                            ORDER BY a.time'''.format(i))
        x_task_type_reslut_list = []
        y_task_type_reslut_list = []
        for i in task_type_sql_list:
            y_task_type_reslut_list.append(SqliteDB1(i).connectdb()['task_count'].tolist())
            if len(y_task_type_reslut_list) == 1:
                x_task_type_reslut_list.append(SqliteDB1(i).connectdb()['time'].tolist())

        task_type_line = echarts_lin(x_data_list=x_task_type_reslut_list[0], y_name=reslut_name,
                                     y_data_list=y_task_type_reslut_list)

        return render_template('task.html', task_data_list=task_data_list,
                               task_count_line=task_count_line.dump_options(),
                               task_type_line=task_type_line.dump_options(),
                               update_time=update_time
                               )


# 行为日志
@app.route('/useraction', methods=['get', 'post'])
@singOut
def useraction():
    if request.method == 'GET':
        return render_template('useraction.html')
    else:
        user_id = request.form.get('user_id')
        print(user_id)
        if user_id:
            es_hosts = str("52.82.47.234,52.83.95.66").split(",")
            es = Elasticsearch(es_hosts)
            body = '''{
                      "_source": ["c_time","ip","param_json","jid"],
                      "query": {
                        "bool": {
                          "must": [
                            {
                              "term": {
                                "jid": {
                                  "value": %s
                                }
                              }
                            }
                          ]
                        }
                      },"sort": [
                        {
                          "c_time": {
                            "order": "desc"
                          }
                        }
                      ],
                      "from":1,
                      "size":5000
                }''' % user_id

            res = es.search(index="two_month_action_logs", body=body)
            res = json.dumps(res)
            # with open('file/{}行为数据.txt'.format(user_id), 'a') as file:
            #     file.write(res)
            #     file.write('\n')
            # url = 'file/{}行为数据.txt'.format(user_id)
            return render_template('useraction.html', res=res)
        else:
            res = {'masg': ''}
            return render_template('useraction.html', res=res)


# ocr识别
@app.route('/imgocr', methods=['get', 'post'])
@singOut
def imgocr():
    if request.method == 'GET':
        return render_template('imgocr.html')
    else:
        file = request.files.get('img_file')
        if file:
            file_path = basedir + '\\static\\images\\' + file.filename
            # 保存图片
            file.save(file_path)

            # 图片识别
            res = imgOcr(file_path)

            # 删除图片
            # os.remove(file_path)

            # img = cv2.imread()
            # cv2.imwrite(os.path.join(basedir, 'static/images', 'test.jpg'), img)

        return render_template('imgocr.html', res=res, file_path=file_path)


# 有问题练习册路由
@app.route('/exercisePaper', methods=['get'])
@singOut
def exercisePaper():
    return render_template('exercisePaper.html')


# 练习册试卷数路由
@app.route('/exerciseCount', methods=['get'])
@singOut
def exerciseCount():
    return render_template('exerciseCount.html')


# 练习册试卷详情路由
@app.route('/exerciseList', methods=['get'])
@singOut
def exerciseList():
    return render_template('exerciseList.html')


# 练习册试卷学校使用情况路由
@app.route('/exerciseSchool', methods=['get'])
@singOut
def exerciseSchool():
    return render_template('exerciseSchool.html')


# 练习册试卷分校每添使用情况路由
@app.route('/exerciseBranchSchool', methods=['get'])
@singOut
def exerciseBranchSchool():
    return render_template('exerciseBranchSchool.html')

@app.route('/exerciseBook',methods=['get'])
def exerciseBook():
    sql = '''
    SELECT book_id,book_name  FROM `exercise_book_info`
    ORDER BY  grade_id,subject_id
    '''

    data = MysqlDB(sql).connectdb()
    book_id = []
    book_name = []

    for i in data:
        book_id.append(i['book_id'])
        book_name.append(i['book_name'])

    data = dict(zip(book_id, book_name))
    print(data)
    return  data

@app.route('/exercise', methods=['post', 'get'])
@singOut
def exercise():
    if request.method == 'POST':
        code = request.get_json()
        # print(code)
        # 练习册同步查询
        if code['code'] == '0':
            no_structure_sql = '''
            SELECT DISTINCT(ex.test_paper_id),ex.test_paper_name,ex.grade_id,subject_id,DATE_FORMAT(ex.C_TIME,'%Y-%m-%d %H:%i:%s') as c_time,DATE_FORMAT(ex.M_TIME,'%Y-%m-%d %H:%i:%s') as m_time 
            FROM oracle2utf.ex_exam_paper_ques_category exc , oracle2utf.ex_exam_paper_info ex   WHERE exc.category_score =0 AND exc.test_paper_id IN
            (SELECT paper_id FROM oracle2utf.ex_exam_paper_supplement_info) and exc.test_paper_id = ex.test_paper_id 

            '''
            no_structure_data = MysqlDB(no_structure_sql).connectdb()
            # print(paper_data)
            structure_sql = '''
            SELECT test_paper_id,test_paper_name,grade_id,subject_id,DATE_FORMAT(C_TIME,'%Y-%m-%d %H:%i:%s') as c_time,DATE_FORMAT(M_TIME,'%Y-%m-%d %H:%i:%s') as m_time FROM oracle2utf.ex_exam_paper_info WHERE ENABLE =1 AND test_paper_id IN
            (SELECT paper_id FROM oracle2utf.ex_exam_paper_supplement_info WHERE paper_id NOT IN
            (SELECT DISTINCT test_paper_id FROM oracle2utf.ex_exam_paper_ques_category)) 
            
            '''
            structure_data = MysqlDB(structure_sql).connectdb()

            data = {
                'no_structure_data': no_structure_data,
                'structure_data': structure_data
            }
            return data

        # 练习册试卷数量
        elif code['code'] == '1':

            sql = '''
            SELECT eb.grade_id,eb.subject_id ,eb.version_name ,eb.material_name,eb.book_name,count(DISTINCT p.paper_id) as paper_count
            from exercise_book_info eb,paper_info p  
            where  p.practice_book_id = eb.book_id 
            GROUP BY eb.book_id, eb.grade_id,eb.subject_id ,eb.version_name ,eb.material_name,eb.book_name
            ORDER BY eb.grade_id,eb.subject_id ,eb.version_name ,eb.material_name,book_name
             '''
            exercisecount_data = MysqlDB(sql).connectdb()

            data = {
                'exercisecount_data': exercisecount_data,
            }
            return data

        # 练习册试卷分布
        elif code['code'] == '2':
            subject_id = code['subject']
            grade_id = code['grade']
            book_id = code['book']
            print(subject_id, grade_id, book_id)

            if book_id == '0' or book_id == '':
                book_id = 'eb.book_id'
            else:
                book_id = code['book']

            sql = '''
        SELECT eb.grade_id,eb.subject_id ,eb.version_name ,eb.material_name,tc.course_name,p.paper_id,pt.test_paper_id,p.paper_name,eb.book_name ,SUM(pt.category_ques_count) as ques_count   from tp_j_course_paper tjc,tp_course_info tc,exercise_book_info eb,paper_info p  ,paper_template_info  pt 
        where tjc.course_id >0 and tjc.course_id = tc.course_id  and tjc.paper_id =p.paper_id and p.practice_book_id = eb.book_id  and p.paper_id = pt.paper_id and eb.subject_id={}   and eb.grade_id ={}  and eb.book_id = {}
        GROUP BY eb.grade_id,eb.subject_id ,eb.version_name ,eb.material_name,tc.course_name,p.paper_id
        ORDER BY eb.grade_id,eb.subject_id ,eb.version_name ,eb.material_name,tc.course_id

                     '''.format(subject_id, grade_id, book_id)
            exerciselist_data = MysqlDB(sql).connectdb()
            user_token = session.get('user_token')

            data = {
                'exerciselist_data': exerciselist_data,
                'user_token': user_token,
            }

            return data

        # 学校练习册使用情况
        elif code['code'] == '3':
            sql = '''
            SELECT fr.school_id,fr.name,os.name as belong_name ,count( DISTINCT tt.task_id ) as task_count
            from tp_task_info  tt, franchised_school_info fr ,as_answer_sheet_info aa ,oracle2utf.school_info os
            where    fr.school_id not in ( 50043,51613,50041,53741,50068,53535)  and fr.SCHOOL_ID = aa.dc_school_id 
            and tt.task_value_id = aa.paper_id  and aa.workbook_paper = 1 and os.school_id = fr.belong_school_id
            GROUP BY fr.school_id
            ORDER BY task_count desc
            '''
            exerciseschool_data = MysqlDB(sql).connectdb()

            data = {
                'exerciseschool_data': exerciseschool_data,
            }
            return data

        # 分校每天使用情况
        elif code['code'] == '4':

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

            df = [every_day, ]
            for i in school_list:
                school_sql = '''
                SELECT DATE_FORMAT(tt.c_time,'%Y-%m-%d ') as vevry_day ,count(tt.task_id) as task_count
                    from tp_task_info  tt, as_answer_sheet_info aa ,franchised_school_info fr 
                    where   tt.task_value_id = aa.paper_id   and aa.workbook_paper=1 and aa.dc_school_id  not in ( 50043,51613,50041,53741,50068,53535) and aa.DC_SCHOOL_ID = fr.school_id  and fr.belong_school_id = {}
                    GROUP BY vevry_day
            		ORDER BY vevry_day DESC
                '''.format(i)
                beschool = mysqlDB(school_sql)
                beschool.columns = ['vevry_day', '{}'.format(i)]
                df.append(beschool)

            every_count = reduce(lambda left, right: pd.merge(left, right, on=['vevry_day'], how='left'), df)
            every_count = every_count.fillna(0)

            column = ['vevry_day', 'task_count']
            for i in school['name'].tolist():
                column.append(i)
            every_count.columns = column
            every_count.loc['sum'] = every_count.iloc[:, 1:].apply(lambda x: x.sum())

            every_count_data = json.loads(every_count.to_json(orient='records', force_ascii=False))

            data = {
                'every_count_data': every_count_data,
            }
            return data

        else:
            data = {
                'code': '1',
                'masg': '失败',
            }
            return data

    if request.method == 'GET':

        school_id = request.args.get('schoolId')
        print(school_id)
        # school_id = 100002021
        sql = '''
                    SELECT  GROUP_CONCAT(a.task_id ) as task_id  from
                 (SELECT   DISTINCT(tt.task_id ) as task_id
                from tp_task_info  tt, school_info s ,as_answer_sheet_info aa
                where    s.school_id ={}  and s.SCHOOL_ID = aa.dc_school_id and tt.task_value_id = aa.paper_id  and aa.workbook_paper = 1) a
                    '''.format(school_id)
        task_data = MysqlDB(sql).connectdb()
        task_id_list = task_data[0]['task_id']

        task_sql = '''
        SELECT DISTINCT(tt.task_id ) as task_id,aa.paper_id,tt.c_user_id  ,tt.task_full_name,aa.grade_id,aa.subject_id  ,DATE_FORMAT(tt.c_time,'%Y-%m-%d %H:%i:%s') as c_time,t.teacher_name,u.ett_user_id
        from tp_task_info  tt, as_answer_sheet_info aa,teacher_info t,user_info u
        where   tt.task_value_id = aa.paper_id  and aa.workbook_paper = 1 and tt.task_id in({})
        and t.user_id = tt.c_user_id  and u.ref  = tt.C_USER_ID
        GROUP BY task_id
        ORDER BY tt.c_time desc
        '''.format(task_id_list)

        c_sql = '''

                SELECT tta.task_id ,count(DISTINCT jc.user_id ) as fm ,count(DISTINCT ttp.user_id) as fz FROM tp_task_allot_info tta, j_class_user jc,tp_task_performance ttp
                WHERE  tta.task_id in ({})
                and jc.class_id = tta.user_type_id and jc.RELATION_TYPE = '学生'  and tta.task_id = ttp.task_id
                GROUP BY tta.task_id
        '''.format(task_id_list)

        g_sql = '''
              SELECT tta.task_id ,count(DISTINCT tjg.user_id ) as fm,count(DISTINCT ttp.user_id) as fz FROM tp_task_allot_info tta, tp_j_group_student tjg,tp_task_performance ttp
                WHERE  tta.task_id in({})
                and   tta.task_id = ttp.task_id  and tta.user_type_id = tjg.group_id
                GROUP BY tta.task_id
        '''.format(task_id_list)

        stu_sql = '''
         SELECT aa.task_id , aa.fm ,bb.fz FROM (
            SELECT tta.task_id ,count(DISTINCT tjt.user_id ) as fm from tp_task_allot_info tta, tp_j_task_user tjt  WHERE  tta.task_id in ({0})
            and  tta.task_id = tjt.task_id
            GROUP BY tta.task_id )aa
            LEFT JOIN
            (SELECT ttp.task_id ,count(DISTINCT ttp.user_id) as fz  from tp_task_performance ttp  WHERE ttp.task_id in ({0})
            GROUP by  ttp.task_id
            ) bb  on aa.task_id = bb.task_id
        '''.format(task_id_list)

        pg_sql = '''
        SELECT task_id ,count(DISTINCT user_id ) as pg from as_stu_as_logs asa  where asa.task_id in ({0}) and is_marking = 1 and marking_count > 0
        GROUP BY task_id
        '''.format(task_id_list)

        df = pd.concat([mysqlDB(c_sql), mysqlDB(g_sql), mysqlDB(stu_sql)])

        task_dfs = [
            mysqlDB(task_sql),
            df,
            mysqlDB(pg_sql)]
        df_merge = reduce(lambda left, right: pd.merge(left, right, on=['task_id'], how='left'), task_dfs)
        df_merge = df_merge.fillna(0)
        school_task = json.loads(df_merge.to_json(orient='records', force_ascii=False))
        user_token = session.get('user_token')
        # print(school_task)
        data = {
            'school_task': school_task,
            'user_token': user_token
        }
        return data



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
