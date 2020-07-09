import pytest
from pesel import Pesel, PeselNotValid


class TestPesel:

    @pytest.fixture
    def pesel_correct_example_man(self):
        p = Pesel(peselkwarg=12320471479)
        return p

    @pytest.fixture
    def pesel_correct_example_woman(self):
        p = Pesel(peselkwarg=12320481700)
        return p

    @pytest.fixture
    def pesel_incorrect_example(self):
        p = Pesel(peselkwarg=12345677910)
        return p

    @pytest.fixture
    def pesel_toolong_example(self):
        p = Pesel(peselkwarg=909204136101)
        return p

    @pytest.fixture
    def pesel_string_example(self):
        p = Pesel(peselkwarg="12320471479")
        return p

    @pytest.fixture
    def pesel_tooshort_example(self):
        p = Pesel(peselkwarg="3234")
        return p

    def test_validate_correct(self, pesel_correct_example_man):
        result = pesel_correct_example_man.validate()
        assert result

    def test_validaate_not_valid_toolong(self, pesel_toolong_example):
        with pytest.raises(PeselNotValid):
            result = pesel_toolong_example.validate()
            assert result

    def test_short_pesel_not_valid(self, pesel_tooshort_example):
        with pytest.raises(PeselNotValid) as e:
            result = pesel_tooshort_example.validate()
            assert result

    def test_pesel_string(self, pesel_string_example):
        result = pesel_string_example
        assert result

    def test_pesel_int(self, pesel_correct_example_man):
        result = pesel_correct_example_man
        assert result

    def test_pesel_lenght(self, pesel_tooshort_example):
        with pytest.raises(PeselNotValid):
            result = pesel_tooshort_example.validate()
            assert result

    def test_pesel_char(self):
        with pytest.raises(ValueError):
            result = Pesel(peselkwarg="sdfds")
            assert result

    def test_gender_woman(self, pesel_correct_example_woman):
        gender_woman = pesel_correct_example_woman.gender_check()
        assert gender_woman == "Kobieta"

    def test_gender_man(self, pesel_correct_example_man):
        gender_man = pesel_correct_example_man.gender_check()
        assert gender_man == "Mężczyzna"

    def test_birthdate_correct(self, pesel_correct_example_man, fmt=1):
        birthdate_correct = pesel_correct_example_man.date_of_birth(fmt)
        assert birthdate_correct == "2012-Dec-04"

    def test_birthdate_failure(self, fmt=1):
        with pytest.raises(ValueError) as e:
            birthdate_failure = Pesel(peselkwarg="97341100156").date_of_birth(fmt)
            assert e.value == 'month must be in 1..12'

    def test_control_sum_correct(self, pesel_correct_example_man):
        result = pesel_correct_example_man._calculate_control_sum()
        assert result

    def test_control_sum_failure(self):
        with pytest.raises(ValueError):
            result = Pesel(peselkwarg="fdsfser")._calculate_control_sum()
            assert result





