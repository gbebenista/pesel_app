import datetime
import time
from random import choice
from faker import Faker


def timer(func):
    def wrapper_timer(*args, **kwargs):
        start_time = time.time()
        do_things = func(*args, **kwargs)
        stop_time = time.time()
        elapsed_time = stop_time - start_time
        print("Executing time is: ", elapsed_time)
        return do_things

    return wrapper_timer


class PeselNotValid(Exception):
    pass

class GenderNotValid(Exception):
    pass


class Pesel:
    VALID_PESEL_LENGTH = 11

    def __init__(self, **kwargs):
        self._pesel = self._pesel_to_list(kwargs.get('peselkwarg', None))

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

    # metody do generowania PESEL

    def _get_year_to_generate_pesel(self, dob):
        if isinstance(dob.year, int):
            if 1800 <= dob.year <= 2299:
                year = str(dob.year)
                return year
            raise ValueError("Year must be between 1800 and 2299")
        raise AttributeError("Year must be a string")

    def _get_day_to_generate_pesel(self, dob):
        if isinstance(dob.day, int):
            day = str(dob.day)
            if len(day) == 1:
                day_list = ["0", day[0]]
            else:
                day_list = [day[0], day[1]]
            return day_list
        raise AttributeError

    def _month_dictionary(self, dob):

        year = [self._get_year_to_generate_pesel(dob)[0], self._get_year_to_generate_pesel(dob)[1]]
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

    def _get_month_to_generate_pesel(self, dob):
        if isinstance(dob.month, int):
            month = str(dob.month)
            if len(month) == 2 and month[0] == "1":
                month_list = [self._month_dictionary(dob) + 1, month[1]]
            else:
                month_list = [self._month_dictionary(dob), month[0]]
            return month_list
        raise AttributeError

    def _get_gender_value(self, gender):
        if isinstance(gender, str):
            if gender == "K":
                gender_value = choice(range(0, 8, 2))
                return gender_value
            elif gender == "M":
                gender_value = choice(range(1, 9, 2))
                return gender_value
            raise GenderNotValid("Gender must be 'M' or 'K'")
        raise TypeError("gender must be a string or 'M','K'")

    @staticmethod
    def _get_random_number():
        random_to_pesel = str(choice(range(0, 9, 1)))

        return random_to_pesel

    def _join_pesel_elements(self, dob, gender):
        pesel_elements = [self._get_year_to_generate_pesel(dob)[2], self._get_year_to_generate_pesel(dob)[3],
                          self._get_month_to_generate_pesel(dob)[0], self._get_month_to_generate_pesel(dob)[1],
                          self._get_day_to_generate_pesel(dob)[0], self._get_day_to_generate_pesel(dob)[1],
                          self._get_random_number(),
                          self._get_random_number(), self._get_random_number(), self._get_gender_value(gender)]

        return pesel_elements

    def _make_control_sum(self, dob, gender):

        control_sum_formula = [9, 7, 3, 1, 9, 7, 3, 1, 9, 7]
        control_sum = 0

        i = 0
        while i < 10:
            control_sum += int(self._join_pesel_elements(dob, gender)[i]) * control_sum_formula[i]
            i += 1

        return control_sum

    def _get_control_digit(self, dob, gender):
        control_digit = self._make_control_sum(dob, gender) % 10
        return control_digit

    def _join_control_digit_to_pesel(self, dob, gender):
        pesel_with_joined_control_digit = self._join_pesel_elements(dob, gender)

        pesel_with_joined_control_digit.append(self._get_control_digit(dob, gender))

        return pesel_with_joined_control_digit

    @timer
    def generate(self, dob, gender):
        generated_pesel_joined = ''.join(map(str, self._join_control_digit_to_pesel(dob, gender)))
        return generated_pesel_joined

    def fake_pesel(self, dob, gender):
        fake = Faker("pl_PL")
        return fake.pesel(dob, gender)
