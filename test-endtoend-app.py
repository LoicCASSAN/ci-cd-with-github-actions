import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time  # module pour voir les étapes de test

class TestAppE2E(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome('')
        self.driver.get('http://localhost:5000')

    def test_add_update_and_delete_item(self):
        # Ajout d'un item
        input_field = self.driver.find_element(By.NAME, 'item')
        input_field.send_keys('Item : Voiture')
        time.sleep(2)  # Attend 2 seconds  

        input_field.send_keys(Keys.RETURN)
        time.sleep(2)  

        # Vérication ajout de l'item
        self.assertIn('Item : Voiture', self.driver.page_source)

        # Cherche le bouton update
        update_links = self.driver.find_elements(By.XPATH, '//a[contains(@href, "/update/")]')
        if update_links:
            update_links[0].click()
            time.sleep(2)  

        # Updated de l'item
        update_field = self.driver.find_element(By.NAME, 'new_item')
        update_field.send_keys('Item : Voiture Updated')
        update_field.send_keys(Keys.RETURN)
        time.sleep(2)  

        # Vérification update
        self.assertIn('Item : Voiture Updated', self.driver.page_source)

        # Suppression de l'item
        delete_buttons = self.driver.find_elements(By.XPATH, '//a[contains(@href, "/delete/")]')
        if delete_buttons:
            delete_buttons[0].click()  
            time.sleep(2)  

        # Vérification suppression
        self.assertNotIn('Item : Voiture Updated', self.driver.page_source)

    def tearDown(self):
        time.sleep(2) 
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
