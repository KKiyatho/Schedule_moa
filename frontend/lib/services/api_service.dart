import 'package:dio/dio.dart';
import '../models/user.dart';
import '../models/schedule_item.dart';
import '../models/calendar.dart';
import '../models/document.dart';
import '../models/tag.dart';

class ApiService {
  static const String baseUrl = 'http://localhost:8000';
  static const String apiVersion = '/api/v1';

  late Dio _dio;

  ApiService() {
    _dio = Dio(
      BaseOptions(
        baseUrl: '$baseUrl$apiVersion',
        connectTimeout: const Duration(seconds: 10),
        receiveTimeout: const Duration(seconds: 10),
        headers: {
          'Content-Type': 'application/json',
        },
      ),
    );

    // Add interceptor for logging
    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) {
          print('🚀 [${options.method}] ${options.path}');
          return handler.next(options);
        },
        onResponse: (response, handler) {
          print('✅ [${response.statusCode}] ${response.requestOptions.path}');
          return handler.next(response);
        },
        onError: (error, handler) {
          print('❌ [ERROR] ${error.requestOptions.path}');
          print('   ${error.message}');
          return handler.next(error);
        },
      ),
    );
  }

  // Health Check
  Future<bool> healthCheck() async {
    try {
      final response = await _dio.get('/health');
      return response.statusCode == 200;
    } catch (e) {
      print('Health check failed: $e');
      return false;
    }
  }

  // Auth - Register
  Future<Map<String, dynamic>?> register({
    required String email,
    required String username,
    required String password,
  }) async {
    try {
      final response = await _dio.post(
        '/auth/register',
        data: {
          'email': email,
          'username': username,
          'password': password,
        },
      );
      if (response.statusCode == 200) {
        return response.data;
      }
    } catch (e) {
      print('Register failed: $e');
    }
    return null;
  }

  // Auth - Login
  Future<Map<String, dynamic>?> login({
    required String email,
    required String password,
  }) async {
    try {
      final response = await _dio.post(
        '/auth/login',
        data: {
          'email': email,
          'password': password,
        },
      );
      if (response.statusCode == 200) {
        return response.data;
      }
    } catch (e) {
      print('Login failed: $e');
    }
    return null;
  }

  // Auth - Get current user
  Future<User?> getCurrentUser() async {
    try {
      final response = await _dio.get('/auth/me');
      if (response.statusCode == 200) {
        return User.fromJson(response.data);
      }
    } catch (e) {
      print('Get current user failed: $e');
    }
    return null;
  }

  // Calendars
  Future<List<Calendar>?> getCalendars({int skip = 0, int limit = 100}) async {
    try {
      final response = await _dio.get(
        '/calendars',
        queryParameters: {'skip': skip, 'limit': limit},
      );
      if (response.statusCode == 200) {
        return (response.data as List).map((item) => Calendar.fromJson(item as Map<String, dynamic>)).toList();
      }
    } catch (e) {
      print('Get calendars failed: $e');
    }
    return null;
  }

  Future<Calendar?> getCalendar(int id) async {
    try {
      final response = await _dio.get('/calendars/$id');
      if (response.statusCode == 200) {
        return Calendar.fromJson(response.data);
      }
    } catch (e) {
      print('Get calendar failed: $e');
    }
    return null;
  }

  Future<Calendar?> createCalendar({
    required String name,
    String? description,
    String? color,
  }) async {
    try {
      final response = await _dio.post(
        '/calendars',
        data: {
          'name': name,
          'description': description,
          'color': color,
        },
      );
      if (response.statusCode == 200) {
        return Calendar.fromJson(response.data);
      }
    } catch (e) {
      print('Create calendar failed: $e');
    }
    return null;
  }

  // Schedule Items
  Future<List<ScheduleItem>?> getScheduleItems({
    int skip = 0,
    int limit = 100,
    String? status,
    String? itemType,
  }) async {
    try {
      final response = await _dio.get(
        '/items',
        queryParameters: {
          'skip': skip,
          'limit': limit,
          if (status != null) 'status': status,
          if (itemType != null) 'item_type': itemType,
        },
      );
      if (response.statusCode == 200) {
        final data = response.data as Map<String, dynamic>;
        final items = (data['items'] as List? ?? [])
            .map((item) => ScheduleItem.fromJson(item as Map<String, dynamic>))
            .toList();
        return items;
      }
    } catch (e) {
      print('Get schedule items failed: $e');
    }
    return null;
  }

  Future<ScheduleItem?> getScheduleItem(int id) async {
    try {
      final response = await _dio.get('/items/$id');
      if (response.statusCode == 200) {
        return ScheduleItem.fromJson(response.data);
      }
    } catch (e) {
      print('Get schedule item failed: $e');
    }
    return null;
  }

  Future<ScheduleItem?> createScheduleItem({
    required int calendarId,
    required String title,
    String? description,
    required String type,
    String? status,
    DateTime? startDate,
    DateTime? endDate,
    DateTime? dueDate,
    int priority = 3,
    bool isAllDay = false,
  }) async {
    try {
      final response = await _dio.post(
        '/items',
        data: {
          'calendar_id': calendarId,
          'title': title,
          'description': description,
          'type': type,
          'status': status ?? 'pending',
          'start_date': startDate?.toIso8601String(),
          'end_date': endDate?.toIso8601String(),
          'due_date': dueDate?.toIso8601String(),
          'priority': priority,
          'is_all_day': isAllDay,
        },
      );
      if (response.statusCode == 200) {
        return ScheduleItem.fromJson(response.data);
      }
    } catch (e) {
      print('Create schedule item failed: $e');
    }
    return null;
  }

  Future<ScheduleItem?> updateScheduleItem(
    int id, {
    String? title,
    String? description,
    String? type,
    String? status,
    DateTime? startDate,
    DateTime? endDate,
    DateTime? dueDate,
    int? priority,
    bool? isAllDay,
  }) async {
    try {
      final response = await _dio.put(
        '/items/$id',
        data: {
          if (title != null) 'title': title,
          if (description != null) 'description': description,
          if (type != null) 'type': type,
          if (status != null) 'status': status,
          if (startDate != null) 'start_date': startDate.toIso8601String(),
          if (endDate != null) 'end_date': endDate.toIso8601String(),
          if (dueDate != null) 'due_date': dueDate.toIso8601String(),
          if (priority != null) 'priority': priority,
          if (isAllDay != null) 'is_all_day': isAllDay,
        },
      );
      if (response.statusCode == 200) {
        return ScheduleItem.fromJson(response.data);
      }
    } catch (e) {
      print('Update schedule item failed: $e');
    }
    return null;
  }

  Future<bool> completeScheduleItem(int id) async {
    try {
      final response = await _dio.post('/items/$id/complete');
      return response.statusCode == 200;
    } catch (e) {
      print('Complete schedule item failed: $e');
      return false;
    }
  }

  Future<bool> deleteScheduleItem(int id) async {
    try {
      final response = await _dio.delete('/items/$id');
      return response.statusCode == 200;
    } catch (e) {
      print('Delete schedule item failed: $e');
      return false;
    }
  }

  // Documents
  Future<List<Document>?> getDocuments({int skip = 0, int limit = 100}) async {
    try {
      final response = await _dio.get(
        '/documents',
        queryParameters: {'skip': skip, 'limit': limit},
      );
      if (response.statusCode == 200) {
        return (response.data as List)
            .map((item) => Document.fromJson(item as Map<String, dynamic>))
            .toList();
      }
    } catch (e) {
      print('Get documents failed: $e');
    }
    return null;
  }

  Future<Document?> uploadDocument(String filePath) async {
    try {
      final file = MultipartFile.fromFileSync(filePath);
      final formData = FormData()..files.add(MapEntry('file', file));

      final response = await _dio.post(
        '/documents/upload',
        data: formData,
      );
      if (response.statusCode == 200) {
        return Document.fromJson(response.data);
      }
    } catch (e) {
      print('Upload document failed: $e');
    }
    return null;
  }

  Future<bool> deleteDocument(int id) async {
    try {
      final response = await _dio.delete('/documents/$id');
      return response.statusCode == 200;
    } catch (e) {
      print('Delete document failed: $e');
      return false;
    }
  }

  // Tags
  Future<List<Tag>?> getTags({int skip = 0, int limit = 100}) async {
    try {
      final response = await _dio.get(
        '/tags',
        queryParameters: {'skip': skip, 'limit': limit},
      );
      if (response.statusCode == 200) {
        return (response.data as List)
            .map((item) => Tag.fromJson(item as Map<String, dynamic>))
            .toList();
      }
    } catch (e) {
      print('Get tags failed: $e');
    }
    return null;
  }

  Future<Tag?> createTag({
    required String name,
    String? color,
  }) async {
    try {
      final response = await _dio.post(
        '/tags',
        data: {
          'name': name,
          'color': color,
        },
      );
      if (response.statusCode == 200) {
        return Tag.fromJson(response.data);
      }
    } catch (e) {
      print('Create tag failed: $e');
    }
    return null;
  }

  // Update headers with token
  void setAuthToken(String token) {
    _dio.options.headers['Authorization'] = 'Bearer $token';
  }

  void clearAuthToken() {
    _dio.options.headers.remove('Authorization');
  }
}

final apiService = ApiService();
