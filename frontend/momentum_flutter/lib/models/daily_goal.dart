class DailyGoal {
  final String goal;
  final int target;
  final String type;

  DailyGoal({required this.goal, required this.target, required this.type});

  factory DailyGoal.fromJson(Map<String, dynamic> json) {
    return DailyGoal(
      goal: json['goal'] as String,
      target: json['target'] as int,
      type: json['type'] as String? ?? 'daily',
    );
  }
}
