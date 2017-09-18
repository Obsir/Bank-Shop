# @Time    : 2017/9/17 下午8:46
# @Author  : Obser


"""
main program handle module , handle all the user interaction stuff

"""
from core import auth
from core import accounts
from conf import settings
from core import logger
from core import accounts
from core import transaction
from core.auth import login_required
import time

# transaction logger
trans_logger = logger.logger('transaction')
# access logger
access_logger = logger.logger('access')

# temp account data ,only saves the data in memory
user_data = {
    'account_id': None,
    'is_authenticated': False,
    'account_data': None
}


@login_required
def account_info(acc_data):
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance = ''' --------- BALANCE INFO --------
            Credit :    %s
            Balance:    %s''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    return account_data['balance']


@login_required
def repay(acc_data):
    """
    print current balance and let user repay the bill
    :return:
    """
    account_data = accounts.load_current_balance(acc_data['account_id'])
    # for k,v in account_data.items():
    #    print(k,v )
    current_balance = ''' --------- BALANCE INFO --------
        Credit :    %s
        Balance:    %s''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        repay_amount = input("\033[33;1mInput repay amount:\033[0m").strip()
        if len(repay_amount) > 0 and repay_amount.isdigit():
            print('ddd 00')
            new_balance = transaction.make_transaction(trans_logger, account_data, 'repay', repay_amount)
            if new_balance:
                print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))

        else:
            print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % repay_amount)

        if repay_amount == 'b':
            back_flag = True


@login_required
def withdraw(acc_data):
    """
    print current balance and let user do the withdraw action
    :param acc_data:
    :return:
    """
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance = ''' --------- BALANCE INFO --------
        Credit :    %s
        Balance:    %s''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        withdraw_amount = input("\033[33;1mInput withdraw amount:\033[0m").strip()
        if len(withdraw_amount) > 0 and withdraw_amount.isdigit():
            new_balance = transaction.make_transaction(trans_logger, account_data, 'withdraw', withdraw_amount)
            if new_balance:
                print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))

        else:
            print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % withdraw_amount)

        if withdraw_amount == 'b':
            back_flag = True


@login_required
def transfer(acc_data):
    """
    print current balance and let user do the transfer action
    :param acc_data:
    :return:
    """
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance = ''' --------- BALANCE INFO --------
            Credit :    %s
            Balance:    %s''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        transfer_account_id = input("\033[33;1mInput transfer account:\033[0m").strip()
        if transfer_account_id == 'b':
            back_flag = True
            continue
        transfer_account_data = accounts.load_current_balance(transfer_account_id)
        if transfer_account_data:
            transfer_amount = input("\033[33;1mInput transfer amount:\033[0m").strip()
            if len(transfer_amount) > 0 and transfer_amount.isdigit():
                new_balance = transaction.make_transaction(trans_logger, account_data, 'transfer', transfer_amount)
                transfer_account_new_balance = transaction.make_transaction(trans_logger, transfer_account_data,
                                                                            'repay', transfer_amount)
                if new_balance and transfer_account_new_balance:
                    print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))
            else:
                print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % transfer_amount)

            if transfer_amount == 'b':
                back_flag = True


def pay_check(acc_data):
    log_file = "%s/log/%s" % (settings.BASE_DIR, settings.LOG_TYPES['transaction'])
    with open(log_file, "r") as f:
        for line in f:
            if 'account:%s' % acc_data['account_id'] in line:
                print("\033[32;1m%s\033[0m" % line, end='')


def logout(acc_data, mode=False):
    if not mode:
        acc_data['is_authenticated'] = False
        return True
    else:
        acc_data['is_authenticated'] = False


def interactive(acc_data):
    """
    interact with user
    :return:
    """
    menu = u'''
\033[33;1m------- Obser Bank ---------\033[0m
    \033[32;1m1.  账户信息
    2.  还款
    3.  取款
    4.  转账
    5.  账单
    6.  退出
    \033[0m'''
    menu_dic = {
        '1': account_info,
        '2': repay,
        '3': withdraw,
        '4': transfer,
        '5': pay_check,
        '6': logout,
    }
    exit_flag = False
    while not exit_flag:
        print(menu)
        user_option = input(">>:").strip()
        if user_option in menu_dic:
            print('accdata', acc_data)
            # acc_data['is_authenticated'] = False
            if menu_dic[user_option](acc_data):
                exit_flag = True

        else:
            print("\033[31;1mOption does not exist!\033[0m")


def login():
    """
    this function is used for shopping interface
    :return:
    """
    if user_data['is_authenticated']:
        return user_data
    else:
        acc_data = auth.acc_login(user_data, access_logger)
        if user_data['is_authenticated']:
            user_data['account_data'] = acc_data
            return user_data


@login_required
def pay(acc_data, amount):
    """
    api for user to pay for their shopping cart
    :return:
    """
    account_data = accounts.load_current_balance(acc_data['account_id'])
    new_balance = transaction.make_transaction(trans_logger, account_data, 'consume', amount)
    if new_balance:
        print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))
        return True
    else:
        return False


def run():
    """
    this function will be called right a way when the program started, here handles the user interaction stuff
    :return:
    """
    acc_data = auth.acc_login(user_data, access_logger)
    if user_data['is_authenticated']:
        user_data['account_data'] = acc_data
        interactive(user_data)
