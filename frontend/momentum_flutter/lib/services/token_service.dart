import 'package:shared_preferences/shared_preferences.dart';

class TokenService {
  static const _kAccess = 'access_token';
  static const _kRefresh = 'refresh_token';
  static String? _access;
  static String? _refresh;

  /// Load tokens from SharedPreferences into memory.
  static Future<void> init() async {
    final prefs = await SharedPreferences.getInstance();
    _access = prefs.getString(_kAccess);
    _refresh = prefs.getString(_kRefresh);
  }

  static String? get accessToken => _access;
  static String? get refreshToken => _refresh;

  /// Persist tokens to storage and update cache.
  static Future<void> save(String access, String refresh) async {
    _access = access;
    _refresh = refresh;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_kAccess, access);
    await prefs.setString(_kRefresh, refresh);
  }

  /// Clear tokens from storage and cache.
  static Future<void> clear() async {
    _access = null;
    _refresh = null;
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_kAccess);
    await prefs.remove(_kRefresh);
  }
}
