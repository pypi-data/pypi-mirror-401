import os.path
import struct
import time
from typing import Optional, List


class FileUtil:
    type_dict = {
        # '424D': 'bmp',
        'FFD8FF': 'jpg',
        # '2E524D46': 'rm',
        # '4D546864': 'mid',
        '89504E47': 'png',
        '47494638': 'gif',
        '49492A00': 'tif',
        # '41433130': 'dwg',
        # '38425053': 'psd',
        # '2142444E': 'pst',
        # 'FF575043': 'wpd',
        # 'AC9EBD8F': 'qdf',
        # 'E3828596': 'pwl',
        '504B0304': 'zip',
        '52617221': 'rar',
        '57415645': 'wav',
        '41564920': 'avi',
        '2E7261FD': 'ram',
        '000001BA': 'mpg',
        '000001B3': 'mpg',
        '6D6F6F76': 'mov',
        # '7B5C727466': 'rtf',
        '3C3F786D6C': 'xml',
        '68746D6C3E': 'html',
        'D0CF11E0': 'doc/xls',
        '255044462D312E': 'pdf',
        'CFAD12FEC5FD746F': 'dbx',
        # '3026B2758E66CF11': 'asf',
        '5374616E64617264204A': 'mdb',
        # '252150532D41646F6265': 'ps/eps',
        # '44656C69766572792D646174653A': 'eml'
    }
    file_type = {
        "image": ["jpg", "png", "gif", "tif"],
        "document": ["zip", "rar", "wav", "xml", "html", "doc", "xls", "pdf", "dbx", "mdb"],
        "voice": ["mp3", "amr"],
        "video": ["wav", "avi", "ram", "mpg", "mov", "mp4"],
    }

    @staticmethod
    def get_sub_file_names(file_num: int, base_dir: Optional[str] = "./temp", dir_name: Optional[str] = None, file_name: Optional[str] = None) -> List[str]:
        """
        功能用于多个文件打包在压缩包中下载
        在指定或时间戳文件夹下，根据文件数量生成对应文件名
        :param base_dir: 基础路径
        :param file_num: 子文件数量
        :param dir_name: 文件夹名称，可以忽略
        :param file_name: 文件夹名称，建议填写，方便区分
        :return: 文件名列表
        """
        if not base_dir:
            base_dir = "./temp"
        if not dir_name:
            dir_name = str(int(time.time()*1000))
        dir_path = os.path.join(base_dir, dir_name)
        if os.path.exists(dir_path):
            dir_path = os.path.join(base_dir, str(int(time.time()*1000)))
        os.makedirs(dir_path, exist_ok=True)
        file_name_list = []
        for i in range(1, file_num+1):
            file_name_list.append(os.path.join(dir_path, (file_name or "") +"_"+str(i)))
        return file_name_list

    @classmethod
    def get_max_len(cls):
        """动态计算 type_dict 中键的最大长度（字节数）"""
        if not cls.type_dict:  # 处理空字典的边界情况
            return 0
        # 先找键中长度最长的那个，再计算长度并除以2（转字节数）
        max_key = max(cls.type_dict.keys(), key=len)
        return len(max_key) // 2

    @classmethod
    async def get_filetype(cls, file):
        # 读取二进制文件开头一定的长度
        if isinstance(file, str):
            filename = file
            with open(filename, 'rb') as f:
                byte = f.read(cls.get_max_len())
        else:
            filename = file.filename
            byte = await file.read(cls.get_max_len())
            await file.seek(0)
        # 解析为元组
        byte_list = struct.unpack('B' * cls.get_max_len(), byte)
        # 转为16进制
        code = ''.join([('%X' % each).zfill(2) for each in byte_list])
        # 根据标识符筛选判断文件格式
        result = list(filter(lambda x: code.startswith(x), cls.type_dict))
        nametype = filename.split('.')[-1]
        if result:
            filetype = cls.type_dict[result[0]]
            if filetype == "zip":
                filetype = nametype if nametype in ['xlsx', 'docx'] else "zip"
            elif filetype == "doc/xls":
                filetype = nametype if nametype in ['doc', 'xls'] else None
            elif filetype == "jpg":
                filetype = nametype if nametype in ['jpg', 'jpeg'] else None
            else:
                filetype = filetype if filetype == nametype else None
        else:
            filetype = nametype if nametype in ['mp3', 'mp4', 'txt'] else None
        return filetype
