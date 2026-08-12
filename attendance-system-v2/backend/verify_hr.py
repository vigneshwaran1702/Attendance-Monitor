import os
import sys

sys.path.insert(0, os.path.abspath('src'))
from app.api.v1.api import login, hr_dashboard
from app.api.v1.api import LoginRequest

response = login(LoginRequest(email='hr@example.com', password='hrpass', role='hr'))
print('login_role=' + response['user']['role'])
print('dashboard_employees=' + str(len(hr_dashboard()['employees'])))
