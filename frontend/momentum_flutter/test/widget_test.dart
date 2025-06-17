import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:momentum_flutter/main.dart';

void main() {
  testWidgets('TodayPage loads', (WidgetTester tester) async {
    await tester.pumpWidget(const MyApp());

    expect(find.text('MoveYourAzz 🫏'), findsOneWidget);
    expect(find.byType(ListView), findsOneWidget);
  });
}
