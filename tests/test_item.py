"""Здесь надо написать тесты с использованием pytest для модуля item."""
from src.item import Item
import pytest

"""Тесты для модуля item."""


@pytest.fixture
def item1():
    return Item("Смартфон", 10000, 20)


@pytest.fixture
def item2():
    return Item("Ноутбук", 20000, 5)


# Тест расчета общей стоимости одинаковых товаров.
@pytest.mark.parametrize('item, excepted',
                         [("item1", 200000),
                          ("item2", 100000)]
                         )
def test_total_price(item, excepted, request):
    """Тест расчета общей цены за N шт товаров"""
    item = request.getfixturevalue(item)
    assert item.calculate_total_price() == excepted


# Тест расчета скидки на 1шт товара
@pytest.mark.parametrize('item, excepted',
                         [("item1", 8000),
                          ("item2", 16000)]
                         )
def test_discount(item, excepted, request):
    """Тест расчет дисконта"""
    item = request.getfixturevalue(item)
    Item.pay_rate = 0.8
    item.apply_discount()
    assert item.price == excepted


# Тест формирования списка со всеми созданными товарами на уровне класса Item
@pytest.mark.parametrize('item',
                         ['item1',
                          'item2']
                         )
def test_fill_all(item, request):
    """Тест автоматического добавления объекта Item в список Item.all. После инициализации Item"""
    item = request.getfixturevalue(item)
    # Список не пуст
    assert any(Item.all) is True
    # Созданные элементы попали в список
    assert item in Item.all


def test_instantiate_from_csv():
    """Тестирование метода instantiate_from_csv чтения списка Items из файла"""
    # это добавление в all должно затереться при вызове instantiate_from_csv, судя по логике описанной в main. hw2.
    # Т.к. 5шт это только в csv файле
    Item("наименование", 1, 2)
    Item.instantiate_from_csv('src/items.csv')  # создание объектов из данных файла
    assert len(Item.all) == 5  # в файле 5 записей с данными по товарам

    with pytest.raises(FileNotFoundError):
        Item.instantiate_from_csv('src/no_file.csv')


def test_string_to_number():
    """Тесты функции string_to_number преоразования строки-числа в целое число.
    Округялется в меньшую сторону до целого"""
    assert Item.string_to_number('5') == 5
    assert Item.string_to_number('5.0') == 5
    assert Item.string_to_number('5.9') == 5
    with pytest.raises(ValueError):
        Item.string_to_number('error str num')


def test_set_name():
    """Проверка, что выставленную в сеттере строку при привышении 10 символов записываются только первый 10 символов"""

    init_name = "Наименование заданное через инициализатор"
    item = Item(init_name, 1, 2)
    assert item.name == init_name

    # наименование менее 10 символов, геттер выдаст полностью
    new_name = "Машинка"
    item.name = new_name
    assert item.name == new_name

    # наименования больше 10 символов
    new_name = 'Машинка для стирки'
    item.name = new_name
    assert item.name == new_name[0: 10]


def test_item_represent():
    item = Item("Утюг", 1200, 100)
    assert repr(item) == "Item('Утюг', 1200, 100)"
    assert str(item) == 'Утюг'


@pytest.mark.parametrize('item',
                         ['item1',
                          'item2']
                         )
def test_add(item, request):
    """Тест расчет дисконта"""
    item = request.getfixturevalue(item)
    item_other = Item("Смартфон", 10000, 20)
    assert item + item_other == item.quantity + item_other.quantity
    assert item_other + item == item.quantity + item_other.quantity

    with pytest.raises(ValueError, match=r'Складывать можно только объекты Item и дочерние от них.'):
        item + 100
