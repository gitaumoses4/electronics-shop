import json
import unittest
import app
import models


class CategoriesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.create_app("TESTING")
        self.client = self.app.test_client
        self.headers = {'Content-Type': 'application/json'}
        self.category = json.dumps({
            'id': 0,
            'name': 'Laptops',
            'parent_id': 0
        })

    def test_category_creation(self):
        res = self.client().post('/api/v1/category', data=self.category, headers=self.headers)

        with self.app.app_context():
            models.db.drop_all()
        json_result = json.loads(res.get_data(as_text=True))

        print(json_result)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(json_result['name'], "Laptops")
        self.assertEqual(json_result['parent_id'], 0)


if __name__ == '__main__':
    unittest.main()
