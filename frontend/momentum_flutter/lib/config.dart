class AppConfig {
  /// Base URL for all API calls.
  ///
  /// The value is resolved in the following order:
  /// 1. The [baseUrl] provided to the constructor.
  /// 2. The compile-time environment variable `API_BASE_URL` supplied via
  ///    `--dart-define`.
  /// 3. Defaults to `http://localhost:8000`.
  AppConfig({String? baseUrl}) {
    AppConfig.baseUrl = baseUrl ??
        const String.fromEnvironment('API_BASE_URL',
            defaultValue: 'http://localhost:8000');
  }

  /// Current API base URL used throughout the application.
  static late String baseUrl;
}
