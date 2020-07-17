import re


class Common:
    @staticmethod
    def standardize_phone_number(mobile):
        valid_prefixes = '[+98|98|0098|09]'
        result = re.match('^' + valid_prefixes + '*([0-9]{10})$', mobile)
        if result:
            return '98' + result.group(1)
        else:
            return None
