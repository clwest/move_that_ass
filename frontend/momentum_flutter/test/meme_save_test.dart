import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:momentum_flutter/models/meme.dart';
import 'package:momentum_flutter/pages/meme_share_page.dart';

void main() {
  const MethodChannel galleryChannel = MethodChannel('plugins.flutter.io/gallery_saver');
  TestWidgetsFlutterBinding.ensureInitialized();
  galleryChannel.setMockMethodCallHandler((MethodCall methodCall) async {
    if (methodCall.method == 'saveImage') {
      return true;
    }
    return null;
  });

  testWidgets('Successful meme save shows SnackBar', (WidgetTester tester) async {
    const meme = Meme(imageUrl: 'http://example.com/img', caption: 'hi', tone: 'funny');
    await tester.pumpWidget(const MaterialApp(home: MemeSharePage(meme: meme)));
    await tester.pump();

    await tester.tap(find.textContaining('Save to Device'));
    await tester.pump();

    expect(find.text('Meme saved 🎉'), findsOneWidget);
  });
}
