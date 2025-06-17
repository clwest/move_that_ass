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
    return UserProfile(
      username: json['username'] as String,
      displayName: json['display_name'] as String? ?? '',
      mood: json['mood'] as String? ?? '',
      moodAvatar: json['mood_avatar'] as String? ?? '',
      herdName: json['herd_name'] as String?,
      herdSize: json['herd_size'] as int? ?? 0,
      badges: json['badges'] as int? ?? 0,
    );
  }
}
