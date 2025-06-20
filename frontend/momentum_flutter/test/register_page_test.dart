import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:momentum_flutter/pages/register_page.dart';
import 'package:momentum_flutter/pages/login_page.dart';
import 'package:momentum_flutter/services/auth_service.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  SharedPreferences.setMockInitialValues({});

  testWidgets('Successful registration shows SnackBar and navigates to LoginPage', (tester) async {
    AuthService.register = (String u, String e, String p1, String p2) async => true;

    await tester.pumpWidget(const MaterialApp(home: RegisterPage()));
    await tester.pump();

    await tester.enterText(find.byType(TextField).at(0), 'tester');
    await tester.enterText(find.byType(TextField).at(1), 'a@mail.com');
    await tester.enterText(find.byType(TextField).at(2), 'pass123');
    await tester.enterText(find.byType(TextField).at(3), 'pass123');
    await tester.tap(find.text('Register'));
    await tester.pump();

    expect(find.text('Registration complete. Please log in.'), findsOneWidget);
    expect(find.byType(LoginPage), findsOneWidget);
  });

  testWidgets('Error shows message text', (tester) async {
    AuthService.register = (String u, String e, String p1, String p2) async {
      throw Exception('Email exists');
    };

    await tester.pumpWidget(const MaterialApp(home: RegisterPage()));
    await tester.pump();

    await tester.enterText(find.byType(TextField).at(0), 'tester');
    await tester.enterText(find.byType(TextField).at(1), 'a@mail.com');
    await tester.enterText(find.byType(TextField).at(2), 'pass123');
    await tester.enterText(find.byType(TextField).at(3), 'pass123');
    await tester.tap(find.text('Register'));
    await tester.pump();

    expect(find.text('Email exists'), findsOneWidget);
  });
}
