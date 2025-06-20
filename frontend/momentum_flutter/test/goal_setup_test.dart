import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:momentum_flutter/main.dart';
import 'package:momentum_flutter/pages/goal_setup_page.dart';
import 'package:momentum_flutter/pages/today_page.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  SharedPreferences.setMockInitialValues({});

  testWidgets('Saving goal navigates to TodayPage', (WidgetTester tester) async {
    final server = await HttpServer.bind(InternetAddress.loopbackIPv4, 0);

    server.listen((HttpRequest request) async {
      final path = request.uri.path;
      if (path == '/api/auth/login/') {
        request.response
          ..statusCode = 200
          ..headers.contentType = ContentType.json
          ..write('{"access":"tok","refresh":"ref"}');
      } else if (path == '/api/core/profile/' || path == '/api/core/profiles/') {
        request.response
          ..statusCode = 200
          ..headers.contentType = ContentType.json
          ..write('{"username":"a","display_name":"A","mood":"","mood_avatar":""}');
      } else if (path == '/api/core/daily-goal/' && request.method == 'GET') {
        request.response.statusCode = 404;
      } else if (path == '/api/core/daily-goal/' && request.method == 'POST') {
        request.response
          ..statusCode = 201
          ..headers.contentType = ContentType.json
          ..write('{"goal":"walk","target":1,"type":"daily"}');
      } else if (path == '/api/core/dashboard/') {
        request.response
          ..statusCode = 200
          ..headers.contentType = ContentType.json
          ..write('{"mood":"happy","mood_avatar":"","challenge":null,"workout_plan":null,"meal_plan":null,"recap":""}');
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

    expect(find.byType(GoalSetupPage), findsOneWidget);

    await tester.enterText(find.byType(TextField).at(0), 'walk');
    await tester.tap(find.text('Save Goal'));
    await tester.pumpAndSettle();

    expect(find.byType(TodayPage), findsOneWidget);
    expect(find.textContaining("Today's goal"), findsOneWidget);

    await server.close(force: true);
  });
}
