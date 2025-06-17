import 'package:flutter/material.dart';

import 'pages/today_page.dart';
import 'pages/login_page.dart';
import 'pages/profile_page.dart';
import 'pages/goal_setup_page.dart';

import 'themes/app_theme.dart';
import 'services/token_service.dart';
import 'services/api_service.dart';
import 'config.dart';



void main({String? baseUrl}) {
  // Initialize global configuration.
  AppConfig(baseUrl: baseUrl);
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {

    return FutureBuilder<Widget>(
      future: _determineHome(),

      builder: (context, snapshot) {
        if (!snapshot.hasData) {
          return const MaterialApp(
            home: Scaffold(
              body: Center(child: CircularProgressIndicator()),
            ),
          );
        }

        return MaterialApp(
          title: 'MoveYourAzz',
          theme: AppTheme.theme,
          home: snapshot.data!,
        );
      },
    );
  }

  Future<Widget> _determineHome() async {
    final loggedIn = await TokenService.isAuthenticated();
    if (!loggedIn) return const LoginPage();

    final profile = await ApiService.fetchProfile();
    if (profile.displayName.isEmpty) return const ProfilePage();

    final goal = await ApiService.fetchDailyGoal();
    if (goal == null) return const GoalSetupPage();

    return const TodayPage();


  }
}
