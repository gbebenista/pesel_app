import datetime
from random import choice
from faker import Faker


class PeselNotValid(Exception):
    pass


class Pesel:
    VALID_PESEL_LENGTH = 11

    def __init__(self, **kwargs):
        self._pesel = self.pesel_to_list(kwargs.get('peselkwarg', None))

    @property
    def pesel(self):
        return self._pesel

    @pesel.setter
    def pesel(self, value):
        self._pesel = value

    @staticmethod
    def pesel_to_list(pesel):
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

    def _check_control_sum(self):
        return self._calculate_control_sum() % 10 == self.pesel[10]

    def validate(self):
        if self._is_pesel_length_valid() and self._check_control_sum():
            return True
        raise PeselNotValid("Pesel not valid")

    def _year(self):
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

    def _month(self):
        if self.pesel[2] % 2 == 0:
            month = [0, self.pesel[3]]
        else:
            month = [1, self.pesel[3]]

        month_joined = int(''.join(map(str, month)))
        return month_joined

    def _day(self):
        day = [self.pesel[4], self.pesel[5]]

        day_joined = int(''.join(map(str, day)))
        return day_joined

    def date_of_birth(self):
        date_of_birth = datetime.date(self._year(), self._month(), self._day())

        return date_of_birth.strftime("%Y-%b-%d")

    def _date_format(self, format):
        date_format_dict = {
            1: "%Y-%b-%d",
            2: "%Y/%b/%d",
            3: "%Y:%B:%d",
            4: "%Y %B %d"
        }

        format_value = date_format_dict.get(format)
        return format_value

    def date_of_birth_with_format(self, format):
        date_of_birth = datetime.date(self._year(), self._month(), self._day())

        return date_of_birth.strftime(self._date_format(format))

    def gender_check(self):

        gender = "Mężczyzna"
        if int(self.pesel[9]) % 2 == 0:
            gender = "Kobieta"
        return gender

    # metody do generowania PESEL

    def get_year(self, dob):
        year = str(dob.year)
        return year

    def get_day(self, dob):
        day = str(dob.day)
        return day

    def get_gender_value(self, gender):
        if gender == "K":
            gender_value = choice(range(0, 8, 2))
        elif gender == "M":
            gender_value = choice(range(1, 9, 2))

        return gender_value

    def month_dictionary(self, dob):

        year = [self.get_year(dob)[0], self.get_year(dob)[1]]
        year_joined = int(''.join(map(str, year)))

        month_dict = {
            18: 8,
            19: 0,
            20: 2,
            21: 4,
            22: 6
        }

        right_month = month_dict.get(year_joined)
        return right_month

    def get_month(self, dob):
        month = str(dob.month)
        if len(month) == 2 and month[0] == "1":
            month_list = [self.month_dictionary(dob) + 1, month[1]]
        else:
            month_list = [self.month_dictionary(dob), month[0]]
        return month_list

    @staticmethod
    def random_number():
        random_to_pesel = str(choice(range(0, 9, 1)))

        return random_to_pesel

    def prepare_pesel(self, dob, gender):
        prepared_pesel = [self.get_year(dob)[2], self.get_year(dob)[3], self.get_month(dob)[0], self.get_month(dob)[1],
                          self.get_day(dob)[0], self.get_day(dob)[1], self.random_number(),
                          self.random_number(), self.random_number(), self.get_gender_value(gender)]

        return prepared_pesel

    def prepare_to_generate(self, dob, gender):

        control_sum_formula = [9, 7, 3, 1, 9, 7, 3, 1, 9, 7]
        control_sum = 0

        i = 0
        while i < 10:
            control_sum += int(self.prepare_pesel(dob, gender)[i]) * control_sum_formula[i]
            i += 1

        return control_sum

    def prepare_control_digit(self, dob, gender):
        control_digit = self.prepare_to_generate(dob, gender) % 10
        return control_digit

    def generate(self, dob, gender):
        generated_pesel = self.prepare_pesel(dob, gender)

        generated_pesel.append(self.prepare_control_digit(dob, gender))

        generated_pesel_joined = int(''.join(map(str, generated_pesel)))

        return generated_pesel_joined

    def fake_pesel(self, dob, gender):
        fake = Faker("pl_PL")
        return fake.pesel(dob, gender)