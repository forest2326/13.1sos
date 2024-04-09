from src.phone import Phone
import pytest
"""Тесты для модуля phone."""


@pytest.fixture
def phone1():
    return Phone("Nokia", 10000, 20, 1)


@pytest.fixture
def phone2():
    return Phone("Huaway", 20000, 5, 22)



@pytest.mark.parametrize('phone',
    ['phone1',
     'phone2']
)
def test_add(phone, request):
    """Тест сложения объектов Phone"""
    phone = request.getfixturevalue(phone)
    phone_other = Phone("Xiomi", 10000, 20, 44)
    assert phone + phone_other == phone.quantity + phone_other.quantity
    assert phone_other + phone == phone.quantity + phone_other.quantity

    with pytest.raises(ValueError, match=r'Складывать можно только объекты Item и дочерние от них.'):
        phone + 100

def test_phone_represent():
    phone1 = Phone("iPhone 14", 120_000, 5, 2)
    assert str(phone1) == 'iPhone 14'
    assert repr(phone1) == "Phone('iPhone 14', 120000, 5, 2)"


def test_set_number_of_sim():
    """Тест сеттера set_number_of_sim"""
    phone1 = Phone("iPhone 14", 120_000, 5, 2)

    phone1.number_of_sim = 1

    with pytest.raises(ValueError, match=r"Количество физических SIM-карт должно быть целым числом больше нуля"):
        phone1.number_of_sim = 0

    with pytest.raises(ValueError, match=r"Количество физических SIM-карт должно быть целым числом больше нуля"):
        phone1.number_of_sim = 0.0

    with pytest.raises(ValueError, match=r"Количество физических SIM-карт должно быть целым числом больше нуля"):
        phone1.number_of_sim = -1

    with pytest.raises(ValueError, match=r"Количество физических SIM-карт должно быть целым числом больше нуля"):
        phone1.number_of_sim = "test"

    # # ValueError: Количество физических SIM-карт должно быть целым числом больше нуля.