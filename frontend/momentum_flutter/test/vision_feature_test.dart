import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:image_picker/image_picker.dart';
import 'package:momentum_flutter/pages/today_page.dart';
import 'package:momentum_flutter/services/task_poller.dart';
import 'package:momentum_flutter/services/api_service.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  SharedPreferences.setMockInitialValues({});

  testWidgets('Vision flow shows result sheet', (WidgetTester tester) async {
    TestWidgetsFlutterBinding.ensureInitialized();
    final pickerChannel = const MethodChannel('plugins.flutter.io/image_picker');
    pickerChannel.setMockMethodCallHandler((MethodCall methodCall) async {
      return '/tmp/test.jpg';
    });

    TaskPoller.poll = (String id, {Duration interval = const Duration(seconds: 2)}) async {
      return {
        'state': 'SUCCESS',
        'data': jsonEncode({'label':'oak leaf','is_dangerous':false,'wiki_url':'http://wiki'})
      };
    };

    ApiService.uploadImage = (String url, XFile file) async => '123';

    await tester.pumpWidget(const MaterialApp(home: TodayPage()));
    await tester.pump();

    await tester.tap(find.byIcon(Icons.camera_alt));
    await tester.pumpAndSettle();

    expect(find.text('🏷  Name: oak leaf'), findsOneWidget);
    expect(find.text('☠️ Dangerous: No'), findsOneWidget);
    expect(find.text('🔗 Wikipedia'), findsOneWidget);
  });
}
