class Meme {
  final String imageUrl;
  final String caption;
  final String tone;

  Meme({required this.imageUrl, required this.caption, required this.tone});

  factory Meme.fromJson(Map<String, dynamic> json) {
    final imageUrl = json['image_url'] as String? ?? '';
    final caption = json['caption'] as String? ?? '';
    final tone = json['tone'] as String? ?? 'funny';
    return Meme(imageUrl: imageUrl, caption: caption, tone: tone);
  }
}
