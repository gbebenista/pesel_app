import datetime
from generatepesel import GeneratePesel


class PeselNotValid(Exception):
    pass


class Pesel():
    VALID_PESEL_LENGTH = 11

    def __init__(self, **kwargs):
        self._pesel = self._pesel_to_list(kwargs.get('peselkwarg', None))
        self.generate = GeneratePesel()

    @property
    def pesel(self):
        return self._pesel

    @pesel.setter
    def pesel(self, value):
        self._pesel = value

    @staticmethod
    def _pesel_to_list(pesel):
        if isinstance(pesel, tuple):
            for p in pesel:
                pesel_number = pesel(p)
        elif isinstance(pesel, int):
            pesel_number = [int(x) for x in str(pesel)]
        elif not pesel:
            return
        else:
            pesel_number = list(map(int, pesel))
        return pesel_number

    def _calculate_control_sum(self):
        control_sum_formula = [9, 7, 3, 1, 9, 7, 3, 1, 9, 7]
        control_sum = 0

        i = 0
        while i < 10:
            control_sum += self._pesel[i] * control_sum_formula[i]
            i += 1

        return control_sum

    def _is_pesel_length_valid(self):
        return len(self._pesel) == self.VALID_PESEL_LENGTH

    def _is_control_sum_valid(self):
        return self._calculate_control_sum() % 10 == self.pesel[10]

    def validate(self):
        if self._is_pesel_length_valid() and self._is_control_sum_valid():
            return True
        raise PeselNotValid("Pesel not valid")

    def _get_year_from_pesel(self):
        century_dic = {
            8: 18,
            0: 19,
            2: 20,
            4: 21,
            6: 22
        }

        century_check = 0

        if self.pesel[2] % 2 == 1:
            century_check = self.pesel[2] - 1

        year = [century_dic.get(century_check), self.pesel[0], self.pesel[1]]

        year_joined = int(''.join(map(str, year)))
        return year_joined

    def _get_month_from_pesel(self):
        if self.pesel[2] % 2 == 0:
            month = [0, self.pesel[3]]
        else:
            month = [1, self.pesel[3]]

        month_joined = int(''.join(map(str, month)))
        return month_joined

    def _get_day_from_pesel(self):
        day = [self.pesel[4], self.pesel[5]]

        day_joined = int(''.join(map(str, day)))
        return day_joined

    def _date_format_dictionary(self, format):
        date_format_dict = {
            1: "%Y-%b-%d",
            2: "%Y/%b/%d",
            3: "%Y:%B:%d",
            4: "%Y %B %d"
        }

        format_value = date_format_dict.get(format)
        return format_value

    def date_of_birth(self, format):
        date_of_birth = datetime.date(self._get_year_from_pesel(), self._get_month_from_pesel(),
                                      self._get_day_from_pesel())

        return date_of_birth.strftime(self._date_format_dictionary(format))

    def gender_check(self):

        gender = "Mężczyzna"
        if int(self.pesel[9]) % 2 == 0:
            gender = "Kobieta"
        return gender
