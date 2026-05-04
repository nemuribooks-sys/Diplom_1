import pytest
from unittest.mock import Mock
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


class TestBurger:
    def test_set_buns(self, burger, mock_bun):
        """Тест установки булочки"""
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun
    
    def test_set_buns_none(self, burger):
        """Тест установки None в качестве булочки"""
        burger.set_buns(None)
        assert burger.bun is None

    def test_add_single_ingredient(self, burger, mock_ingredient_sauce):
        """Тест добавления одного ингредиента"""
        burger.add_ingredient(mock_ingredient_sauce)
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == mock_ingredient_sauce
    
    def test_add_multiple_ingredients(self, burger, mock_ingredient_sauce, mock_ingredient_filling):
        """Тест добавления нескольких ингредиентов"""
        burger.add_ingredient(mock_ingredient_sauce)
        burger.add_ingredient(mock_ingredient_filling)
        assert len(burger.ingredients) == 2
        assert burger.ingredients[0] == mock_ingredient_sauce
        assert burger.ingredients[1] == mock_ingredient_filling

    @pytest.mark.parametrize("index_to_remove, expected_count, expected_first_type", [
        (0, 2, INGREDIENT_TYPE_FILLING),   # Удаляем первый
        (1, 2, INGREDIENT_TYPE_SAUCE),     # Удаляем второй
        (2, 2, INGREDIENT_TYPE_SAUCE),     # Удаляем последний
    ])
    def test_remove_ingredient(self, burger, mock_ingredient_sauce, 
                               mock_ingredient_filling, index_to_remove, 
                               expected_count, expected_first_type):
        """Параметризованный тест удаления ингредиентов"""
        # Добавляем 3 ингредиента
        ing_extra = Mock(spec=Ingredient)
        ing_extra.get_type.return_value = INGREDIENT_TYPE_SAUCE
        
        burger.add_ingredient(mock_ingredient_sauce)      # индекс 0
        burger.add_ingredient(mock_ingredient_filling)    # индекс 1
        burger.add_ingredient(ing_extra)                  # индекс 2
        
        # Удаляем по индексу
        burger.remove_ingredient(index_to_remove)
        
        # Проверяем количество
        assert len(burger.ingredients) == expected_count
        
        # Проверяем тип первого оставшегося ингредиента
        if expected_count > 0:
            assert burger.ingredients[0].get_type() == expected_first_type
    
    def test_remove_ingredient_out_of_range(self, burger, mock_ingredient_sauce):
        """Тест удаления ингредиента с невалидным индексом"""
        burger.add_ingredient(mock_ingredient_sauce)
        
        # Должно выбросить исключение
        with pytest.raises(IndexError):
            burger.remove_ingredient(5)

    @pytest.mark.parametrize("old_index, new_index, expected_order", [
        (0, 1, ["filling", "sauce", "extra"]),      # Перемещаем первый на вторую позицию
        (1, 0, ["filling", "sauce", "extra"]),      # Перемещаем второй на первую позицию
        (0, 0, ["sauce", "filling", "extra"]),      # Перемещаем на ту же позицию
        (2, 0, ["extra", "sauce", "filling"]),  # Перемещаем последний в начало
        ])
    
    def test_move_ingredient(self, burger, mock_ingredient_sauce, 
                             mock_ingredient_filling, old_index, 
                             new_index, expected_order):
        """Параметризованный тест перемещения ингредиентов"""
        # Создаем дополнительный ингредиент
        ing_extra = Mock(spec=Ingredient)
        ing_extra.get_type.return_value = INGREDIENT_TYPE_FILLING
        ing_extra.get_name.return_value = "extra"
        
        # Добавляем ингредиенты
        burger.add_ingredient(mock_ingredient_sauce)    # 0: sauce
        burger.add_ingredient(mock_ingredient_filling)  # 1: filling
        burger.add_ingredient(ing_extra)                # 2: extra
        
        # Перемещаем
        burger.move_ingredient(old_index, new_index)
        
        # Проверяем порядок имен
        actual_order = [ing.get_name() for ing in burger.ingredients]
        
        # Ожидаемые имена
        expected_names = []
        for name in expected_order:
            if name == "sauce":
                expected_names.append("Test Sauce")
            elif name == "filling":
                expected_names.append("Test Filling")
            elif name == "extra":
                expected_names.append("extra")
        
        assert actual_order == expected_names
    
    def test_move_ingredient_invalid_old_index(self, burger, mock_ingredient_sauce):
        """Тест перемещения с невалидным исходным индексом"""
        burger.add_ingredient(mock_ingredient_sauce)
        
        with pytest.raises(IndexError):
            burger.move_ingredient(5, 0)
    
    def test_move_ingredient_invalid_new_index(self, burger, mock_ingredient_sauce):
        """Тест перемещения с невалидным целевым индексом"""
        burger.add_ingredient(mock_ingredient_sauce)
        original_len = len(burger.ingredients)
        
        burger.move_ingredient(0, 10)

        len(burger.ingredients) == original_len
        assert mock_ingredient_sauce in burger.ingredients

    def test_get_price_without_bun(self, burger, mock_ingredient_sauce):
        """Тест цены бургера без булочки"""
        burger.add_ingredient(mock_ingredient_sauce)
        
        # Должно упасть с ошибкой, так как bun = None
        with pytest.raises(AttributeError):
            burger.get_price()
    
    def test_get_price_with_bun_only(self, burger, mock_bun):
        """Тест цены бургера только с булочкой"""
        burger.set_buns(mock_bun)
        expected_price = mock_bun.get_price() * 2  # 50 * 2 = 100
        assert burger.get_price() == expected_price
    
    def test_get_price_with_bun_and_ingredients(self, burger, mock_bun, mock_ingredient_sauce, mock_ingredient_filling):
        """Тест полной цены бургера"""
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient_sauce)   # 30
        burger.add_ingredient(mock_ingredient_filling) # 40
        
        expected_price = (mock_bun.get_price() * 2) + 30 + 40  # 100 + 70 = 170
        assert burger.get_price() == expected_price
    

    def test_get_receipt_without_bun(self, burger, mock_ingredient_sauce):
        """Тест чека без булочки (должен упасть)"""
        burger.add_ingredient(mock_ingredient_sauce)
        
        with pytest.raises(AttributeError):
            burger.get_receipt()
    
    def test_get_receipt_with_bun_only(self, burger, mock_bun):
        """Тест чека только с булочкой"""
        burger.set_buns(mock_bun)
        receipt = burger.get_receipt()
        
        expected_lines = [
            f'(==== {mock_bun.get_name()} ====)',
            f'(==== {mock_bun.get_name()} ====)',
            '',
            f'Price: {mock_bun.get_price() * 2}'
        ]
        
        actual_lines = receipt.split('\n')
        
        assert actual_lines[0] == expected_lines[0]
        assert actual_lines[1] == expected_lines[1]
        assert actual_lines[2] == expected_lines[2]
        assert actual_lines[3] == expected_lines[3]
    
    def test_get_receipt_full_burger(self, burger, mock_bun, mock_ingredient_sauce, mock_ingredient_filling):
        """Тест полного чека бургера с ингредиентами"""
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient_sauce)
        burger.add_ingredient(mock_ingredient_filling)
        
        receipt = burger.get_receipt()
        
        # Проверяем структуру чека
        assert f'(==== {mock_bun.get_name()} ====)' in receipt
        assert f'= {mock_ingredient_sauce.get_type().lower()} {mock_ingredient_sauce.get_name()} =' in receipt
        assert f'= {mock_ingredient_filling.get_type().lower()} {mock_ingredient_filling.get_name()} =' in receipt
        assert f'Price: {burger.get_price()}' in receipt
        
        # Проверяем порядок строк
        lines = receipt.split('\n')
        assert len(lines) == 6  # Верхняя булка + 2 ингредиента + нижняя булка + пустая + цена
        
        # Проверяем вызовы методов
        mock_bun.get_name.assert_called()
        mock_ingredient_sauce.get_type.assert_called()
        mock_ingredient_sauce.get_name.assert_called()
        mock_ingredient_filling.get_type.assert_called()
        mock_ingredient_filling.get_name.assert_called()
    
    def test_get_receipt_with_sauce_only(self, burger, mock_bun, mock_ingredient_sauce):
        """Тест чека только с соусом"""
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient_sauce)
        
        receipt = receipt = burger.get_receipt()
        
        assert f'= {INGREDIENT_TYPE_SAUCE.lower()} {mock_ingredient_sauce.get_name()} =' in receipt
    
    def test_get_receipt_correct_format(self, burger, mock_bun, mock_ingredient_sauce):
        """Тест правильного форматирования чека"""
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient_sauce)
        
        receipt = burger.get_receipt()
        lines = receipt.split('\n')
        
        assert lines[0] == f'(==== {mock_bun.get_name()} ====)'
        assert lines[1] == f'= {mock_ingredient_sauce.get_type().lower()} {mock_ingredient_sauce.get_name()} ='
        assert lines[2] == f'(==== {mock_bun.get_name()} ====)'
        # lines[3] - пустая строка (может быть или не быть в зависимости от реализации)
        assert lines[-1].startswith('Price: ')
