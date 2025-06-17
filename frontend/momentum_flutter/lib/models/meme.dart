class Meme {
  final String imageUrl;
  final String caption;
  final String tone;

  Meme({required this.imageUrl, required this.caption, required this.tone});

  factory Meme.fromJson(Map<String, dynamic> json) {
    return Meme(
      imageUrl: json['image_url'] as String,
      caption: json['caption'] as String,
      tone: json['tone'] as String? ?? 'funny',
    );
  }
}
