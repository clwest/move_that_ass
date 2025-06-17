import 'package:flutter/material.dart';

import 'pages/today_page.dart';
import 'pages/login_page.dart';
import 'pages/profile_page.dart';
import 'pages/goal_setup_page.dart';
import 'themes/app_theme.dart';
import 'services/token_service.dart';
import 'services/api_service.dart';
import 'package:shared_preferences/shared_preferences.dart';


void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Map<String, dynamic>>(
      future: _determineStart(),
      builder: (context, snapshot) {
        if (!snapshot.hasData) {
          return const MaterialApp(
            home: Scaffold(
              body: Center(child: CircularProgressIndicator()),
            ),
          );
        }
        final data = snapshot.data!;
        final Widget home = data['page'] as Widget;
        final bool showWelcome = data['welcome'] as bool? ?? false;

        return MaterialApp(
          title: 'MoveYourAzz',
          theme: AppTheme.theme,
          home: _HomeWrapper(child: home, showWelcome: showWelcome),
        );
      },
    );
  }

  Future<Map<String, dynamic>> _determineStart() async {
    final loggedIn = await TokenService.isAuthenticated();
    if (!loggedIn) {
      return {'page': const LoginPage(), 'welcome': false};
    }

    final profile = await ApiService.fetchProfile();
    if (profile.displayName.isEmpty) {
      return {'page': const ProfilePage(), 'welcome': false};
    }

    final goal = await ApiService.getDailyGoal();
    if (goal == null) {
      return {'page': const GoalSetupPage(), 'welcome': false};
    }

    final prefs = await SharedPreferences.getInstance();
    final showWelcome = !(prefs.getBool('welcome_shown') ?? false);
    if (showWelcome) {
      await prefs.setBool('welcome_shown', true);
    }

    return {'page': const TodayPage(), 'welcome': showWelcome};
  }
}

class _HomeWrapper extends StatefulWidget {
  final Widget child;
  final bool showWelcome;
  const _HomeWrapper({required this.child, required this.showWelcome});

  @override
  State<_HomeWrapper> createState() => _HomeWrapperState();
}

class _HomeWrapperState extends State<_HomeWrapper> {
  @override
  void initState() {
    super.initState();
    if (widget.showWelcome) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        showDialog(
          context: context,
          builder: (_) => AlertDialog(
            title: const Text('Welcome to MoveYourAzz 🫏'),
            content: const Text("Let's get that azz moving!"),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(context),
                child: const Text('OK'),
              ),
            ],
          ),
        );
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return widget.child;
  }
}
