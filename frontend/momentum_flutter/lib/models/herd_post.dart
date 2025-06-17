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
    return HerdPost(
      type: json['type'] as String,
      user: json['user'] as String,
      content: json['content'] as Map<String, dynamic>? ?? {},
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }
}
