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
    final type = json['type'] as String? ?? '';
    final createdRaw = json['created_at'] as String? ?? '';
    final createdAt = DateTime.tryParse(createdRaw) ?? DateTime.now();
    return DashboardItem(
      type: type,
      createdAt: createdAt,
      content: json['content'] as Map<String, dynamic>? ?? {},
    );
  }
}
