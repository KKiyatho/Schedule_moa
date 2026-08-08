import 'package:dio/dio.dart';

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

  // Auth
  Future<String?> register({
    required String email,
    String? fullName,
  }) async {
    try {
      final response = await _dio.post(
        '/auth/register',
        data: {
          'email': email,
          'full_name': fullName,
        },
      );
      if (response.statusCode == 200) {
        return response.data['access_token'];
      }
    } catch (e) {
      print('Register failed: $e');
    }
    return null;
  }

  Future<String?> login({
    required String email,
    required String password,
  }) async {
    try {
      final response = await _dio.post(
        '/auth/login',
        queryParameters: {
          'email': email,
          'password': password,
        },
      );
      if (response.statusCode == 200) {
        return response.data['access_token'];
      }
    } catch (e) {
      print('Login failed: $e');
    }
    return null;
  }

  // Documents
  Future<List<dynamic>?> getDocuments() async {
    try {
      final response = await _dio.get('/documents/');
      if (response.statusCode == 200) {
        return response.data;
      }
    } catch (e) {
      print('Get documents failed: $e');
    }
    return null;
  }

  // Items
  Future<List<dynamic>?> getItems({String? itemType}) async {
    try {
      final response = await _dio.get(
        '/items/',
        queryParameters: {
          if (itemType != null) 'item_type': itemType,
        },
      );
      if (response.statusCode == 200) {
        return response.data;
      }
    } catch (e) {
      print('Get items failed: $e');
    }
    return null;
  }

  // Update headers with token
  void setAuthToken(String token) {
    _dio.options.headers['Authorization'] = 'Bearer $token';
  }
}

final apiService = ApiService();
