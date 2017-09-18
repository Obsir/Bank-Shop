# @Time    : 2017/9/18 上午12:13
# @Author  : Obser


import pickle
from core import main
from conf import settings

conn_params = settings.DATABASE
db_path = '%s/%s' % (conn_params['path'], conn_params['shop'])
shop_list_file = "%s/%s.data" % (db_path, 'shop_list')
user_info_file = "%s/%s.data" % (db_path, 'user_info')


def load_list():
    file = open(shop_list_file, 'rb')
    try:
        stored_list = pickle.load(file)
        file.close()
        # for index, item in enumerate(shop_list_file):
        #     print("商品信息列表如下".center(40, '-'))
        #     print(index, item)
        return stored_list
    except:
        file.close()
        print("商品信息列表为空".center(40, '-'))
        stored_list = []
        return stored_list


def load_info():
    file = open(user_info_file, 'rb')
    try:
        stored_info = pickle.load(file)
        file.close()
        return stored_info
    except:
        file.close()
        stored_info = {'cart': {}}
        return stored_info


def interactive():
    exit_flag = False

    def logout():
        return True

    menu = u'''
\033[33;1m------- Obser Shop ---------\033[0m
        \033[32;1m1.  购物
        2.  结算
        3.  退出
        \033[0m'''

    menu_dic = {
        '1': buy,
        '2': cart,
        '3': logout,
    }

    while not exit_flag:
        print(menu)
        user_option = input(">>:").strip()
        if user_option in menu_dic:
            if menu_dic[user_option]():
                exit_flag = True
        else:
            print("\033[31;1mOption does not exist!\033[0m")


def pay(*args):
    """
    api of atm for user to pay for their shopping cart
    :return:
    """
    amount = args[0]
    if int(amount) == 0:
        print("\033[31;1m请先添加商品！\033[0m")
        return
    shopping_list = args[1]
    acc_data = main.login()
    result = main.pay(acc_data, amount)
    main.logout(acc_data, mode=True)
    if result:
        shopping_list.clear()
        dump_shopping_list(shopping_list)


def sort(*args):
    """
    this function is called when user want to clear up their shopping cart
    :return:
    """
    shopping_list = args[1]
    product_list = args[2]
    print("\033[32;1m购物车列表\033[0m".center(40, '-'))
    print_cart(shopping_list, product_list)
    back_flag = False

    def clear():
        back_flag = False
        print("\033[31;1m确认要清空购物车吗? y/n\033[0m")
        while not back_flag:
            user_info = load_info()
            product_list = load_list()
            shopping_list = dict(user_info['cart'])
            user_option = input(">>:").strip()
            if user_option == 'y':
                shopping_list.clear()
                print("\033[32;1m购物车列表\033[0m".center(40, '-'))
                print_cart(shopping_list, product_list)
                dump_shopping_list(shopping_list)
                back_flag = True
            elif user_option == 'n':
                print("\033[32;1m购物车列表\033[0m".center(40, '-'))
                print_cart(shopping_list, product_list)
                back_flag = True
            else:
                print("\033[31;1mOption does not exist!\033[0m")

    def modify():
        back_flag = False
        print("\033[33;1m请输入要修改的商品序号:\033[0m")
        while not back_flag:
            user_info = load_info()
            product_list = load_list()
            shopping_list = dict(user_info['cart'])
            index = input(">>:").strip()
            if index.isdigit() and int(index) in shopping_list:
                index = int(index)
                while not back_flag:
                    print("\033[33;1m请输入要修改的商品数量:\033[0m")
                    count = input(">>:").strip()
                    if count.isdigit() and 0 <= int(count):
                        shopping_list[index] = int(count)
                        dump_shopping_list(shopping_list)
                        print_cart(shopping_list, product_list)
                        back_flag = True
                    elif count == 'b':
                        back_flag = True
                    else:
                        print("\033[31;1mOption does not exist!\033[0m")
            elif index == 'b':
                print("\033[32;1m购物车列表\033[0m".center(40, '-'))
                print_cart(shopping_list, product_list)
                back_flag = True
            else:
                print("\033[31;1mOption does not exist!\033[0m")

    menu = u'''
\033[33;1m------- 整理购物车 ---------\033[0m
        \033[32;1m1.  修改
        2.  清空
        \033[0m'''
    menu_dic = {
        '1': modify,
        '2': clear
    }
    while not back_flag:
        print(menu)
        user_option = input(">>:").strip()
        if user_option in menu_dic:
            menu_dic[user_option]()
        elif user_option == 'b':
            back_flag = True
        else:
            print("\033[31;1mOption does not exist!\033[0m")


