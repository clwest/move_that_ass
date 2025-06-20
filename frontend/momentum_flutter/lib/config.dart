import 'dart:io' show Platform;
import 'package:flutter/foundation.dart';

class AppConfig {
  /// Base URL for all API calls.
  ///
  /// The value is resolved in the following order:
  /// 1. The [baseUrl] provided to the constructor.
  /// 2. The compile-time environment variable `API_BASE_URL` supplied via
  ///    `--dart-define`.
  /// 3. Defaults to `http://localhost:8000` (or `http://10.0.2.2:8000` on the
  ///    Android emulator).
  AppConfig({String? baseUrl}) {
    final envBaseUrl = const String.fromEnvironment('API_BASE_URL');
    AppConfig.baseUrl =
        baseUrl ?? (envBaseUrl.isNotEmpty ? envBaseUrl : _defaultBaseUrl);
  }

  static String get _defaultBaseUrl {
    if (!kIsWeb && Platform.isAndroid) {
      // 'localhost' refers to the device itself when running on the Android
      // emulator. `10.0.2.2` routes to the host machine instead.
      return 'http://10.0.2.2:8000';
    }
    return 'http://localhost:8000';
  }

  /// Current API base URL used throughout the application.
  static late String baseUrl;
}
