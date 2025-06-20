import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:momentum_flutter/pages/profile_page.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  SharedPreferences.setMockInitialValues({});

  testWidgets('ProfilePage shows header text', (WidgetTester tester) async {
    await tester.pumpWidget(const MaterialApp(home: ProfilePage()));
    await tester.pump();

    expect(find.text('My Profile 🫏'), findsOneWidget);
  });
}
