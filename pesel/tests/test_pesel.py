import datetime

import pytest

from pesel.pesel import Pesel, PeselNotValid, GenderNotValid


class TestClass:

    @pytest.fixture
    def test_fixture(self):
        assert 0

    def test_short_pesel_not_valid(self):
        with pytest.raises(PeselNotValid):
            result = Pesel(peselkwarg="2423").validate()
            assert result

    def test_pesel_string(self):
        result = Pesel(peselkwarg="12345678901")
        assert result

    def test_pesel_int(self):
        assert Pesel(peselkwarg=12345678901)

    def test_pesel_lenght(self):
        result = len(Pesel(peselkwarg="12345").pesel) != 11
        assert result

    def test_pesel_char(self):
        with pytest.raises(ValueError):
            result = Pesel(peselkwarg="qwertyuiop")
            assert result

    def test_gender_woman(self):
        gender_woman = Pesel(peselkwarg="97082035264").gender_check()
        assert gender_woman == "Kobieta"

    def test_gender_man(self):
        gender_man = Pesel(peselkwarg="97081032157").gender_check()
        assert gender_man == "Mężczyzna"

    def test_birthdate_correct(self, fmt=1):
        birthdate_correct = Pesel(peselkwarg="97121100156").date_of_birth(fmt)
        assert birthdate_correct == "1997-Dec-11"

    def test_birthdate_failure(self, fmt=1):
        with pytest.raises(ValueError) as e:
            birthdate_failure = Pesel(peselkwarg="97341100156").date_of_birth(fmt)
            assert e.value == 'month must be in 1..12'

    def test_control_sum_correct(self):
        result = Pesel(peselkwarg="97341100156")._calculate_control_sum()
        assert result

    def test_control_sum_failure(self):
        with pytest.raises(ValueError) as e:
            result = Pesel(peselkwarg="qweetrywer1")._calculate_control_sum()
            assert result

    def test_validate_correct(self):
        result = Pesel(peselkwarg="97081800157").validate()
        assert result

    def test_validate_failure(self):
        with pytest.raises(PeselNotValid):
            result = Pesel(peselkwarg="97081800167").validate()
            assert result

    # testy dla generowania numeru PESEL

    def test_get_year_to_generate_correct(self):
        dob = datetime.date(1992, 3, 3)
        result = Pesel()._get_year_to_generate_pesel(dob)
        assert result == "1992"

    def test_get_year_to_generate_wrong_type(self):
        with pytest.raises(AttributeError) as e:
            dob = "dfsdfdf"
            result = Pesel()._get_year_to_generate_pesel(dob)
            assert e

    def test_get_year_to_generate_wrong_year(self):
        with pytest.raises(ValueError) as e:
            dob = datetime.date(1700, 4, 4)
            result = Pesel()._get_year_to_generate_pesel(dob)
            assert e

    def test_get_day_to_generate_correct(self):
        dob = datetime.datetime(1992, 3, 13)
        result = Pesel()._get_day_to_generate_pesel(dob)
        assert result == ["1", "3"]

    def test_get_day_to_generate_wrong_type(self):
        with pytest.raises(TypeError) as e:
            dob = datetime.time(1992, 3, "5354")
            result = Pesel()._get_day_to_generate_pesel(dob)
            assert e

    def test_get_day_to_generate_wrong_attribute(self):
        with pytest.raises(AttributeError) as e:
            dob = "DFds"
            result = Pesel()._get_day_to_generate_pesel(dob)
            assert e

    def test_get_day_to_generate_wrong_day_value(self):
        with pytest.raises(ValueError) as e:
            dob = datetime.datetime(1992, 12, 32)
            result = Pesel()._get_day_to_generate_pesel(dob)
            assert e

    def test_get_month_to_generate_correct(self):
        dob = datetime.datetime(1992, 3, 31)
        result = Pesel()._get_day_to_generate_pesel(dob)
        assert result

    def test_get_month_to_generate_wrong_attribute(self):
        with pytest.raises(AttributeError) as e:
            dob = "fdsfsd"
            result = Pesel()._get_day_to_generate_pesel(dob)
            assert result

    def test_get_month_to_generate_wrong_type(self):
        with pytest.raises(TypeError) as e:
            dob = datetime.datetime(1992, 31, "32")
            result = Pesel()._get_day_to_generate_pesel(dob)
            assert result

    def test_get_month_to_generate_wrong_value(self):
        with pytest.raises(ValueError) as e:
            dob = datetime.datetime(1992, 31, 31)
            result = Pesel()._get_day_to_generate_pesel(dob)
            assert result

    def test_gender_value_woman(self):
        gender = "K"
        result = Pesel()._get_gender_value(gender)
        assert result % 2 == 0

    def test_gender_value_man(self):
        gender = "M"
        result = Pesel()._get_gender_value(gender)
        assert result % 2 == 1

    def test_gender_value_wrong_type(self):
        with pytest.raises(TypeError) as e:
            gender_value = 3
            result = Pesel()._get_gender_value(gender_value)
            assert e

    def test_gender_value_not_gender(self):
        with pytest.raises(GenderNotValid) as e:
            gender_value = "R"
            result = Pesel()._get_gender_value(gender_value)
            assert e

    def test_join_pesel_elements_correct(self):
        dob = datetime.datetime(1942, 3, 5)
        gender = "K"
        result = Pesel()._join_pesel_elements(dob, gender)
        assert result

    def test_join_pesel_elements_gender_not_valid(self):
        with pytest.raises(GenderNotValid) as e:
            dob = datetime.datetime(1942, 3, 5)
            gender = "R"
            result = Pesel()._join_pesel_elements(dob, gender)
            assert e

    def test_join_pesel_elements_dob_not_valid(self):
        with pytest.raises(ValueError) as e:
            dob = datetime.datetime(1942, 33, 5)
            gender = "K"
            result = Pesel()._join_pesel_elements(dob, gender)
            assert e

    def test_make_control_sum_correct(self):
        dob = datetime.datetime(1932, 12, 3)
        gender = "K"
        result = Pesel()._make_control_sum(dob, gender)
        assert result

    def test_make_control_sum_dob_not_valid(self):
        with pytest.raises(AttributeError) as e:
            dob = "3223"
            gender = "K"
            result = Pesel()._make_control_sum(dob, gender)
            assert result

    def test_make_control_sum_gender_not_valid(self):
        with pytest.raises(GenderNotValid) as e:
            dob = datetime.datetime(1932, 12, 3)
            gender = "a"
            result = Pesel()._make_control_sum(dob, gender)
            assert e

    def test_get_control_digit_correct(self):
        dob = datetime.datetime(1932, 12, 3)
        gender = "K"
        result = Pesel()._get_control_digit(dob, gender)
        assert 0 <= result <= 9

    def test_get_control_digit_failure(self):
        with pytest.raises(AttributeError) as e:
            dob = "erew2"
            gender = 2
            result = Pesel()._get_control_digit(dob, gender)
            assert e

    def test_get_control_digit_gender_not_valid(self):
        with pytest.raises(GenderNotValid) as e:
            dob = datetime.datetime(1932, 12, 3)
            gender = "W"
            result = Pesel()._get_control_digit(dob, gender)
            assert e

    def test_join_control_digit_to_pesel_correct(self):
        dob = datetime.datetime(1826, 12, 3)
        gender = "M"
        result = Pesel()._join_control_digit_to_pesel(dob, gender)
        assert result

    def test_join_control_digit_to_pesel_failure(self):
        with pytest.raises(AttributeError):
            dob = 1997 - 4 - 12
            gender = "K"
            result = Pesel()._join_control_digit_to_pesel(dob, gender)
            assert result

    def test_generate_correct(self):
        dob = datetime.datetime(1932, 12, 3)
        gender = "M"
        result = Pesel().generate(dob, gender)
        assert result

    def test_generate_failure(self):
        with pytest.raises(AttributeError) as e:
            dob = "343"
            gender = "M"
            result = Pesel().generate(dob, gender)
            assert e

    def test_generate_dob_empty(self):
        with pytest.raises(AttributeError) as e:
            dob = ""
            gender = "M"
            result = Pesel().generate(dob, gender)
            assert e

    def test_generate_gender_failure(self):
        with pytest.raises(GenderNotValid) as e:
            dob = datetime.datetime(1826, 12, 3)
            gender = "R"
            result = Pesel().generate(dob, gender)
            assert e



