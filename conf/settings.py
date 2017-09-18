# @Time    : 2017/9/17 下午8:44
# @Author  : Obser

import os
import sys
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE = {
    'engine': 'file_storage',  # support mysql,postgresql in the future
    'name': 'accounts',
    'shop': 'shop',
    'path': "%s/db" % BASE_DIR
}

LOG_LEVEL = logging.INFO
LOG_TYPES = {
    'transaction': 'transactions.log',
    'access': 'access.log',
}

TRANSACTION_TYPE = {
    'repay': {'action': 'plus', 'interest': 0},
    'withdraw': {'action': 'minus', 'interest': 0.05},
    'transfer': {'action': 'minus', 'interest': 0.05},
    'consume': {'action': 'minus', 'interest': 0},

}
