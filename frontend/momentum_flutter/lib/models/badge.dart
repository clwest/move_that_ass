class Badge {
  final String code;
  final String name;
  final String emoji;
  final String description;
  final bool isEarned;
  final String? earnedAt;

  Badge({
    required this.code,
    required this.name,
    required this.emoji,
    required this.description,
    required this.isEarned,
    this.earnedAt,
  });

  factory Badge.fromJson(Map<String, dynamic> json) {
    final code = json['code'] as String? ?? '';
    final name = json['name'] as String? ?? '';
    final emoji = json['emoji'] as String? ?? '';
    final description = json['description'] as String? ?? '';
    final isEarned = json['is_earned'] as bool? ?? false;
    final earnedAt = json['earned_at'] as String?;
    return Badge(
      code: code,
      name: name,
      emoji: emoji,
      description: description,
      isEarned: isEarned,
      earnedAt: earnedAt,
    );
  }
}
