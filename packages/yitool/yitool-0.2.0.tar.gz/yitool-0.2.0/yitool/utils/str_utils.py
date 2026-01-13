import yitool.utils._humps as _humps


class StrUtils:
    """字符串工具类"""

    @staticmethod
    def is_empty(s: str) -> bool:
        """判断字符串是否为空"""
        return s is None or s.strip() == ""

    @staticmethod
    def is_not_empty(s: str) -> bool:
        """判断字符串是否非空"""
        return not StrUtils.is_empty(s)

    @staticmethod
    def safe(s: str) -> str:
        """安全获取字符串，避免 None，返回空字符串"""
        return s if s is not None else ""

    # @cached(cache={}, key=lambda str_or_iter: str_or_iter)
    @staticmethod
    def camel_ize(str_or_iter: str) -> str:
        """将字符串或可迭代对象转换为驼峰命名法"""
        return _humps.camelize(str_or_iter)

    @staticmethod
    def de_camelize(str_or_iter: str) -> str:
        """将字符串或可迭代对象转换为蛇形命名法"""
        return _humps.decamelize(str_or_iter)

    @staticmethod
    def pascal_ize(str_or_iter: str) -> str:
        """将字符串或可迭代对象转换为帕斯卡命名法"""
        return _humps.pascalize(str_or_iter)

    @staticmethod
    def kebab_ize(str_or_iter: str) -> str:
        """将字符串或可迭代对象转换为短横线命名法"""
        return _humps.kebabize(str_or_iter)

    @staticmethod
    def split(s: str, delimiter: str = ",") -> list:
        """将字符串拆分为数组，使用指定的分隔符"""
        if StrUtils.is_empty(s):
            return []
        return [item.strip() for item in s.split(delimiter) if item.strip()]

    @staticmethod
    def camelize_dict_keys(d: dict) -> dict:
        """将字典的键转换为驼峰命名法"""
        if d is None:
            return {}
        return {StrUtils.camel_ize(k): v for k, v in d.items()}

    @staticmethod
    def decamelize_dict_keys(d: dict) -> dict:
        """将字典的键转换为蛇形命名法"""
        if d is None:
            return {}
        return {StrUtils.de_camelize(k): v for k, v in d.items()}

    @staticmethod
    def camelize_list_of_dicts(lst: list) -> list:
        """将字典列表的键转换为驼峰命名法"""
        if lst is None:
            return []
        return [StrUtils.camelize_dict_keys(item) if isinstance(item, dict) else item for item in lst]

    @staticmethod
    def decamelize_list_of_dicts(lst: list) -> list:
        """将字典列表的键转换为蛇形命名法"""
        if lst is None:
            return []
        return [StrUtils.decamelize_dict_keys(item) if isinstance(item, dict) else item for item in lst]
