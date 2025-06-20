class DailyGoal {
  final String goal;
  final int target;
  final String type;

  DailyGoal({required this.goal, required this.target, required this.type});

  factory DailyGoal.fromJson(Map<String, dynamic> json) {
    final goal = json['goal'] as String? ?? '';
    final target = json['target'] is int
        ? json['target'] as int
        : int.tryParse(json['target'].toString()) ?? 0;
    final type = json['type'] as String? ?? 'daily';
    return DailyGoal(goal: goal, target: target, type: type);
  }
}
