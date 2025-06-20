class DashboardItem {
  final String type;
  final DateTime createdAt;
  final Map<String, dynamic> content;

  DashboardItem({
    required this.type,
    required this.createdAt,
    required this.content,
  });

  factory DashboardItem.fromJson(Map<String, dynamic> json) {
    return DashboardItem(
      type: json['type'] as String,
      createdAt: DateTime.parse(json['created_at'] as String),
      content: json['content'] as Map<String, dynamic>? ?? {},
    );
  }
}
