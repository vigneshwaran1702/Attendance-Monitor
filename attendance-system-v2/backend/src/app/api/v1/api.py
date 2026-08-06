from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query, Path
from pydantic import BaseModel, EmailStr

api_router = APIRouter()

first_names = [
    'Alice','Bob','Clara','David','Eve','Frank','Grace','Helen','Isaac','Jade',
    'Kyle','Lina','Mason','Nora','Omar','Paula','Quinn','Riley','Sara','Tom',
    'Uma','Victor','Wendy','Xavier','Yara','Zane','Amy','Brad','Celia','Dylan'
]
last_names = [
    'Johnson','Martinez','Lee','Brown','Davis','Garcia','Miller','Wilson','Taylor','Anderson',
    'Thomas','Martin','Jackson','White','Harris','Clark','Lewis','Robinson','Walker','Perez',
    'Hall','Young','Allen','Sanchez','Wright','King','Scott','Green','Baker','Adams'
]

class AttendanceRecord(BaseModel):
    date: str
    status: str
    hours: float
    checkIn: str
    checkOut: str

class UserResponse(BaseModel):
    email: EmailStr
    name: str
    role: str
    records: List[AttendanceRecord] = []

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    role: str

class LoginResponse(BaseModel):
    user: UserResponse
    token: str

class SaveAttendanceRequest(BaseModel):
    email: EmailStr
    date: str
    status: str

class AdminSummary(BaseModel):
    employees: int
    totalHours: float
    onTimeRate: float
    totalLate: int

class AdminEmployeeSummary(BaseModel):
    name: str
    email: EmailStr
    present: int
    absent: int
    late: int
    hours: float

class PermissionRequestModel(BaseModel):
    id: int
    email: EmailStr
    name: str
    type: str
    date: str
    time: str
    status: str

class CreatePermissionRequest(BaseModel):
    email: EmailStr
    type: str
    date: str
    time: str

class UpdatePermissionRequest(BaseModel):
    status: str

admin_user = {
    'email': 'admin@example.com',
    'password': 'adminpass',
    'name': 'Attendance Admin',
    'role': 'admin',
}

employees = []
permission_requests = []
request_id_counter = 1


def create_attendance_record(date: str, status: str) -> dict:
    hours = 0.0 if status == 'Absent' else 7.5 if status == 'Late' else 8.0
    check_in = '-'
    check_out = '-'
    if status != 'Absent':
        if status == 'Late':
            minute = 10 + (hash(date) % 30)
            check_in = f'09:{minute:02d}'
        else:
            check_in = f'09:{(hash(date) % 10):02d}'
        check_out = f'17:{(hash(date + status) % 30):02d}'
    return {
        'date': date,
        'status': status,
        'hours': hours,
        'checkIn': check_in,
        'checkOut': check_out,
    }


def generate_records(record_count: int = 30) -> List[dict]:
    statuses = ['Present', 'Present', 'Late', 'Present', 'Absent']
    records = []
    for day in range(1, record_count + 1):
        status = statuses[day % len(statuses)]
        records.append(create_attendance_record(f'2026-07-{day:02d}', status))
    return records


def initialize_employees() -> List[dict]:
    result = []
    for index in range(30):
        first = first_names[index % len(first_names)]
        last = last_names[index % len(last_names)]
        email = f'employee{index + 1}@example.com'
        result.append({
            'id': index + 1,
            'name': f'{first} {last}',
            'email': email,
            'password': 'password',
            'role': 'employee',
            'records': generate_records(),
        })
    return result


employees = initialize_employees()


def find_user(email: str) -> Optional[dict]:
    email = email.lower()
    if email == admin_user['email']:
        return admin_user
    return next((user for user in employees if user['email'] == email), None)


@api_router.post('/auth/login', response_model=LoginResponse)
def login(request: LoginRequest):
    user = find_user(request.email)
    if not user or user.get('password') != request.password or request.role not in ['employee', 'admin']:
        raise HTTPException(status_code=401, detail='Invalid email, password, or role.')
    if request.role == 'admin' and user['email'] != admin_user['email']:
        raise HTTPException(status_code=401, detail='Admin login requires the admin account.')
    if request.role == 'employee' and user['email'] == admin_user['email']:
        raise HTTPException(status_code=401, detail='Employee login requires an employee account.')

    response_user = {
        'email': user['email'],
        'name': user['name'],
        'role': user['role'],
        'records': user.get('records', []),
    }
    return {
        'user': response_user,
        'token': 'fake-token-for-demo',
    }


