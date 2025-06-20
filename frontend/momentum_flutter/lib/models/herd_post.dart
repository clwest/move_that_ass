class HerdPost {
  final String type;
  final String user;
  final Map<String, dynamic> content;
  final DateTime createdAt;

  HerdPost({
    required this.type,
    required this.user,
    required this.content,
    required this.createdAt,
  });

  factory HerdPost.fromJson(Map<String, dynamic> json) {
    final type = json['type'] as String? ?? '';
    final user = json['user'] as String? ?? '';
    final createdRaw = json['created_at'] as String? ?? '';
    final createdAt = DateTime.tryParse(createdRaw) ?? DateTime.now();
    return HerdPost(
      type: type,
      user: user,
      content: json['content'] as Map<String, dynamic>? ?? {},
      createdAt: createdAt,
    );
  }
}
