import 'package:flutter/foundation.dart';

class Challenge {
  final int id;
  final String text;
  final DateTime expiresAt;

  Challenge({required this.id, required this.text, required this.expiresAt});

  factory Challenge.fromJson(Map<String, dynamic> json) {
    final id = json['id'] as int? ?? 0;
    final text = json['text'] as String? ?? '';
    final expiresRaw = json['expires_at'] as String? ?? '';
    final expiresAt = DateTime.tryParse(expiresRaw) ?? DateTime.now();
    return Challenge(id: id, text: text, expiresAt: expiresAt);
  }
}

class TodayDashboard {
  final String mood;
  final String moodAvatar;
  final Challenge? challenge;
  final List<String>? workoutPlan;
  final Map<String, dynamic>? mealPlan;
  final String recap;

  TodayDashboard({
    required this.mood,
    required this.moodAvatar,
    required this.challenge,
    required this.workoutPlan,
    required this.mealPlan,
    required this.recap,
  });

  factory TodayDashboard.fromJson(Map<String, dynamic> json) {
    final mood = json['mood'] as String? ?? '';
    final moodAvatar = json['mood_avatar'] as String? ?? '';
    final challenge = json['challenge'] != null
        ? Challenge.fromJson(json['challenge'] as Map<String, dynamic>)
        : null;
    final workoutPlan =
        (json['workout_plan'] as List?)?.map((e) => e.toString()).toList();
    final mealPlan = json['meal_plan'] as Map<String, dynamic>?;
    final recap = json['azz_recap'] as String? ?? '';
    return TodayDashboard(
      mood: mood,
      moodAvatar: moodAvatar,
      challenge: challenge,
      workoutPlan: workoutPlan,
      mealPlan: mealPlan,
      recap: recap,
    );
  }
}
