import unittest
from app import app

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_read_page(self):
        print("Testing 1 : reading the main page...")
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200, "Page should load with status code 200")
        print("Passed: Main page loads correctly\n")

    def test_add_item(self):
        print("Testing 2 : adding an item...")
        response = self.app.post('/add', data=dict(item="Test Item"), follow_redirects=True)
        self.assertEqual(response.status_code, 200, "Response should be 200 OK")
        print("Passed: Item added successfully\n")

    def test_delete_item(self):
        print("Testing 3 : deleting an item...")
        # Add an item first
        add_response = self.app.post('/add', data=dict(item="Test Item"), follow_redirects=True)
        self.assertEqual(add_response.status_code, 200, "Item should be added")

        # Delete the item
        delete_response = self.app.get('/delete/0', follow_redirects=True)
        self.assertEqual(delete_response.status_code, 200, "Item should be deleted")
        print("Passed: Item deleted successfully\n")
        
    def test_update_item(self):
        print("Testing 4 : updating an item...")
        # Add an item first
        self.app.post('/add', data=dict(item="Test Item"), follow_redirects=True)

        # Update the item
        response = self.app.post('/update/0', data=dict(new_item="Updated Item"), follow_redirects=True)
        self.assertEqual(response.status_code, 200, "Response should be 200 OK")
        print("Passed: Item updated successfully\n")


    #Autre test
    def test_add_and_delete_specific_item(self):
        print("Testing 5 : adding three items and deleting the second one...")

        # Ajoutez trois éléments
        for i in range(3):
            self.app.post('/add', data=dict(item=f"Test Item {i+1}"), follow_redirects=True)

        # Supprimez le deuxième élément
        delete_response = self.app.get('/delete/1', follow_redirects=True)
        self.assertEqual(delete_response.status_code, 200, "Second item should be deleted")

        # Vérifiez que le deuxième élément a été supprimé et que les autres sont toujours là
        response = self.app.get('/')
        self.assertNotIn("Test Item 2", response.data.decode())
        self.assertIn("Test Item 1", response.data.decode())
        self.assertIn("Test Item 3", response.data.decode())

        print("Passed: Three items added and second item deleted successfully\n")


if __name__ == '__main__':
    unittest.main()
