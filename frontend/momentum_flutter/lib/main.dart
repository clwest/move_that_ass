import 'package:flutter/material.dart';

import 'pages/today_page.dart';
import 'pages/login_page.dart';
import 'themes/app_theme.dart';
import 'services/token_service.dart';


void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<bool>(
      future: TokenService.isAuthenticated(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const MaterialApp(
            home: Scaffold(
              body: Center(child: CircularProgressIndicator()),
            ),
          );
        }
        final loggedIn = snapshot.data == true;
        return MaterialApp(
          title: 'MoveYourAzz',
          theme: AppTheme.theme,
          home: loggedIn ? const TodayPage() : const LoginPage(),
        );
      },
    );
  }
}
