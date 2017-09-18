# @Time    : 2017/9/17 下午8:30
# @Author  : Obser


import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core import main
from core import shopping
if __name__ == '__main__':
    menu = u'''
\033[33;1m------- Obser Union ---------\033[0m
        \033[32;1m1.  ATM
        2.  购物
        3.  退出
        \033[0m'''
    menu_dic = {
        '1': main.run,
        '2': shopping.run,
        '3': exit,
    }
    exit_flag = False
    while not exit_flag:
        print(menu)
        user_option = input(">>:").strip()
        if user_option in menu_dic:
            menu_dic[user_option]()
        else:
            print("\033[31;1mOption does not exist!\033[0m")
