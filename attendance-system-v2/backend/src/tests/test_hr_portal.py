import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from app.main import app


class HrPortalTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_hr_login_and_dashboard_access(self):
        response = self.client.post(
            '/api/v1/auth/login',
            json={
                'email': 'hr@example.com',
                'password': 'hrpass',
                'role': 'hr',
            },
        )

        self.assertEqual(response.status_code, 200, response.text)
        payload = response.json()
        self.assertEqual(payload['user']['role'], 'hr')

        dashboard_response = self.client.get('/api/v1/hr/dashboard')
        self.assertEqual(dashboard_response.status_code, 200, dashboard_response.text)
        dashboard_payload = dashboard_response.json()
        self.assertIn('summary', dashboard_payload)
        self.assertGreater(dashboard_payload['summary']['employees'], 0)


if __name__ == '__main__':
    unittest.main()
