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
    return Badge(
      code: json['code'] as String,
      name: json['name'] as String,
      emoji: json['emoji'] as String? ?? '',
      description: json['description'] as String? ?? '',
      isEarned: json['is_earned'] as bool? ?? false,
      earnedAt: json['earned_at'] as String?,
    );
  }
}
