import re
import calendar
import time as _time
import datetime as _datetime
from dateutil import rrule, relativedelta


class Moment:

    def __init__(self):
        pass

    def timeStamp(self):
        '''
        获取时间戳
        :return: 时间戳（1629294055.8056374）
        '''
        return _time.time()

    def stamp_to_struct_time(self, now=None):
        '''
        时间戳转换为 struct_time
        :param now:
        :return:struct_time
        '''
        if not now:
            now = _time.time()

        return _time.localtime(float(now))

    def struct_time_to_stamp(self, struct_time=None):
        '''
        struct_time 转换为时间戳
        :param struct_time:
        :return:时间戳
        '''

        if not struct_time:
            struct_time = self.stamp_to_struct_time()
        return _time.mktime(struct_time)

    def struct_time_to_datetime(self, struct_time=None):
        '''
        struct_time 转换为标准时间datetime
        :param struct_time:
        :return:datetime
        '''

        if not struct_time:
            struct_time = self.stamp_to_struct_time()
        return _time.strftime("%Y-%m-%d %H:%M:%S", struct_time)

    def datetime_to_struct_time(self, datetime=None):
        '''
        标准格式的time转换为struct_time
        :param datetime:
        :return: struct_time
        '''
        if not datetime:
            datetime = self.struct_time_to_datetime()
        return _time.strptime(datetime, "%Y-%m-%d %H:%M:%S")

    def stamp_to_datetime(self, now=None):
        '''
        时间戳转换为年月日时分秒
        :param now: 时间戳
        :return: datetime
        '''
        return _time.strftime("%Y-%m-%d %H:%M:%S", self.stamp_to_struct_time(now))

    def datetime_to_stamp(self, datetime=None):
        '''
        标准时间转换为时间错
        :param datetime:
        :return: 时间错
        '''

        struct_time = self.datetime_to_struct_time(datetime)
        return self.struct_time_to_stamp(struct_time)

    def datetime_format(self, datetime, delimiter=""):
        '''
        格式化标准时间
        :param datetime: 年月日时分秒
        :param delimiter: 分隔符
        :return: 格式化后的标准时间
        '''

        datetime = str(datetime)
        reg_exp = r"[^0-9]"
        if delimiter:
            reg_exp = r"[^0-9" + reg_exp + "]"

        return re.sub(reg_exp, delimiter, datetime)

    def addzero(self, n):
        '''
        add 0 before 0-9
        :param n:
        :return:  01-09
        '''
        nabs = abs(int(n))
        if (nabs < 10):
            return "0" + str(nabs)
        else:
            return nabs

    def year(self, timeStamp=None):
        '''
        获取年
        :param timeStamp: 时间戳
        :return: 年
        '''
        return self.stamp_to_struct_time(timeStamp).tm_year

    def month(self, timeStamp=None):
        '''
        获取月
        :param timeStamp: 时间戳
        :return: 月
        '''
        tm_mon = self.stamp_to_struct_time(timeStamp).tm_mon
        return self.addzero(tm_mon)

    def day(self, timeStamp=None):
        '''
        获取日
        :param timeStamp: 时间戳
        :return: 日
        '''
        return self.stamp_to_struct_time(timeStamp).tm_mday

    def hour(self, timeStamp=None):
        '''
        获取小时
        :param timeStamp: 时间戳
        :return: 小时
        '''
        return self.stamp_to_struct_time(timeStamp).tm_hour

    def min(self, timeStamp=None):
        '''
        获取分钟
        :param timeStamp: 时间戳
        :return: 分钟
        '''
        return self.stamp_to_struct_time(timeStamp).tm_min

    def sec(self, timeStamp=None):
        '''
        获取秒
        :param timeStamp: 时间戳
        :return: 秒
        '''
        return self.stamp_to_struct_time(timeStamp).tm_sec

    def is_timeStamp(self, stamp):
        '''
        判断是否为时间戳
        :param stamp:
        :return:
        '''
        try:
            return self.stamp_to_datetime(stamp)
        except:
            return False

    def is_datetime(self, datetime):
        '''
        判断是否为标准时间
        :param datetime:
        :return:
        '''
        try:
            datetime = str(datetime)
            time_reg_exp_full = re.compile(r"\d{4}\D{1}\d{2}\D{1}\d{2} \d{2}:\d{2}:\d{2}")
            time_reg_exp = re.compile(r"\d{4}\D{1}\d{2}\D{1}\d{2}")
            matchs_list_full = time_reg_exp_full.findall(datetime)
            matchs_list = time_reg_exp.findall(datetime)
            sub_pattern = r"(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})"

            sub_repl = r"\1-\2-\3 \4:\5:\6"
            # 这里其实有点问题，但够用了

            if len(matchs_list_full) == 1:
                datetime = re.sub(sub_pattern, sub_repl, matchs_list_full[0])
                return datetime
            elif len(matchs_list) == 1:
                datetime = re.sub(sub_pattern, sub_repl, matchs_list[0])
                return datetime + " 00:00:00"
            else:
                return False
        except:
            return False

    def format_time(self, datetime, return_type):
        '''
        时间转换
        :param datetime: 原始时间
        :param return_type: 目标类型 struct_time\datetime\timeStamp
        :return: 目标类型的时间
        '''
        try:
            time_str = ""
            if isinstance(datetime, _time.struct_time):
                if return_type.lower() == "datetime":
                    time_str = self.stamp_to_datetime(datetime)
                elif return_type.lower() == "timestamp":
                    time_str = self.struct_time_to_stamp(datetime)
                else:
                    time_str = datetime
            elif self.is_timeStamp(datetime):
                if return_type.lower() == "datetime":
                    time_str = self.stamp_to_datetime(datetime)
                elif return_type.lower() == "struct_time":
                    time_str = self.stamp_to_struct_time(datetime)
                else:
                    time_str = datetime
            elif self.is_datetime(datetime):
                datetime = self.is_datetime(datetime)
                if return_type.lower() == "struct_time":
                    time_str = self.datetime_to_struct_time(datetime)
                elif return_type.lower() == "timestamp":
                    time_str = self.datetime_to_stamp(datetime)
                else:
                    time_str = datetime

            return time_str
        except BaseException as e:
            print(e)
            raise Exception("转换失败")

    def today(self):
        '''
        获取 “yyyy-MM-dd”格式日期
        :return: “yyyy-MM-dd”格式日期 （eg. 2021-08-19）
        '''

        return _datetime.date.today()

    def today_str(self):
        '''
        获取 “yyyyMMdd”格式日期
        :return: “yyyyMMdd”格式日期 （eg. 20210819）
        '''

        return self.datetime_format(self.today())

    def datetime(self):
        '''
        获取 “yyyy-MM-dd HH:mm:ss”格式日期
        :return: “yyyy-MM-dd HH:mm:ss”格式日期 （eg. 2021-08-19）
        '''

        return self.struct_time_to_datetime()

    def datetime_str(self):
        '''
        获取 “yyyyMMddHHmmss”格式日期
        :return: “yyyyMMddHHmmss”格式日期 （eg. 2021-08-19）
        '''

        return self.datetime_format(self.datetime())

    def get_current_year_month(self):
        '''
        获取当前年月
        :return: “yyyyMM” (eg. 20210819)
        '''

        return str(self.year()) + str(self.month())

    def get_datetime_of_day(self, n=0):
        '''
        获取当前日期前后N天的日期
        n>0 获取当前日期前N天的日期,
        n<0 获取当前日期后N天的日期
        date format = "YYYY-MM-DD"
        :param n:天数
        :return: "YYYY-MM-DD"
        '''

        if (n < 0):
            n = abs(n)
            return _datetime.date.today() - _datetime.timedelta(days=n)
        else:
            return _datetime.date.today() + _datetime.timedelta(days=n)

    def get_days_of_month(self, year, month):
        '''
        获取月份的天数
        :param year:
        :param month:
        :return:
        '''

        return calendar.monthrange(int(year), int(month))[1]

    def get_firstday_of_month(self, year, mon):
        '''
        获取月份的第一天
        :param year: 年
        :param mon: 月
        :return: "YYYY-MM-DD"格式日期 eg.2021-08-25
        '''
        days = "01"
        mon = self.addzero(mon)
        arr = (year, mon, days)
        return "-".join("%s" % i for i in arr)

    def get_lastday_of_month(self, year, mon):
        '''
        获取月份的最后一天
        :param year: 年
        :param mon: 月
        :return: "YYYY-MM-DD"格式日期 eg.2021-08-31
        '''

        days = calendar.monthrange(int(year), int(mon))[1]
        mon = self.addzero(mon)
        arr = (year, mon, days)
        return "-".join("%s" % i for i in arr)

    def get_year_month_days_from_month_number(self, n=0, arr=None):
        '''
        根据输入的月相对数量，返回年月日的元组，年为当前年份，日为当月最后一天
        :param n: befor or after n months
        :param arr: 指定年月日的元组
        :return: 年月日的元组 eg.("2019","09","30")
        '''

        cur_year = int(self.year())
        cur_month = int(self.month())

        if arr:
            cur_year = int(arr[0])
            cur_month = int(arr[1])

        totalmon = cur_month + n

        if (n > 0):
            if (totalmon <= 12):
                days = str(self.get_days_of_month(cur_year, cur_month))
                totalmon = self.addzero(totalmon)
                return (str(cur_year), totalmon, days)

            else:
                i = totalmon // 12
                _month = totalmon % 12

                if (_month == 0):
                    i -= 1
                    _month = 12
                    cur_year += i
                    days = str(self.get_days_of_month(cur_year, _month))
                    _month = self.addzero(_month)
                    return (str(cur_year), str(_month), days)

                else:
                    _month = self.addzero(_month)
                    cur_year += i
                    days = str(self.get_days_of_month(cur_year, _month))
                    _month = self.addzero(_month)
                    return (str(cur_year), str(_month), days)



        else:
            if ((totalmon > 0) and (totalmon < 12)):
                days = str(self.get_days_of_month(cur_year, totalmon))
                totalmon = self.addzero(totalmon)
                return (str(cur_year), totalmon, days)
            else:
                i = totalmon // 12
                _month = totalmon % 12

                if (_month == 0):
                    i -= 1
                    _month = 12
                    cur_year += i
                    days = str(self.get_days_of_month(cur_year, _month))
                    _month = self.addzero(_month)
                    return (str(cur_year), str(_month), days)
                else:
                    _month = self.addzero(_month)
                    cur_year += i
                    days = str(self.get_days_of_month(cur_year, _month))
                    _month = self.addzero(_month)
                    return (str(cur_year), str(_month), days)

    def get_date_from_month_number(self, n=0, arr=None):
        '''
        获取当前日期前后N月的日期
        :param n: berfor or after n months,if n>0,获取当前日期前N月的日期， if n<0,获取当前日期后N月的日期
        :param arr: 指定年月的元组
        :return: 返回当前日期前后N月的日期"YYYY-MM-DD"
        '''

        day = int(self.day())
        if arr:
            day = int(arr[2])

        (y, m, d) = self.get_year_month_days_from_month_number(n, arr)
        if (int(day) < int(d)):
            arr = (y, m, day)
        else:
            arr = (y, m, self.day())
        return "-".join("%s" % i for i in arr)

    def get_firstday_month(self, n=0):
        '''
        当前月份+n后的月份，包含月份第一天 YYYY-MM-01
        :param n: n是多少个月，支持负数
        :return: 当前月份+n后的月份的第一天
        '''

        (y, m, d) = self.get_year_month_days_from_month_number(n)
        d = "01"
        arr = (y, m, d)
        return "-".join("%s" % i for i in arr)

    def get_lastday_month(self, n=0):
        '''
        当前月份+n后的月份，包含月份最后一天 YYYY-MM-DD
        :param n: n是多少个月，支持负数
        :return: 当前月份+n后的月份的最后一天
        '''

        arr = self.get_year_month_days_from_month_number(n)
        return "-".join("%s" % i for i in arr)

    def get_match_date_from_date_and_number(self, date, n):
        '''
        获取对应日期前后N月的日期
        :param date: 日期
        :param n: berfor or after n months, if n>0，获取当前日期N月的日期，if n < 0,获取日期后N月的日期
        :return: YYYY-MM-DD
        '''

        time_reg_exp = re.compile(r"(\d{4})\D?(\d{1,2})\D?(\d{1,2})")
        arr = time_reg_exp.findall(date)[0]
        return self.get_date_from_month_number(n, arr)

    def get_year_month_from_number(self, year_month,n):
        '''
        获取对应日期前后N月的年月
        :param year_month: 年月 eg:202009
        :return:   YYYYMM eg.202108
        '''

        date = "{}01".format(year_month)

        new_date = self.get_match_date_from_date_and_number(date, n)
        new_year_month = new_date.replace("-", "")[:6]
        return new_year_month

    def is_greater(self, datetime1, datetime2):
        '''
        判断两个日期时间的先后顺序
        :param datetime1:
        :param datetime2:
        :return: 0, 日期相等，1，前值大，-1 前值小
        '''

        datetime1 = self.is_datetime(datetime1)
        datetime2 = self.is_datetime(datetime2)

        if datetime1 and datetime2:
            difference = self.datetime_to_stamp(datetime1) - self.datetime_to_stamp(datetime2)
            if difference == 0:
                return 0
            elif difference > 0:
                return 1
            else:
                return -1
        else:
            raise Exception("日期格式不正确")

    def datetime_diff(self, datetime1, datetime2):
        '''
        计算两个日期之前的差值
        :param datetime1:
        :param datetime2:
        :return: 年月日的差值（years,months,days） eg.(-1,-2,-4)
        '''

        oneDay, towDay = (datetime1, datetime2)
        is_greater = self.is_greater(datetime1, datetime2)

        if is_greater >= 0:
            oneDay, towDay = (datetime2, datetime1)

        time_reg_exp = re.compile(r"(\d{4})\D?(\d{1,2})\D?(\d{1,2})")
        arr1 = time_reg_exp.findall(oneDay)[0]
        arr2 = time_reg_exp.findall(towDay)[0]
        oneDay = _datetime.date(int(arr1[0]), int(arr1[1]), int(arr1[2]))
        towDay = _datetime.date(int(arr2[0]), int(arr2[1]), int(arr2[2]))

        days = rrule.rrule(rrule.DAILY, dtstart=oneDay, until=towDay).count()

        years = rrule.rrule(rrule.YEARLY, dtstart=oneDay, until=towDay).count()
        months = rrule.rrule(rrule.MONTHLY, dtstart=oneDay, until=towDay).count()

        if is_greater == 0:
            return (0, 0, 0)
        elif is_greater > 0:
            return (years, months, days)
        else:
            return (-years, -months, -days)


    def is_standard_datetime(self,datetime):
        '''
        判断日期是否为标准合法的日期
        :param datetime:
        :return:
        '''

        # 判断YYYY - MM - DD这种格式的，基本上把闰年和2月等的情况都考虑进去了
        r = r"^((((1[6-9]|[2-9]\d)\d{2})-(0?[13578]|1[02])-(0?[1-9]|[12]\d|3[01]))|(((1[6-9]|[2-9]\d)\d{2})-(0?[13456789]|1[012])-(0?[1-9]|[12]\d|30))|(((1[6-9]|[2-9]\d)\d{2})-0?2-(0?[1-9]|1\d|2[0-8]))|(((1[6-9]|[2-9]\d)(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00))-0?2-29-))$"
        reg_exp = re.compile(r)
        match = reg_exp.search(datetime)

        if match:
            today = self.today()
            try:
                is_greater = self.is_greater(today,datetime)
                if is_greater ==0:
                    return "It's today."
                elif is_greater > 0:
                    return "It's a past date."
                else:
                    return "It's a future date."
            except OverflowError:
                return "It's an old date."
            except BaseException as e:
                print(e)
        else:
            return False

    def get_monthly_arr(self,year_month):
        '''
        获取 年度分月
        :param year_month: 年月
        :return: 月份list
        '''

        year = year_month[0:4]
        month = year_month[4:6]

        def str_year_month(year,month):
            month = self.addzero(month)

            return str(year) + str(month)

        return [str_year_month(year,x) for x in range(1,int(month) + 1)]



moment = Moment()