def cart():
    """
    this function is called when user want to check their shopping cart
    :return:
    """
    back_flag = False
    user_info = load_info()
    product_list = load_list()
    shopping_list = dict(user_info['cart'])
    sum = 0
    menu = u'''
\033[33;1m------- 购物车 ---------\033[0m
    \033[32;1m1.  整理
    2.  支付
    \033[0m'''
    menu_dic = {
        '1': sort,
        '2': pay
    }
    print("\033[32;1m购物车列表\033[0m".center(40, '-'))
    if len(shopping_list) == 0:
        print("当前购物车为空")
    else:
        sum = print_cart(shopping_list, product_list)
    while not back_flag:
        print(menu)
        user_option = input(">>:").strip()
        if user_option in menu_dic:
            menu_dic[user_option](sum, shopping_list, product_list)
        elif user_option == 'b':
            back_flag = True
        else:
            print("\033[31;1mOption does not exist!\033[0m")




# def sort_cart(shopping_list):
#     set_list = set(sorted(shopping_list, key=lambda x: int(x[1])))
#
#     for item in set_list:
#
#
#     return sorted_list
def print_cart(shopping_list, product_list):
    """
    this function is for developer to print the user's shopping cart
    :param shopping_list:
    :param product_list:
    :return:
    """
    sum = 0
    for p in shopping_list:
        print("\033[32;1m序号: %s\033[0m" % p, end='\t\t')
        print("\033[32;1m名称: %s\033[0m" % product_list[p][0], end='\t\t')
        print("\033[32;1m价格: %s\033[0m" % product_list[p][1], end='\t\t')
        print("\033[32;1m数量: %s\033[0m" % shopping_list[p])
        sum += int(shopping_list[p]) * int(product_list[p][1])
    print("\033[32;1m合计: %s\033[0m" % sum)
    return sum


def buy():
    """
    add product to user's shopping cart
    :param:
    :return:
    """
    back_flag = False

    user_info = load_info()
    product_list = load_list()
    shopping_list = dict(user_info['cart'])
    print("\033[32;1m购物车列表\033[0m".center(40, '-'))
    if len(shopping_list) == 0:
        print("当前购物车为空")
    else:
        print_cart(shopping_list, product_list)
    # print("\033[33;1m您当前余额为:%s\033[0m" % balance)
    while not back_flag:
        print("\033[34;1m商品信息列表如下\033[0m".center(40, '-'))
        for index, item in enumerate(product_list):
            print("\033[34;1m序号: %s\033[0m" % index, end='\t\t')
            print("\033[34;1m名称: %s\033[0m" % item[0], end='\t\t')
            print("\033[34;1m价格: %s\033[0m" % item[1])
        user_choice = input("\033[33;1m请输入您要购买的商品序号:\033[0m")
        if user_choice.isdigit():
            user_choice = int(user_choice)
            if 0 <= user_choice < len(product_list):
                p_item = product_list[user_choice]
                if user_choice not in shopping_list:
                    shopping_list[user_choice] = 1
                else:
                    shopping_list[user_choice] += 1
                print("\033[34;1m%s 已被加入您的购物车\033[0m" % p_item)
            else:
                print("\033[31;1m商品序号 [%s] 不存在!\033[0m" % user_choice)
        elif user_choice == 'b':
            print("\033[32;1m购物车列表\033[0m".center(40, '-'))
            # sorted_cart = sort_cart(shopping_list)
            print_cart(shopping_list, product_list)
            user_info['cart'] = shopping_list

            dump_user_info(user_info)
            # f = open(user_info_file, 'wb')
            # pickle.dump(user_info, f)
            # f.close()
            back_flag = True
        else:
            print("\033[31;1m非法选项\033[0m")


def dump_shopping_list(shopping_list):
    user_info = load_info()
    user_info['cart'] = shopping_list
    with open(user_info_file, 'wb') as f:
        pickle.dump(user_info, f)


def dump_user_info(user_info):
    with open(user_info_file, 'wb') as f:
        pickle.dump(user_info, f)


def run():
    """
    this function will be called right a way when user choose to shop
    :return:
    """
    interactive()
