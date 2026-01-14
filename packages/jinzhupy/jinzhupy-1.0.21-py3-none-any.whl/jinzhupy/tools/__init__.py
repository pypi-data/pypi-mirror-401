# -*- coding: utf-8 -*-
# @Author	: brotherbaby
# @Date		: 2025/8/22 10:18
# @Last Modified by:   brotherbaby
# @Last Modified time: 2025/8/22 10:18
# Thanks for your comments!

from typing import Any, List, Set, Union


def check_post_params(params, must_list, must_type=None, is_or=False):
    if not isinstance(must_list, list):
        return True
    if is_or:
        for field in must_list:
            if field in params:
                return True
        return "lack %s" % ','.join(must_list)
    if isinstance(params, list):
        for p in params:
            p_result = check_post_params(p, must_list)
            if isinstance(p_result, str):
                return p_result
    if isinstance(params, dict):
        for attr in must_list:
            if attr not in params:
                return 'lack %s' % attr
    if must_type and isinstance(must_type, dict):
        for k, v in must_type.items():
            if not isinstance(params.get(k), v):
                return "%s type error, need %s" % (k, str(v))
    return True


def build_in_clause(values: Union[List[Any], Set[Any]]):
    """
    将数组转换为SQL中IN条件的字符串格式
    """
    if not values:
        raise ValueError("输入数组不能为空，无法生成有效的IN条件")

    processed = []
    for value in values:
        if isinstance(value, (int, float)):
            # 数值类型直接转换为字符串
            processed.append(str(value))
        elif isinstance(value, str):
            processed.append(f"'{value}'")
        else:
            # 不支持的类型
            raise TypeError(f"不支持的元素类型: {type(value)}，仅支持int、float、str")

    return f"({', '.join(processed)})"
