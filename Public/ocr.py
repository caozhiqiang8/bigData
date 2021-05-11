import requests
import base64

def imgOcr(img_path):

    # 获取access_token： client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=omveihBTuNPdIsU332DbEIsM&client_secret=8M6KFi85pHFsRbaD1slRUDcFD5vWEWr8'
    response = requests.get(host).json()
    access_token = response['access_token']

    #ocr调取地址
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/doc_analysis"

    # 二进制方式打开图片文件
    f = open(img_path, 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img, "language_type": "CHN_ENG", "result_type": "big"}
    access_token = '{}'.format(access_token)
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        response = response.json()
        words_list = []
        for i in range(response['results_num']):
            response_word = response['results'][i]['words']['word']
            words_list.append(response_word)
        return words_list

    else:
        return '调取失败'


if __name__ == '__main__':

    print(imgOcr('C:/Users/caozhiqiang/Desktop/2.png'))

