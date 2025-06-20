import 'package:flutter/material.dart';

import 'pages/today_page.dart';
import 'pages/login_page.dart';
import 'pages/profile_page.dart';
import 'pages/goal_setup_page.dart';
import 'pages/voice_journal_page.dart';
import 'pages/challenge_result_page.dart';

import 'themes/app_theme.dart';
import 'services/auth_service.dart';
import 'services/api_service.dart';
import 'services/token_service.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'config.dart';



Future<void> main({String? baseUrl}) async {
  WidgetsFlutterBinding.ensureInitialized();
  // Initialize global configuration.
  AppConfig(baseUrl: baseUrl);
  await TokenService.init();
  final prefs = await SharedPreferences.getInstance();
  final hasToken = prefs.getString('access_token') != null;
  runApp(MyApp(startAtHome: hasToken));
}

class MyApp extends StatelessWidget {
  final bool startAtHome;
  const MyApp({super.key, this.startAtHome = false});

  @override
  Widget build(BuildContext context) {

    return MaterialApp(
      title: 'MoveYourAzz',
      theme: AppTheme.theme,
      initialRoute: startAtHome ? '/today' : '/login',
      routes: {
        '/login': (_) => const LoginPage(),
        '/today': (_) => const TodayPage(),
        '/profile': (_) => const ProfilePage(),
        '/goal-setup': (_) => const GoalSetupPage(),
        VoiceJournalPage.routeName: (_) => const VoiceJournalPage(),
        ChallengeResultPage.routeName: (context) {
          final args = ModalRoute.of(context)!.settings.arguments
              as Map<String, dynamic>;
          return ChallengeResultPage(
            challengeId: args['id'] as int,
            challengeText: args['text'] as String,
          );
        },
      },
    );
  }
}
