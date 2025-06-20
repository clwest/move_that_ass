import 'package:flutter/foundation.dart';

class Challenge {
  final int id;
  final String text;
  final DateTime expiresAt;

  Challenge({required this.id, required this.text, required this.expiresAt});

  factory Challenge.fromJson(Map<String, dynamic> json) {
    return Challenge(
      id: json['id'] as int,
      text: json['text'] as String,
      expiresAt: DateTime.parse(json['expires_at'] as String),
    );
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
    return TodayDashboard(
      mood: json['mood'] as String,
      moodAvatar: json['mood_avatar'] as String? ?? '',
      challenge: json['challenge'] != null ? Challenge.fromJson(json['challenge'] as Map<String, dynamic>) : null,
      workoutPlan: (json['workout_plan'] as List?)?.map((e) => e.toString()).toList(),
      mealPlan: json['meal_plan'] as Map<String, dynamic>?,
      recap: json['azz_recap'] as String? ?? '',
    );
  }
}
