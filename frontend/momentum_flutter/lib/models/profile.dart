class UserProfile {
  final String username;
  final String displayName;
  final String mood;
  final String moodAvatar;
  final String? herdName;
  final int herdSize;
  final int badges;

  UserProfile({
    required this.username,
    required this.displayName,
    required this.mood,
    required this.moodAvatar,
    required this.herdName,
    required this.herdSize,
    required this.badges,
  });

  factory UserProfile.fromJson(Map<String, dynamic> json) {
    final username = json['username'] as String? ?? '';
    final displayName = json['display_name'] as String? ?? '';
    final mood = json['mood'] as String? ?? '';
    final moodAvatar = json['mood_avatar'] as String? ?? '';
    final herdName = json['herd_name'] as String?;
    final herdSize = json['herd_size'] is int
        ? json['herd_size'] as int
        : int.tryParse(json['herd_size'].toString()) ?? 0;
    final badges = json['badges'] is int
        ? json['badges'] as int
        : int.tryParse(json['badges'].toString()) ?? 0;
    return UserProfile(
      username: username,
      displayName: displayName,
      mood: mood,
      moodAvatar: moodAvatar,
      herdName: herdName,
      herdSize: herdSize,
      badges: badges,
    );
  }
}
