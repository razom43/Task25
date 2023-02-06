import pytest
from selenium import webdriver
import time

@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('C:\Task24\chromedriver.exe')
    # Переходим на страницу авторизации
    # неясное ожидание 10 секунд
    pytest.driver.implicitly_wait(10)
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()


def test_show_my_pets():
    # Вводим email
    pytest.driver.find_element_by_id('email').send_keys('evan3@gmail.com')
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys('Evan123')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="sub1mit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"
    # Получаем множество картинок питомцев
    images = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')
    # Получаем множество имен питомцев
    names = pytest.driver.find_elements_by_css_selector('.card-deck .card-title')
    # получаем множество возрастов и видов питомцев
    descriptions = pytest.driver.find_elements_by_css_selector('.card-deck .card-text')



    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0