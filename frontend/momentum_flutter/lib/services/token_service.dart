import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class TokenService {
  static final _storage = const FlutterSecureStorage();
  static const _tokenKey = 'auth_token';
  static String? _cachedToken;

  static Future<void> saveToken(String token) async {
    _cachedToken = token;
    await _storage.write(key: _tokenKey, value: token);
  }

  static Future<String?> getToken() async {
    if (_cachedToken != null) return _cachedToken;
    _cachedToken = await _storage.read(key: _tokenKey);
    return _cachedToken;
  }

  static Future<void> clearToken() async {
    _cachedToken = null;
    await _storage.delete(key: _tokenKey);
  }

  static Future<bool> isAuthenticated() async {
    final token = await getToken();
    return token != null && token.isNotEmpty;
  }
}
