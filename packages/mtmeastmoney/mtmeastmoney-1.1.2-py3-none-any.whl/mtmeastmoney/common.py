import datetime


def today(fmt="%Y%m%d"):
    return datetime.datetime.now().strftime(fmt)


def yesterday(fmt="%Y%m%d"):
    return (datetime.datetime.now() - datetime.timedelta(days=1)).strftime(fmt)


def filter_market_STAR(code):
    # 判断是否是科创板代码
    return code.startswith("688") or code.startswith("689")


def filter_market_GEM(code):
    # 判断是否是创业板代码
    return code.startswith("300") or code.startswith("301")


def filter_market_NEEQ(code):
    # 判断是否是北交所代码
    return code.startswith("43") or code.startswith("83") or code.startswith("87")


def filter_market_SH(code):
    # 判断是否是上交所代码
    return code.startswith("60")


def filter_market_SZ(code):
    # 判断是否是深交所代码
    return code.startswith("00") or code.startswith("30")
