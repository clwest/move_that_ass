import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:momentum_flutter/pages/today_page.dart';

void main() {
  const MethodChannel channel = MethodChannel('plugins.flutter.io/flutter_secure_storage');
  TestWidgetsFlutterBinding.ensureInitialized();
  channel.setMockMethodCallHandler((MethodCall methodCall) async {
    return null;
  });

  testWidgets('TodayPage renders basic widgets', (WidgetTester tester) async {
    await tester.pumpWidget(const MaterialApp(home: TodayPage()));
    await tester.pump();

    expect(find.text('MoveYourAzz 🫏'), findsOneWidget);
    expect(find.byType(FloatingActionButton), findsOneWidget);
  });
}
