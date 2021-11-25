import pandas as pd

rank_score_excel = pd.read_excel('C:\\Users\\caozhiqiang\\Desktop\\考试数据分析\\北京四中数据\\20-21第二学期一模考试\\整理数据\\等级赋分\\等级赋分表.xlsx')

stu_exam = pd.read_excel('C:\\Users\\caozhiqiang\\Desktop\\考试数据分析\\北京四中数据\\20-21第二学期一模考试\\整理数据\\等级赋分\\四中一模成绩单.xlsx')
stu_exam = stu_exam.fillna(0)

def rank_score(score,rank_score):

    if score >= rank_score[0]:

        return 100
    elif score >= rank_score[1] and score<rank_score[0]:
        return 97
    elif score >= rank_score[2] and score<rank_score[1]:
        return 94
    elif score >= rank_score[3] and score<rank_score[2]:
        return 91
    elif score >= rank_score[4] and score<rank_score[3]:
        return 88
    elif score >= rank_score[5] and score<rank_score[4]:
        return 85
    elif score >= rank_score[6] and score<rank_score[5]:
        return 82
    elif score >= rank_score[7] and score<rank_score[6]:
        return 79
    elif score >= rank_score[8] and score<rank_score[7]:
        return 76
    elif score >= rank_score[9] and score<rank_score[8]:
        return 73
    elif score >= rank_score[10] and score<rank_score[9]:
        return 70
    elif score >= rank_score[11] and score<rank_score[10]:
        return 67
    elif score >= rank_score[12] and score<rank_score[11]:
        return 64
    elif score >= rank_score[13] and score<rank_score[12]:
        return 61
    elif score >= rank_score[14] and score<rank_score[13]:
        return 58
    elif score >= rank_score[15] and score<rank_score[14]:
        return 55
    elif score >= rank_score[16] and score<rank_score[15]:
        return 52
    elif score >= rank_score[17] and score<rank_score[16]:
        return 49
    elif score >= rank_score[18] and score<rank_score[17]:
        return 46
    elif score >= rank_score[19] and score<rank_score[18]:
        return 43
    elif score >= rank_score[20] and score<rank_score[19]:
        return 40

wl_rank_score = rank_score_excel['物理'].to_list()
hx_rank_score = rank_score_excel['化学'].to_list()
ls_rank_score = rank_score_excel['历史'].to_list()
sw_rank_score = rank_score_excel['生物'].to_list()
dl_rank_score = rank_score_excel['地理'].to_list()
zz_rank_score = rank_score_excel['政治'].to_list()


stu_exam['物赋分'] = stu_exam['物理'].apply(lambda x: rank_score(x,rank_score=wl_rank_score) )
stu_exam['化赋分'] = stu_exam['化学'].apply(lambda x: rank_score(x,rank_score=hx_rank_score) )
stu_exam['政赋分'] = stu_exam['政治'].apply(lambda x: rank_score(x,rank_score=zz_rank_score) )
stu_exam['历赋分'] = stu_exam['历史'].apply(lambda x: rank_score(x,rank_score=ls_rank_score) )
stu_exam['生赋分'] = stu_exam['生物'].apply(lambda x: rank_score(x,rank_score=sw_rank_score) )
stu_exam['地赋分'] = stu_exam['地理'].apply(lambda x: rank_score(x,rank_score=dl_rank_score) )

stu_exam.to_excel('C:\\Users\\caozhiqiang\\Downloads\\赋分后数据.xls')
