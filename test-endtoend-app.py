from flask import Flask, request, render_template, redirect, url_for
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import time
import threading

# Application Flask
def create_app():
    app = Flask(__name__)
    items = []

    @app.route('/')
    def index():
        return render_template('index.html', items=items)

    @app.route('/add', methods=['POST'])
    def add_item():
        item = request.form.get('item')
        if item:
            items.append(item)
        return redirect(url_for('index'))

    @app.route('/delete/<int:index>')
    def delete_item(index):
        if index < len(items):
            items.pop(index)
        return redirect(url_for('index'))

    @app.route('/update/<int:index>', methods=['POST'])
    def update_item(index):
        if index < len(items):
            items[index] = request.form.get('new_item')
        return redirect(url_for('index'))

    return app

# Test d'intégration avec Selenium
class TestAppE2E(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Démarrage de l'application Flask dans un thread séparé
        cls.app = create_app()
        cls.app_thread = threading.Thread(target=lambda: cls.app.run(debug=True, use_reloader=False, host='0.0.0.0'))
        cls.app_thread.start()
        time.sleep(1)  # Attendre que l'application démarre

        # Configuration de Selenium WebDriver pour utiliser le conteneur Selenium
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')

        cls.driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            options=options
        )

        cls.driver.get('http://localhost:5000')

    def test_add_update_and_delete_item(self):
        # Ajout d'un item
        input_field = self.driver.find_element(By.NAME, 'item')
        input_field.send_keys('Item : Voiture')
        time.sleep(2)
        input_field.send_keys(Keys.RETURN)
        time.sleep(2)

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

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.app_thread.join()

# Exécution des tests si exécuté en tant que script principal
if __name__ == '__main__':
    unittest.main()
