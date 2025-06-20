import 'dart:convert';
import 'package:http/http.dart' as http;

import '../config.dart';
import 'token_service.dart';

class AuthService {
  static http.Client client = http.Client();

  static String get _baseUrl => AppConfig.baseUrl;

  static Future<void> login(String username, String password) async {
    final response = await client.post(
      Uri.parse('$_baseUrl/api/auth/login/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'username': username, 'password': password}),
    );
    if (response.statusCode != 200) {
      throw Exception('Login failed');
    }
    final data = jsonDecode(response.body) as Map<String, dynamic>;
    final access = data['access'] as String?;
    final refresh = data['refresh'] as String?;
    if (access == null || refresh == null) {
      throw Exception('Invalid response');
    }
    await TokenService.save(access, refresh);
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
    final refresh = TokenService.refreshToken;
    if (refresh != null) {
      await client.post(
        Uri.parse('$_baseUrl/api/auth/logout/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'refresh': refresh}),
      );
    }
    await TokenService.clear();
  }

  static Map<String, String> authHeaders() {
    final token = TokenService.accessToken;
    if (token == null) return {};
    return {'Authorization': 'Bearer $token'};
  }

  static bool get isAuthenticated => TokenService.accessToken != null;

  static Future<bool> refresh() async {
    final refresh = TokenService.refreshToken;
    if (refresh == null) return false;
    final res = await client.post(
      Uri.parse('$_baseUrl/api/auth/token/refresh/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'refresh': refresh}),
    );
    if (res.statusCode != 200) return false;
    final data = jsonDecode(res.body) as Map<String, dynamic>;
    final access = data['access'] as String?;
    final newRefresh = data['refresh'] as String? ?? refresh;
    if (access == null) return false;
    await TokenService.save(access, newRefresh);
    return true;
  }
}
