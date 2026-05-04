import pytest
from unittest.mock import Mock
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING
from praktikum.burger import Burger

@pytest.fixture
def burger():
        """Создает пустой бургер для каждого теста"""
        return Burger()

@pytest.fixture
def mock_bun():
        """Мок булочки"""
        bun = Mock(spec=Bun)
        bun.get_name.return_value = "Test Bun"
        bun.get_price.return_value = 50.0
        return bun

@pytest.fixture
def mock_ingredient_sauce():
        """Мок ингредиента-соуса"""
        ing = Mock(spec=Ingredient)
        ing.get_type.return_value = INGREDIENT_TYPE_SAUCE
        ing.get_name.return_value = "Test Sauce"
        ing.get_price.return_value = 30.0
        return ing
    
@pytest.fixture
def mock_ingredient_filling():
        """Мок ингредиента-начинки"""
        ing = Mock(spec=Ingredient)
        ing.get_type.return_value = INGREDIENT_TYPE_FILLING
        ing.get_name.return_value = "Test Filling"
        ing.get_price.return_value = 40.0
        return ing

@pytest.fixture
def real_bun():
    """Реальная булочка для интеграционных тестов"""
    return Bun("Real Black Bun", 150)


@pytest.fixture
def real_ingredient_sauce():
    """Реальный ингредиент-соус"""
    return Ingredient(INGREDIENT_TYPE_SAUCE, "Real Hot Sauce", 75)


@pytest.fixture
def real_ingredient_filling():
    """Реальный ингредиент-начинка"""
    return Ingredient(INGREDIENT_TYPE_FILLING, "Real Cutlet", 120)