import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:momentum_flutter/main.dart';
import 'package:momentum_flutter/pages/today_page.dart';

void main() {
  const MethodChannel channel = MethodChannel('plugins.flutter.io/flutter_secure_storage');
  TestWidgetsFlutterBinding.ensureInitialized();
  channel.setMockMethodCallHandler((MethodCall methodCall) async {
    return null;
  });

  testWidgets('Login navigates to TodayPage on success', (WidgetTester tester) async {
    final server = await HttpServer.bind(InternetAddress.loopbackIPv4, 0);

    server.listen((HttpRequest request) async {
      if (request.uri.path == '/api/auth/login/') {
        request.response
          ..statusCode = 200
          ..headers.contentType = ContentType.json
          ..write('{"access":"tok","refresh":"ref"}');
      } else if (request.uri.path == '/api/core/profiles/') {
        request.response
          ..statusCode = 200
          ..headers.contentType = ContentType.json
          ..write('{"email":"a@example.com","is_verified":true,"date_joined":"2024-01-01"}');
      } else if (request.uri.path == '/api/core/daily-goal/') {
        request.response
          ..statusCode = 200
          ..headers.contentType = ContentType.json
          ..write('{"goal":"walk","target":1,"type":"daily"}');
      } else {
        request.response.statusCode = 404;
      }
      await request.response.close();
    });

    final baseUrl = 'http://localhost:${server.port}';
    main(baseUrl: baseUrl);

    await tester.pumpWidget(const MyApp());
    await tester.pump();

    await tester.enterText(find.byType(TextField).at(0), 'a@example.com');
    await tester.enterText(find.byType(TextField).at(1), 'secret');
    await tester.tap(find.text('Login'));
    await tester.pumpAndSettle();

    expect(find.byType(TodayPage), findsOneWidget);

    await server.close(force: true);
  });
}
