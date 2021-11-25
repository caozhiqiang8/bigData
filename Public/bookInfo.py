from Public.sqlDB import MysqlDB


sql = '''
SELECT book_id,book_name  FROM `exercise_book_info`
ORDER BY  grade_id,subject_id
'''

data = MysqlDB(sql).connectdb()
book_id =[]
book_name = []

for i in data:
    book_id.append(i['book_id'])
    book_name.append(i['book_name'])

data = dict(zip(book_id,book_name))

print(data)