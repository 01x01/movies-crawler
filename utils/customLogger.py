#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
"""
自定义日志格式
"""
import logging,os
 

class CustomLog(object):
    def __init__(self, name, outfile=os.path.join("log","default.log"), errfile=None, level="INFO"):
        super(CustomLog, self).__init__()
        self.name = name
        self.level = level
        if not os.path.exists('log'):
            os.mkdir('log')
 
        # 控制台输出样式（无色）
        self.formatter = logging.Formatter(
            fmt='[%(asctime)s] %(levelname)-8s | %(msg)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
 
        # 保存到文件格式
        self.file_formatter = logging.Formatter(
            fmt='[%(asctime)s] %(levelname)-8s | %(msg)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
 
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.level)
 
        # 如果已有handler则不再处理
        # 修复重复输出的bug
        if self.logger.handlers:
            return
 
        sh = logging.StreamHandler()
        sh.setLevel(self.level)
        sh.setFormatter(self.formatter)
 
        self.logger.addHandler(sh)
 
        if outfile:
            fh = logging.FileHandler(outfile)
            fh.setLevel(self.level)
            fh.setFormatter(self.file_formatter)
            self.logger.addHandler(fh)
 
        if errfile:
            efh = logging.FileHandler(errfile)
            efh.setLevel(logging.ERROR)
            efh.setFormatter(self.file_formatter)
            self.logger.addHandler(efh)
 
 
    def getLogger(self):
        return self.logger

 
 