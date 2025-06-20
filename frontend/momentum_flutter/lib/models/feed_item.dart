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
    final id = json['id'] is int
        ? json['id'] as int
        : int.tryParse(json['id'].toString()) ?? 0;
    final type = json['type'] as String? ?? '';
    final imageUrl = json['image_url'] as String? ?? '';
    final caption = json['caption'] as String? ?? '';
    final likeCount = json['like_count'] is int
        ? json['like_count'] as int
        : int.tryParse(json['like_count'].toString()) ?? 0;
    final likedByMe = json['liked_by_me'] as bool? ?? false;
    return FeedItem(
      id: id,
      type: type,
      imageUrl: imageUrl,
      caption: caption,
      likeCount: likeCount,
      likedByMe: likedByMe,
    );
  }
}
