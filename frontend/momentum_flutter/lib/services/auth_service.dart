import 'dart:convert';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;

import '../config.dart';

class AuthService {
  static final _storage = const FlutterSecureStorage();
  static http.Client client = http.Client();
  static const _accessKey = 'access_token';
  static const _refreshKey = 'refresh_token';
  static String? _access;
  static String? _refresh;

  static String get _baseUrl => AppConfig.baseUrl;

  static Future<void> login(String identifier, String password) async {
    final response = await client.post(
      Uri.parse('$_baseUrl/api/auth/login/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'username': identifier,
        'email': identifier,
        'password': password,
      }),
    );
    if (response.statusCode != 200) {
      throw Exception('Login failed');
    }
    final data = jsonDecode(response.body) as Map<String, dynamic>;
    _access = data['access'] as String?;
    _refresh = data['refresh'] as String?;
    if (_access == null || _refresh == null) {
      throw Exception('Invalid response');
    }
    await _storage.write(key: _accessKey, value: _access);
    await _storage.write(key: _refreshKey, value: _refresh);
  }

  static Future<bool> register(
      String username, String email, String p1, String p2) async {
    final response = await client.post(
      Uri.parse('$_baseUrl/api/auth/registration/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'username': username,
        'email': email,
        'password1': p1,
        'password2': p2,
      }),
    );
    if (response.statusCode == 201) {
      return true;
    }
    try {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      final firstError = data.values.first;
      throw Exception(firstError is List ? firstError.first : firstError.toString());
    } catch (_) {
      throw Exception('Registration failed');
    }
  }

  static Future<void> logout() async {
    final refresh = await getRefreshToken();
    if (refresh != null) {
      await client.post(
        Uri.parse('$_baseUrl/api/auth/logout/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'refresh': refresh}),
      );
    }
    await clearTokens();
  }

  static Future<String?> getAccessToken() async {
    if (_access != null) return _access;
    _access = await _storage.read(key: _accessKey);
    return _access;
  }

  static Future<String?> getRefreshToken() async {
    if (_refresh != null) return _refresh;
    _refresh = await _storage.read(key: _refreshKey);
    return _refresh;
  }

  static Future<void> clearTokens() async {
    _access = null;
    _refresh = null;
    await _storage.delete(key: _accessKey);
    await _storage.delete(key: _refreshKey);
  }

  static Future<Map<String, String>> authHeaders() async {
    final token = await getAccessToken();
    if (token == null) return {};
    return {'Authorization': 'Bearer $token'};
  }

  static Future<bool> isAuthenticated() async =>
      (await getAccessToken()) != null;
}
