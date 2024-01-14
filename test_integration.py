import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class TestAppE2E(unittest.TestCase):
    def setUp(self):
        # Configuration de Selenium WebDriver pour utiliser le service Selenium distant
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--remote-debugging-port=9222')

        self.driver = webdriver.Remote(
            command_executor='http://chrome:4444/wd/hub',
            options=options
        )
        self.driver.get("http://web:5000/")

    def test_add_update_and_delete_item(self):
        # Ajout d'un item
        input_field = self.driver.find_element(By.NAME, 'item')
        input_field.send_keys('Item : Voiture')
        input_field.send_keys(Keys.RETURN)
        time.sleep(2)  # Attendre 2 secondes pour le traitement

        # Vérification de l'ajout de l'item
        self.assertIn('Item : Voiture', self.driver.page_source)

        # Mise à jour de l'item
        update_links = self.driver.find_elements(By.XPATH, '//a[contains(@href, "/update/")]')
        if update_links:
            update_links[0].click()
            time.sleep(2)

            update_field = self.driver.find_element(By.NAME, 'new_item')
            update_field.send_keys('Item : Voiture Updated')
            update_field.send_keys(Keys.RETURN)
            time.sleep(2)

            # Vérification de la mise à jour
            self.assertIn('Item : Voiture Updated', self.driver.page_source)

        # Suppression de l'item
        delete_buttons = self.driver.find_elements(By.XPATH, '//a[contains(@href, "/delete/")]')
        if delete_buttons:
            delete_buttons[0].click()
            time.sleep(2)

        # Vérification de la suppression
        self.assertNotIn('Item : Voiture Updated', self.driver.page_source)

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()



