#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
simple log

    LOG = logging.getLogger(__name__)
    LOG.debug('')
    LOG.warn()
    LOG.exception('invalid host: %s and port: %d' % ('127.0.0.1', 5000))
    LOG.error()

write to different files

    logger = logging.getlog('xxx', level=logging.DEBUG)
    logger.debug('i am debug.')
    logger.error('i am error.')
'''

import logging
import sys
import time
import random
import traceback
import threading
from logging import handlers

g_logger = None
g_charset = 'utf-8'

_DEFAULT_LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FORMAT = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'

# different log level should set different formatters
FORMAT_DICT = {
    logging.DEBUG: logging.Formatter(LOG_FORMAT),
    logging.INFO: logging.Formatter('%(asctime)s %(filename)s %(levelname)s %(message)s'),
    logging.WARN: logging.Formatter(LOG_FORMAT),
    logging.ERROR: logging.Formatter(LOG_FORMAT),
    logging.CRITICAL: logging.Formatter(LOG_FORMAT)
}

#log_dir = /var/log/arch.log
_LOGFILE_MAPPING = {
    "arch": "/var/log/arch/arch.log",
}

log_opts = {
    'debug': False, 'log_dir': '/var/log/arch/arch.log',
    'verbose': False, 'use_stderr': False,
    'log_file': '/var/log/arch/arch.log',
}

_LOGGERS = {}


def get_logid():
    log_id = 0
    try:
        log_id = threading.currentThread().__dict__['log_id']
    except:
        pass
    return log_id


def get_logger():
    logger = g_logger
    try:
        logger = threading.currentThread().__dict__['logger']
    except:
        pass
    return logger


def get_charset():
    charset = g_charset
    try:
        charset = threading.currentThread().__dict__['charset']
    except:
        pass
    return charset


def curframestr(str):
    """Return the frame object for the caller's stack frame."""

    f = sys._getframe(2)
    file = f.f_code.co_filename
    file = file.split('/')[-1]
    lineno = f.f_lineno

    log_id = get_logid()

    basic_str = "[%s:%d][log_id:%d]" % (file, lineno, log_id)
    if "basic" in threading.currentThread().__dict__:
        basic_dict = threading.currentThread().__dict__['basic']
        for key in basic_dict:
            basic_str += "[%s:%s]" % (key, basic_dict[key])

    return "%s %s" % (basic_str, str)


def callerinfo():
    return curframestr('')


def debug(str):
    charset = get_charset()
    logger = get_logger()
    if isinstance(str, unicode):
        str = str.encode(charset, 'ignore')
    str = curframestr(str)
    if logger:
        logger.debug(str)
    else:
        print str


def msg(str):
    charset = get_charset()
    logger = get_logger()
    if isinstance(str, unicode):
        str = str.encode(charset, 'ignore')
    str = curframestr(str)
    if logger:
        logger.info(str)
    else:
        print str


def warning(str):
    charset = get_charset()
    logger = get_logger()
    if isinstance(str, unicode):
        str = str.encode(charset, 'ignore')
    str = curframestr(str)
    if logger:
        logger.warning(str)
    else:
        print str


def error(str):
    logger = get_logger()
    charset = get_charset()
    if isinstance(str, unicode):
        str = str.encode(charset, 'ignore')
    str = curframestr(str)
    if logger:
        logger.error(str)
    else:
        print str


def exception(str):
    logger = get_logger()
    charset = get_charset()
    if isinstance(str, unicode):
        str = str.encode(charset, 'ignore')
    str = curframestr(str)
    str += "\n---------exception---------\n%s---------------------------\n" % (
        traceback.format_exc())
    if logger:
        logger.error(str)
    else:
        print str


def set_logid(logid):
    threading.currentThread().__dict__['log_id'] = logid


def set_basic(key, value):
    if "basic" in threading.currentThread().__dict__:
        threading.currentThread().__dict__['basic'][key] = value
    else:
        threading.currentThread().__dict__['basic'] = {}
        threading.currentThread().__dict__['basic'][key] = value


def init():
    threading.currentThread().__dict__['log_id'] = int(
        random.random() * 0xffffffff + time.time())


def start_log(path='./log/', name='default', level=logging.DEBUG,
              charset='gbk'):
    global g_logger
    global g_charset

    threading.currentThread().__dict__['log_id'] = 0
    logger = logging.getLogger(threading.currentThread().getName())
    logger.setLevel(level)

    log_file = "%s/%s.log" % (path, name)
    ch = handlers.RotatingFileHandler(log_file,
                                      maxBytes=30 * 1024 * 1024,
                                      backupCount=3)
    ch.setLevel(logging.DEBUG)
    formatter = FORMAT_DICT[level]
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    log_file = "%s/%s.log.wf" % (path, name)
    ch = handlers.RotatingFileHandler(log_file,
                                      maxBytes=30 * 1024 * 1024,
                                      backupCount=3)

    ch.setLevel(logging.WARNING)
    formatter = FORMAT_DICT[logging.WARNING]
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.info('init log success')
    if threading.currentThread().getName() == 'MainThread':
        g_logger = logger
    else:
        threading.currentThread().__dict__['logger'] = logger

    if not g_charset:
        g_charset = charset
    else:
        threading.currentThread().__dict__['charset'] = charset


class LoggerHandler(object):
    def __init__(self, logger, logname='arch.log',
                 loglevel=logging.DEBUG, stdout=False):
        '''
           指定保存日志的文件路径，日志级别，以及调用文件
           logger = Logger(logger='waeudp', logname='waeudp-logon.log',
                            loglevel=logging.DEBUG) 将日志存入到指定的文件中
        '''
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(loglevel)
        formatter = FORMAT_DICT[loglevel]

        fh = logging.FileHandler(logname)
        fh.setLevel(loglevel)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        # 如果需要调试再创建一个handler，用于输出到控制台
        if stdout:
            std = logging.StreamHandler()
            std.setLevel(loglevel)
            std.setFormatter(formatter)
            self.logger.addHandler(std)


def getlog(logger, level=logging.DEBUG, log_file='/tmp/arch.log',
           stdout=False):
    '''
    此函数根据给定参数，可以记录日志到不同文件，方便后续对日志文件处理。
    第一次调用时需要设定log_file，之后只要logger是一样的，会自动保存日志到第
    一次设定的log_file。
    使用如下：
    1） logger = getlog('arch', logging.DEBUG)
        logger.debug('i am debug.')
        logger.error('i am error.')

    2） logger = getlog('logon', logging.INFO)
        logger.debug('i am debug.')
        logger.error('i am error.')
    '''
    global _LOGGERS
    global _LOGFILE_MAPPING
    logname = _LOGFILE_MAPPING.setdefault(logger, log_file)
    if logger not in _LOGGERS:
        _LOGGERS[logger] = LoggerHandler(logger, logname, level, stdout)
    return _LOGGERS[logger].logger
