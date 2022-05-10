import unittest
from selenium.webdriver.support.ui import Select
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class BuscarExpediente(unittest.TestCase):
    def setUp(self):
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        option.add_argument('--no-sandbox')

        self.driver = webdriver.Chrome(
            executable_path=r"C:\dchrome\chromedriver.exe", options=option)

    def test_Expediente(self):
        driver = self.driver
        driver.get(
            "https://expediente.mec.gub.uy/apps/FileCenter/ConsultaWeb2.nsf")

        # Coloca los datos correspondientes para realizar la busqueda

        select = Select(driver.find_element(by=By.ID, value='anio'))
        select.select_by_value("Ingresa el año")

        codigo = driver.find_element(by=By.ID, value="codigo")
        codigo.send_keys("Codigo")

        numero = driver.find_element(by=By.ID, value="numero")
        numero.send_keys("Numero")

        buscar = driver.find_element(by=By.ID, value="btnBus").click()

        driver.implicitly_wait(5)

        # Obtiene los resultados
        estado = driver.find_elements(
            by=By.XPATH, value='//*[@id="result"]/table/tbody/tr[4]/td[2]')
        oficina_actual = driver.find_elements(
            by=By.XPATH, value='//*[@id="result"]/table/tbody/tr[6]/td[2]')
        oficina_anterior = driver.find_elements(
            by=By.XPATH, value='//*[@id="result"]/table/tbody/tr[7]/td[2]')

        resultado = 'Estado del tramite: ' + estado[0].text + '\nOficina actual: ' + \
            oficina_actual[0].text + '\nOficina anterior: ' + \
            oficina_anterior[0].text

        # Envia los resultados por telegram
        bot_token = 'TOKEN'
        chatID = 'CHAT ID'

        send_text = 'https://api.telegram.org/bot' + bot_token + \
            '/sendMessage?chat_id=' + chatID + '&parse_mode=Markdown&text=' + resultado

        response = requests.get(send_text)
        return response.json()

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
