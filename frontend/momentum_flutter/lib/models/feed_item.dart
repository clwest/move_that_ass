class FeedItem {
  final int id;
  final String type;
  final String imageUrl;
  final String caption;
  int likeCount;
  bool likedByMe;

  FeedItem({
    required this.id,
    required this.type,
    required this.imageUrl,
    required this.caption,
    required this.likeCount,
    required this.likedByMe,
  });

  factory FeedItem.fromJson(Map<String, dynamic> json) {
    return FeedItem(
      id: json['id'] as int,
      type: json['type'] as String,
      imageUrl: json['image_url'] as String? ?? '',
      caption: json['caption'] as String? ?? '',
      likeCount: json['like_count'] as int? ?? 0,
      likedByMe: json['liked_by_me'] as bool? ?? false,
    );
  }
}
