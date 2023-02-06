import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('C:\Task24\chromedriver.exe')
   pytest.driver.maximize_window()
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')

   yield
   time.sleep(1)
   pytest.driver.quit()


def login():
   # явное ожидание поля email 10 секунд
   element_email = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.ID, "email"))
   )
   # заполняем поле email
   element_email.send_keys('evan3@gmail.com')
   # Заполняем поле пароль
   element_pass = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.ID, "pass"))
   )
   element_pass.send_keys('Evan123')

   # Нажимаем на кнопку входа в аккаунт

   element_login_btn = WebDriverWait(pytest.driver, 10).until(
      EC.element_to_be_clickable((By.CLASS_NAME, "btn-success"))
   )
   element_login_btn.click()
   # включаем фильтр мои питомцы
   pytest.driver.find_element_by_css_selector('a[href="/my_pets"]').click()

def count():
   # получаем количество питомцев
   my_pet_amount = pytest.driver.find_element_by_xpath('(//div[@class=".col-sm-4 left"])')
   my_pet_amount = my_pet_amount.get_attribute('innerText')
   # Получааем первый индекс строки где храниться количество питомцев
   index_start = int(my_pet_amount.index(": ") + 2)
   # Получаем последний индекс строки где храниться количество питомцев
   index_end = int(my_pet_amount.index("\nДрузей"))
   # Получчаем поличество питомцев пользователя
   count = int(my_pet_amount[index_start:index_end])
   return count

def test_amount_my_pets():
   login()
   count_ = count()
   # получем количество питомцев отображенных в таблице
   count_mypet = pytest.driver.find_elements_by_css_selector('td.smart_cell')
   # Проверяем что количество питомцев равно количеству питомцев отображенных в таблице
   assert len(count_mypet) == count_

def test_amount_my_pets_photo():
   login()
   count_ = count()
   # получаем фотографии питомцев
   images = pytest.driver.find_elements_by_css_selector('#all_my_pets img')
   count_images = 0
   # считаем количество фоторгафий
   for i in range(len(images)):
      if images[i].get_attribute('src') != '':
         count_images += 1
   # Проверяем что фотографий больше чем у половины питомцев
   assert count_images >= count_/2

def test_None_filed_my_pets():
   login()
   # получаем имена, возраст и порода питомцев
   descriptions = pytest.driver.find_elements_by_css_selector('#all_my_pets td')
   # Проверяем отсутствие пустых полей
   for i in range(len(descriptions)):
      assert descriptions[i].text != 'None'

def test_unique_name_may_pets():
   login()
   # получаем список только ссылок на имена питомцев
   names = pytest.driver.find_elements_by_css_selector('#all_my_pets td:nth-child(2)')
   # составляем список имен питомцев
   names_list = []
   for i in range(len(names)):
      names_list.append(names[i].get_attribute('innerText'))
   # переводим список имен в множество имен
   names_set = set(names_list)
   # Проверяем наличие повторяжийхся имен (сравниваме размер списка и множества)
   assert len(names_set) == len(names_list)

def test_unique_may_pets():
   login()
   # получаем список только ссылок на данные питомцев
   descriptions = pytest.driver.find_elements_by_css_selector('#all_my_pets tbody tr')
   descriptions_list = []
   for i in range(len(descriptions)):
      descriptions_list.append(descriptions[i].get_attribute('innerText'))
   # переводим список данных питомцев в множество
   descriptions_set = set(descriptions_list)
   # Проверяем наличие повтовряжийхся данных питомце (сравниваме размер списка и множества)
   assert len(descriptions_set) == len(descriptions_list), 'Есть повторяющиеся питомцы'

