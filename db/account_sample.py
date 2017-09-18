# @Time    : 2017/9/17 下午8:45
# @Author  : Obser


import json
acc_dic = {
    'id': 1234,
    'password': 'abc',
    'credit': 15000,
    'balance': 15000,
    'enroll_date': '2016-01-02',
    'expire_date': '2021-01-01',
    'pay_day': 22,
    'status': 0 # 0 = normal, 1 = locked, 2 = disabled
}

new_acc_dic = {
    'id': 5678,
    'password': 'abc',
    'credit': 15000,
    'balance': 10000,
    'enroll_date': '2016-01-02',
    'expire_date': '2021-01-01',
    'pay_day': 22,
    'status': 0 # 0 = normal, 1 = locked, 2 = disabled
}

with open("accounts/%s.json" % new_acc_dic['id'], "w") as f:
    json.dump(new_acc_dic, f)

print(json.dumps(new_acc_dic))