# coding=utf-8

import requests


ss = requests.Session()
lunch_info = {}
dish_list = []
user_info = {}


def login():
    global user_info
    payload = {'user_name': '2017207', 'passwd': '2017207'}
    login_request = ss.post('http://dc.dianchu.cc:8013/api/frontend/login', data=payload)
    info = login_request.json()['user_info']
    user_info = {'user_id': info['id'], 'user_name': info['employee_name'], 'floor': info['position']}
    # print(user_info)


def get_lunch_list():
    global user_info, lunch_info
    payload = {"cmd": 1, "floor": user_info['floor'], "select_type": 8}  # 选择抢购
    lunch_request = ss.post('http://dc.dianchu.cc:8013/api/frontend/select_order', json=payload)
    lunch_info = {'select_id': lunch_request.json()['select_data'][0]['select_id'],
                  'busi_id': lunch_request.json()['select_data'][0]['business_info'][0]['busi_id'],
                  'busi_name': lunch_request.json()['select_data'][0]['business_info'][0]['busi_name']}
    # print(lunch_info)


def get_dish_list():
    global dish_list, lunch_info
    payload = {"cmd": 2, "busi_id": lunch_info['busi_id'], "select_id":  lunch_info['select_id']}
    dish_request = ss.post('http://dc.dianchu.cc:8013/api/frontend/select_order', json=payload)
    dish_list.extend(dish_request.json()['menu_data'])
    # print(dish_list)


def order():
    global lunch_info, dish_list, user_info
    payload = {'floor': user_info['floor'], 'order_menu': [], 'select_id': lunch_info['select_id'], 'user_id': user_info['user_id']}
    dish = {}
    for i in dish_list:
        if not dish.get('actual_price'):
            dish = i
        elif i['actual_price'] > dish['actual_price']:
            dish = i
    payload['order_menu'].append({'busi_id': lunch_info['busi_id'], 'busi_name': lunch_info['busi_name'], 'menu': [dish]})

    print('即将预定：', lunch_info['busi_name'], dish['menu_name'], dish['actual_price'])
    user_check = input('是否预定（[y]/n）？')
    if user_check != 'n':
        order_request = ss.post('http://dc.dianchu.cc:8013/api/frontend/order', json=payload)
        print('ordering……', order_request.json()['message'])
    else:
        print('已取消预定～')


if __name__ == '__main__':
    login()
    get_lunch_list()
    get_dish_list()
    order()


