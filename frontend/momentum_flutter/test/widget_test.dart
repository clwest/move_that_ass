import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:momentum_flutter/main.dart';
import 'package:momentum_flutter/models/meme.dart';
import 'package:momentum_flutter/pages/meme_share_page.dart';

void main() {
  testWidgets('TodayPage loads', (WidgetTester tester) async {
    await tester.pumpWidget(const MyApp());

    expect(find.text('MoveYourAzz 🫏'), findsOneWidget);
    expect(find.byType(ListView), findsOneWidget);
  });

  testWidgets('MemeSharePage shows caption and image', (tester) async {
    final meme = Meme(
      imageUrl: 'https://example.com/meme.png',
      caption: 'funny caption',
      tone: 'funny',
    );

    await tester.pumpWidget(
      MaterialApp(
        home: MemeSharePage(meme: meme),
      ),
    );

    expect(find.text('funny caption'), findsOneWidget);
    expect(find.byType(Image), findsOneWidget);
  });
}
