import 'dart:io';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:momentum_flutter/services/api_service.dart';
import 'package:momentum_flutter/config.dart';

void main() {
  const MethodChannel channel = MethodChannel('plugins.flutter.io/flutter_secure_storage');
  TestWidgetsFlutterBinding.ensureInitialized();
  channel.setMockMethodCallHandler((MethodCall methodCall) async => null);

  test('ApiService.shareBadge returns 201', () async {
    final server = await HttpServer.bind(InternetAddress.loopbackIPv4, 0);
    server.listen((HttpRequest request) async {
      if (request.method == 'POST' && request.uri.path == '/api/core/share-badge/') {
        request.response
          ..statusCode = 201
          ..headers.contentType = ContentType.json
          ..write('{"message":"shared"}');
      } else {
        request.response.statusCode = 404;
      }
      await request.response.close();
    });

    AppConfig(baseUrl: 'http://localhost:${server.port}');
    final msg = await ApiService.shareBadge('abc');
    expect(msg, 'shared');
    await server.close(force: true);
  });
}