@api_router.get('/attendance', response_model=List[AttendanceRecord])
def get_attendance(email: EmailStr = Query(...)):
    user = find_user(email)
    if not user or user['role'] != 'employee':
        raise HTTPException(status_code=404, detail='Employee not found.')
    return user['records']


@api_router.post('/attendance', response_model=List[AttendanceRecord])
def save_attendance(payload: SaveAttendanceRequest):
    user = find_user(payload.email)
    if not user or user['role'] != 'employee':
        raise HTTPException(status_code=404, detail='Employee not found.')

    if not payload.date or not payload.status:
        raise HTTPException(status_code=400, detail='Date and status are required.')

    approved_late = next((r for r in permission_requests if r['email'] == user['email'] and r['date'] == payload.date and r['type'] == 'Late Arrival' and r['status'] == 'Approved'), None)
    approved_early = next((r for r in permission_requests if r['email'] == user['email'] and r['date'] == payload.date and r['type'] == 'Early Logoff' and r['status'] == 'Approved'), None)

    final_status = payload.status
    if payload.status == 'Late' and approved_late:
        final_status = 'Present'

    existing = next((record for record in user['records'] if record['date'] == payload.date), None)
    record = create_attendance_record(payload.date, final_status)
    
    if approved_late:
        record['checkIn'] = approved_late['time']
    if approved_early:
        record['checkOut'] = approved_early['time']

    if existing:
        existing.update(record)
    else:
        user['records'].insert(0, record)
    return user['records']


@api_router.get('/admin/dashboard')
def admin_dashboard():
    total_hours = sum(sum(record['hours'] for record in user['records']) for user in employees)
    total_present = sum(1 for user in employees for record in user['records'] if record['status'] != 'Absent')
    total_possible = len(employees) * (len(employees[0]['records']) if employees else 0)
    total_late = sum(1 for user in employees for record in user['records'] if record['status'] == 'Late')
    employee_summaries = []
    for user in employees:
        present = sum(1 for record in user['records'] if record['status'] != 'Absent')
        absent = sum(1 for record in user['records'] if record['status'] == 'Absent')
        late = sum(1 for record in user['records'] if record['status'] == 'Late')
        hours = sum(record['hours'] for record in user['records'])
        employee_summaries.append({
            'name': user['name'],
            'email': user['email'],
            'present': present,
            'absent': absent,
            'late': late,
            'hours': hours,
        })
    return {
        'summary': {
            'employees': len(employees),
            'totalHours': total_hours,
            'onTimeRate': round((total_present / total_possible) * 100, 0) if total_possible else 0,
            'totalLate': total_late,
        },
        'employees': employee_summaries,
    }

@api_router.get('/admin/user-history', response_model=List[AttendanceRecord])
def admin_user_history(email: EmailStr = Query(...)):
    user = find_user(email)
    if not user or user['role'] != 'employee':
        raise HTTPException(status_code=404, detail='Employee not found.')
    return user['records']

@api_router.post('/permissions', response_model=PermissionRequestModel)
def create_permission(payload: CreatePermissionRequest):
    global request_id_counter
    user = find_user(payload.email)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    req = {
        'id': request_id_counter,
        'email': user['email'],
        'name': user['name'],
        'type': payload.type,
        'date': payload.date,
        'time': payload.time,
        'status': 'Pending'
    }
    request_id_counter += 1
    permission_requests.append(req)
    return req

@api_router.get('/permissions', response_model=List[PermissionRequestModel])
def get_permissions(email: EmailStr = Query(...)):
    return [req for req in permission_requests if req['email'] == email.lower()]

@api_router.get('/admin/permissions', response_model=List[PermissionRequestModel])
def get_admin_permissions():
    return permission_requests

@api_router.put('/admin/permissions/{req_id}', response_model=PermissionRequestModel)
def update_permission(req_id: int = Path(...), payload: UpdatePermissionRequest = None):
    req = next((r for r in permission_requests if r['id'] == req_id), None)
    if not req:
        raise HTTPException(status_code=404, detail='Request not found')
    req['status'] = payload.status
    return req
