import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:momentum_flutter/pages/today_page.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  SharedPreferences.setMockInitialValues({});

  testWidgets('TodayPage renders basic widgets', (WidgetTester tester) async {
    await tester.pumpWidget(const MaterialApp(home: TodayPage()));
    await tester.pump();

    expect(find.text('MoveYourAzz 🫏'), findsOneWidget);
    expect(find.byType(FloatingActionButton), findsOneWidget);
  });
}
