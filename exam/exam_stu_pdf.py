import requests

#  十五中考试    高一：3153806314730   高二：3183950500193
#  理工附  初三二模：32737289539

examId = 32737289539

# 导出项配置  字符串拼接逗号分隔 1学生成绩单 2学生色块分析 3学生试题分析
exportType = '1,2,3'

# 十五中考试     高一班级：%s%%E7%%8F%%AD     高二班级：%s%%E7%%8F%%AD
#  理工附  初三二模： %%E4%%B9%%9D0%s%%E7%%8F%%AD
className = '%%E4%%B9%%9D0%s%%E7%%8F%%AD'

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXRhaWwiOnsidXNlcklkIjoyOTUxNjM1LCJ1c2VyTmFtZSI6IuWkp-i_nua1i-ivlTAwMSIsInBhc3N3b3JkIjoiIiwidXNlcklkZW50aXR5IjoxLCJlbmFibGUiOjEsInNjaG9vbFVzZXJJZCI6MzY3Njg2LCJzY2hvb2xJZCI6NTAwNDMsInNjaG9vbFVzZXJSZWYiOiJmYzI4Y2IwYi1lMDRmLTQ0ODUtOTQ4Yi02M2Q0NTU2ZmNlNGEiLCJzY2hvb2xHcm91cElkIjo3LCJyb2xlcyI6WzE2LDE3LDIsMjEsNiw5LDEzLDE1XSwidXJsTGlzdCI6bnVsbH0sImV4cCI6MTYyMTQyNTc0MywidXNlcl9uYW1lIjoi5aSn6L-e5rWL6K-VMDAxIiwianRpIjoiNjcyMWUyZWItNzZjOC00ZGExLWE0MGQtOGQ3ZDI5MmQwN2JhIiwiY2xpZW50X2lkIjoiRkE5RTIxNUJFNTY2RUU5MjYxNEZCQzExQUJFREY5NjgiLCJzY29wZSI6WyJhbGwiLCJ3ZWIiLCJtb2JpbGUiXX0.k9r8bjcvw6LAg3KXzNGRDNHCbkAnb5F8Ia-Dbl60MK8'

url = "https://school-file.etiantian.com/fileSystem/exam-analysis/classes/stu-analysis/V2?examId={examId}&classType=1&exportType={exportType}&className={className}&token={token}".format(
    examId=examId, exportType=exportType, className=className, token=token)
file_name = "北京理工大学附属中学2020~2021下学期初三二模考试——%s班学生分析简报.zip"
for i in range(1, 11):
    correct_url = url % str(i)
    correct_file_name = file_name % str(i).zfill(2)
    r = requests.get(correct_url, stream=True)
    with open(correct_file_name, "wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                pdf.write(chunk)
    print('{}班下载完成'.format(i))
print('下载完成')