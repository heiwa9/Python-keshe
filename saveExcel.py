from openpyxl import Workbook


def save_to_excel(mongoDB_data):
    outwb = Workbook()
    outws = outwb.worksheets[0]
    # 遍历外层列表
    for new_dict in mongoDB_data:
        a_list = []
        # 遍历内层每一个字典dict，把dict每一个值存入list
        for item in new_dict.values():
            a_list.append(item)
        # sheet直接append list即可
        outws.append(a_list)
 	# excel地址
    outwb.save(r'temp_hum.xlsx')
    print('数据存入excel成功')