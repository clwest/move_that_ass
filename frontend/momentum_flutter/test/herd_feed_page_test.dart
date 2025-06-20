import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:momentum_flutter/pages/herd_feed_page.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  SharedPreferences.setMockInitialValues({});

  testWidgets('HerdFeedPage has title', (WidgetTester tester) async {
    await tester.pumpWidget(const MaterialApp(home: HerdFeedPage()));
    await tester.pump();

    expect(find.text('Herd Feed 🫏'), findsOneWidget);
  });
}
