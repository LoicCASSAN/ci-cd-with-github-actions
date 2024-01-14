from flask import Flask, request, render_template, redirect, url_for
from werkzeug.serving import make_server
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
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
# Test d'intégration avec Selenium
class TestAppE2E(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Démarrage de l'application Flask dans un thread séparé
        cls.app = create_app()
        cls.server = make_server('0.0.0.0', 5000, cls.app)  # Écoute sur toutes les interfaces
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.start()
        time.sleep(1)  # Attendre que l'application démarre

        # Configuration de Selenium WebDriver pour utiliser le service Selenium distant
        cls.driver = webdriver.Remote(
            command_executor='http://host.docker.internal:4444/wd/hub', 
            desired_capabilities=webdriver.DesiredCapabilities.CHROME
        )

    def test_add_update_and_delete_item(self):
        self.driver.get('http://host.docker.internal:5000')  # Assurez-vous que cette URL est accessible depuis votre conteneur


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
        cls.driver.quit()
        cls.server.shutdown()
        cls.server_thread.join()

# Exécution des tests si exécuté en tant que script principal
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)