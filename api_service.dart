import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/attendance.dart';

class ApiService {
  final Dio _dio = Dio(BaseOptions(
    baseUrl: 'http://localhost:8000/api/v1',
    connectTimeout: const Duration(seconds: 5),
    receiveTimeout: const Duration(seconds: 3),
  ));

  ApiService() {
    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        final prefs = await SharedPreferences.getInstance();
        final token = prefs.getString('access_token');
        if (token != null) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        return handler.next(options);
      },
    ));
  }

  Future<Response> login(String email, String password) async {
    return await _dio.post('/login', data: {
      'username': email,
      'password': password,
    });
  }

  Future<List<Attendance>> getAttendances() async {
    final response = await _dio.get('/attendance');
    return (response.data as List).map((e) => Attendance.fromJson(e)).toList();
  }

  Future<Attendance> checkIn() async {
    final response = await _dio.post('/attendance/check-in');
    return Attendance.fromJson(response.data);
  }

  Future<Attendance> checkOut() async {
    final response = await _dio.post('/attendance/check-out');
    return Attendance.fromJson(response.data);
  }
}
