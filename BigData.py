import json
import os
from flask import Flask, render_template, request, redirect, jsonify, make_response
from elasticsearch import Elasticsearch
import settings
from Public.ocr import imgOcr
from Public.sqlDB import MysqlDB, SqliteDB, SqliteDB1, mysqlDB
from Public.echarts import echarts_bar, echarts_lin

Config = settings.Config
app = Flask(__name__)
app.config.from_object(Config)

basedir = os.path.abspath(os.path.dirname(__file__))


# 登录
@app.route("/")
@app.route("/login", methods=['get', 'post'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        data = request.get_json()
        if data['user_name'] == 'admin' and data['password'] == '1111':
            return {
                'code': '1'
            }
        else:
            return {
                'code': '0'
            }


# index学校地图
@app.route('/index', methods=['get'])
def index():

    return render_template('index.html')


# index学校地图
@app.route('/mapdata', methods=['get'])
def mapdata():
    sql = '''
    SELECT s.province as 'name',count(DISTINCT fr.SCHOOL_ID) as 'value'  from franchised_school_info fr,school_info s where fr.school_type in (3,4)   
    and fr.school_id  >50000 and fr.enable = 0  and s.school_id = fr.school_id 
    GROUP BY s.province
            '''
    school_list = MysqlDB(sql).connectdb()

    # print(school_list)


    return {
        'map':school_list
    }


# 用户查询
@app.route('/user', methods=['get', 'post'])
def user():
    if request.method == 'GET':
        return render_template('user.html')
    if request.method == 'POST':
        user_tea_name = request.form.get('user_tea_name')
        user_tea_id = request.form.get('user_tea_id')
        user_stu_name = request.form.get('user_stu_name')
        user_stu_id = request.form.get('user_stu_id')

        if user_tea_name:
            sql = ('''SELECT s.name,s.school_id ,u.ETT_USER_ID,oc.user_name , oc.password,t.TEACHER_NAME ,u.state_id, c.CLASS_ID,c.CLASS_GRADE,c.CLASS_NAME,c.PATTERN,sb.SUBJECT_NAME,jc.C_TIME
                from  oracle2utf.coschuser_info oc,user_info u,school_info s,teacher_info t ,j_class_user jc ,class_info c,subject_info sb
                where  oc.jid = u.ETT_USER_ID and u.DC_SCHOOL_ID = s.school_id and u.ref = t.user_id  and u.ref = jc.user_id  and jc.CLASS_ID = c.CLASS_ID and c.`YEAR` = '2020~2021' and jc.SUBJECT_ID = sb.SUBJECT_ID
                and oc.user_name ='{}'
                GROUP BY s.school_id ,u.ETT_USER_ID,c.CLASS_GRADE,c.CLASS_NAME,sb.SUBJECT_NAME
                '''.format(user_tea_name))
            data = MysqlDB(sql)
            tea_data = data.connectdb()
            # tea_data = tea_data.to_dict('records')

            return render_template('user.html', tea_data=tea_data)

        if user_tea_id:
            sql = ('''SELECT s.name,s.school_id ,u.ETT_USER_ID,oc.user_name , oc.password,t.TEACHER_NAME ,u.state_id, c.CLASS_ID,c.CLASS_GRADE,c.CLASS_NAME,c.PATTERN,sb.SUBJECT_NAME,jc.C_TIME
            from  oracle2utf.coschuser_info oc,user_info u,school_info s,teacher_info t ,j_class_user jc ,class_info c,subject_info sb
            where  oc.jid = u.ETT_USER_ID and u.DC_SCHOOL_ID = s.school_id and u.ref = t.user_id  and u.ref = jc.user_id  and jc.CLASS_ID = c.CLASS_ID and c.`YEAR` = '2020~2021' and jc.SUBJECT_ID = sb.SUBJECT_ID
            and oc.jid = {}
            GROUP BY s.school_id ,u.ETT_USER_ID,c.CLASS_GRADE,c.CLASS_NAME,sb.SUBJECT_NAME
            '''.format(user_tea_id))
            data = MysqlDB(sql)
            tea_data = data.connectdb()
            # tea_data = tea_data.to_dict('records')

            return render_template('user.html', tea_data=tea_data)

        if user_stu_name:
            sql = ('''SELECT s.name,s.school_id ,u.ETT_USER_ID,oc.user_name , oc.password,t.STU_NAME ,u.state_id, c.CLASS_ID,c.CLASS_GRADE,c.CLASS_NAME,jc.C_TIME
                    from  oracle2utf.user_info oc,user_info u,school_info s,student_info t ,j_class_user jc ,class_info c
                    where  oc.user_id = u.ETT_USER_ID and u.DC_SCHOOL_ID = s.school_id and u.ref = t.user_id  and u.ref = jc.user_id  and jc.CLASS_ID = c.CLASS_ID and c.`YEAR` = '2020~2021'
                    and oc.user_name ='{}'
                  '''.format(user_stu_name))
            data = MysqlDB(sql)
            stu_data = data.connectdb()
            # stu_data = stu_data.to_dict('records')
            return render_template('user.html', stu_data=stu_data)

        if user_stu_id:
            sql = ('''    SELECT s.name,s.school_id ,u.ETT_USER_ID,oc.user_name , oc.password,t.STU_NAME ,u.state_id, c.CLASS_ID,c.CLASS_GRADE,c.CLASS_NAME,jc.C_TIME
                        from  oracle2utf.user_info oc,user_info u,school_info s,student_info t ,j_class_user jc ,class_info c
                        where  oc.user_id = u.ETT_USER_ID and u.DC_SCHOOL_ID = s.school_id and u.ref = t.user_id  and u.ref = jc.user_id  and jc.CLASS_ID = c.CLASS_ID and c.`YEAR` = '2020~2021'
                        and oc.user_id = {}
                  '''.format(user_stu_id))
            data = MysqlDB(sql)
            stu_data = data.connectdb()
            # stu_data = stu_data.to_dict('records')

            return render_template('user.html', stu_data=stu_data)


# 资源查询
@app.route('/resource', methods=['get'])
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

# 智能组卷数据查询
@app.route('/paper',methods=['get'])
def paper():
    if request.method == 'GET':
        sql = '''
              select grade_name,subject_name,wisdom_exam,paper_name,c_time,teacher_name,school_id,name from paper_online_info 
	        ORDER BY school_id
        '''
        paper_data = SqliteDB(sql = sql ).connectdb()

        # 更新时间
        update_sql = ''' 
                            SELECT c_time from updata_table where table_name = 'paper_online_info'
                        '''
        update_time = SqliteDB(sql=update_sql).connectdb()

        return  render_template('paper.html',paper_data = paper_data, update_time=update_time)

# 学校数据查询
@app.route('/school', methods=['get'])
def school():
    if request.method == 'GET':
        sql = '''
                select * from school_class_user  order by axp_class_count desc 
                '''
        school_teacher_task = SqliteDB(sql=sql).connectdb()
        # print(school_teacher_task)


        # 更新时间
        update_sql = ''' 
                            SELECT c_time from updata_table where table_name = 'school_class_user'
                        '''
        update_time = SqliteDB(sql=update_sql).connectdb()

        return render_template('school.html', school_teacher_task=school_teacher_task, update_time=update_time)


# 任务数据查询
@app.route('/task', methods=['get'])
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
def useraction():
    if request.method == 'GET':
        return render_template('useraction.html')
    else:
        user_id = request.form.get('user_id')
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
                      "size":10000
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


# vue 示例
@app.route('/login_vue')
def login_vue():
    return render_template('login_vue.html')


@app.route('/login_vue_json', methods=['get', 'post'])
def login_vue_json():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        return '陈功'
    else:
        return {'grade_data':
            {'1': {
                'grade_name': '高三年级',
                'subject_name': '语文',
                'word_count': 389,
                'word_mp4_count': 89.0,
                'mp4_count': 89,
                'mp4_word_count': 89.0,
                'cpaper_count': 212.0,
                'paper_count': 68.0,
                'question_count': 21084.0
            }, '2': {
                'grade_name': '高三年级',
                'subject_name': '数学',
                'word_count': 757,
                'word_mp4_count': 135.0,
                'mp4_count': 176,
                'mp4_word_count': 161.0,
                'cpaper_count': 129.0,
                'paper_count': 2349.0,
                'question_count': 40611.0
            }},
            'bar_data': {
                'x_data':["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"],
                'y_data':[5, 20, 36, 10, 10, 20],
                'bar_name':'这是图名字'

            }}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
