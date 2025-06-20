import 'package:flutter/material.dart';

import '../services/api_service.dart';
import '../pages/profile_page.dart';
import '../pages/goal_setup_page.dart';
import '../pages/today_page.dart';

/// Determines the correct landing page after authentication and
/// navigates there by replacing the current route.
Future<void> navigateToAppHome(BuildContext context) async {
  final profile = await ApiService.fetchProfile();
  if (!context.mounted) return;
  if (profile.displayName.isEmpty) {
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (_) => const ProfilePage()),
    );
    return;
  }

  final goal = await ApiService.fetchDailyGoal();
  if (!context.mounted) return;
  if (goal == null) {
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (_) => const GoalSetupPage()),
    );
    return;
  }

  Navigator.pushReplacement(
    context,
    MaterialPageRoute(builder: (_) => const TodayPage()),
  );
}
