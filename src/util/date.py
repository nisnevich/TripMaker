class DateUtil:
    @staticmethod
    def diff_month(d1, d2):
        '''
        :param d1: greater date
        :param d2: lower date
        :return: difference between dates in calendar months
        '''
        return (d1.year - d2.year) * 12 + d1.month - d2.month
