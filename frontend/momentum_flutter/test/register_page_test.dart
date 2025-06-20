import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:momentum_flutter/pages/register_page.dart';
import 'package:momentum_flutter/pages/login_page.dart';
import 'package:momentum_flutter/services/auth_service.dart';

void main() {
  const MethodChannel channel = MethodChannel('plugins.flutter.io/flutter_secure_storage');
  TestWidgetsFlutterBinding.ensureInitialized();
  channel.setMockMethodCallHandler((MethodCall methodCall) async => null);

  testWidgets('Successful registration shows SnackBar and navigates to LoginPage', (tester) async {
    AuthService.register = (String email, String p1, String p2) async => true;

    await tester.pumpWidget(const MaterialApp(home: RegisterPage()));
    await tester.pump();

    await tester.enterText(find.byType(TextField).at(0), 'a@mail.com');
    await tester.enterText(find.byType(TextField).at(1), 'pass123');
    await tester.enterText(find.byType(TextField).at(2), 'pass123');
    await tester.tap(find.text('Register'));
    await tester.pump();

    expect(find.text('Registration complete. Please log in.'), findsOneWidget);
    expect(find.byType(LoginPage), findsOneWidget);
  });

  testWidgets('Error shows message text', (tester) async {
    AuthService.register = (String email, String p1, String p2) async {
      throw Exception('Email exists');
    };

    await tester.pumpWidget(const MaterialApp(home: RegisterPage()));
    await tester.pump();

    await tester.enterText(find.byType(TextField).at(0), 'a@mail.com');
    await tester.enterText(find.byType(TextField).at(1), 'pass123');
    await tester.enterText(find.byType(TextField).at(2), 'pass123');
    await tester.tap(find.text('Register'));
    await tester.pump();

    expect(find.text('Email exists'), findsOneWidget);
  });
}
