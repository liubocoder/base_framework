# -*- coding: utf-8 -*-
# FileName       : base_file_serializer.py
# Create Time    : 2024/8/1 14:57:52
# Create By      : liubo
"""
base_file_serializer.py 使用说明:
    简单文件上传的序列化类
"""

import datetime
import hashlib
import os
import re

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from app.settings import logger
from rest_framework import serializers


def calculate_md5(file):
    # FIXME 这里计算MD5是将数据全部读到内存，存在问题，需要优化
    # 将文件指针定位到文件开头
    file.seek(0)
    data = file.read()
    md5_hash = hashlib.md5(data).hexdigest()
    return md5_hash


def valid_file_name(fn):
    s = str(fn).strip().replace(" ", "_")
    s = re.sub(r"(?u)[^-\[\]\w.]", "", s)
    assert s not in {"", ".", ".."}, f"{s} 无效字符串"
    return s


class BaseFileUploadSerializer(serializers.Serializer):
    """
    继承该类 用于实现文件上传功能

    上传携带的文件参数：
    fileInfo 通过表单上传的文件key

    内部参数，可以用于业务处理，使用validated_data得到：
    _fileName 上传的文件名称
    _filePath 上传文件的存放路径
    _size 上传文件大小 单位：字节
    _md5 上传文件的md5值，字符串16进制表示

    生成一个文件
    dd if=/dev/zero of=bigfile5M bs=1M count=5
    使用curl测试文件上传
    curl http://url -X POST  -F "fileInfo=@/bigfile5M" -F "objName1=d1" -F "objName2=d2" 可以指定额外的参数，用于具体业务。

    """
    fileInfo = serializers.FileField(required=False, max_length=128)

    def general_absfilepath(self, filename='file'):
        """
        获取文件存储的绝对路径，文件名称以 {时间}-{fileName} 命名
        :return: (绝对路径，带时间的文件名称)
        """
        ts = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        tFileName = f'{ts}-{filename}'
        return os.path.join(self.get_filePath(), tFileName)

    def get_maxFileSize(self):
        """
        获取允许上传的最大文件长度
        :return: 默认 settings.FILE_UPLOADER["DEF_UPLOAD_FILE_MAX_LEN"]
        """
        return settings.FILE_UPLOADER["DEF_UPLOAD_FILE_MAX_LEN"]

    def get_filePath(self):
        """
        获取文件存放路径
        :return: 默认 settings.FILE_UPLOADER["DEF_UPLOAD_FILE_DIR"]
        """
        return settings.FILE_UPLOADER["DEF_UPLOAD_FILE_DIR"]

    def get_fileInfo(self):
        """
        获取上传的文件对象，可以继承重写
        """
        return self.validated_data.get('fileInfo')

    def get_web_md5(self) -> str|None:
        """
        获取web计算的md5，默认 None不校验
        """
        return None

    def save_file(self, ignoreException=True) -> bool:
        """
        存储文件，失败的情况有
        1. 文件超过大小
        2. 文件名称不规范
        3. IO异常
        :return: True成功 False 失败
        """
        try:
            vdata = self.validated_data
            fileInfo = self.get_fileInfo()
            if fileInfo.size > self.get_maxFileSize():
                err = f"上传文件大小超过限度，文件大小[{fileInfo.size}]，最大限制[{self.get_maxFileSize()}]"
                logger.error(err)
                if ignoreException:
                    return False
                raise Exception(err)

            ufMd5 = calculate_md5(fileInfo).lower()
            if self.get_web_md5() is not None and ufMd5 != self.get_web_md5().lower():
                err = f"文件上传的md5不匹配，计算的md5[{ufMd5}]，web的md5[{self.get_web_md5().lower()}]"
                logger.error(err)
                if ignoreException:
                    return False
                raise Exception(err)

            _filepath = self.general_absfilepath(fileInfo.name)
            fss = FileSystemStorage(location=self.get_filePath())
            if fileInfo.name != valid_file_name(fileInfo.name):
                err = f"文件名称格式异常，原名称：{fileInfo.name}，合法名称：{valid_file_name(fileInfo.name)}"
                logger.error(err)
                if ignoreException:
                    return False
                raise Exception(err)

            fss.save(_filepath, fileInfo)
            vdata['_filePath'] = _filepath
            vdata['_fileName'] = fileInfo.name
            vdata['_md5'] = ufMd5
            vdata['_size'] = fileInfo.size
            return True
        except Exception as e:
            logger.error(f"文件存储失败，异常为：{e}")

        if ignoreException:
            return False
        raise Exception("文件存储失败")

    class Meta:
        fields = "__all__"
