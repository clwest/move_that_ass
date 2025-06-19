import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'auth_service.dart';
import '../config.dart';

import '../models/today_dashboard.dart';
import '../models/badge.dart';
import '../models/meme.dart';
import '../models/herd_post.dart';
import '../models/profile.dart';
import '../models/daily_goal.dart';

class ApiService {
  static String get baseUrl => AppConfig.baseUrl;

  static Future<TodayDashboard> fetchTodayDashboard() async {
    final headers = {'Content-Type': 'application/json'};
    headers.addAll(await AuthService.authHeaders());

    final response = await http.get(
      Uri.parse('$baseUrl/api/core/dashboard-today/'),
      headers: headers,
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to load dashboard');
    }

    final data = json.decode(response.body) as Map<String, dynamic>;
    return TodayDashboard.fromJson(data);
  }

  static Future<List<Badge>> fetchBadges() async {
    final headers = {'Content-Type': 'application/json'};
    headers.addAll(await AuthService.authHeaders());
    // ensure badges are evaluated on the server
    await http.get(
      Uri.parse('$baseUrl/api/core/check-badges/'),
      headers: headers,
    );

    final response = await http.get(
      Uri.parse('$baseUrl/api/core/badges/'),
      headers: headers,
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to load badges');
    }

    final List data = json.decode(response.body) as List;
    return data.map((e) => Badge.fromJson(e as Map<String, dynamic>)).toList();
  }

  static Future<List<HerdPost>> fetchHerdFeed() async {
    final headers = {'Content-Type': 'application/json'};
    headers.addAll(await AuthService.authHeaders());

    final response = await http.get(
      Uri.parse('$baseUrl/api/core/herd-feed/'),
      headers: headers,
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to load herd feed');
    }

    final List data = json.decode(response.body) as List;
    return data.map((e) => HerdPost.fromJson(e as Map<String, dynamic>)).toList();
  }

  static Future<UserProfile> fetchProfile() async {
    final headers = {'Content-Type': 'application/json'};
    headers.addAll(await AuthService.authHeaders());

    final response = await http.get(
      Uri.parse('$baseUrl/api/core/profiles/'),
      headers: headers,
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to load profile');
    }

    final data = json.decode(response.body) as Map<String, dynamic>;
    return UserProfile.fromJson(data);
  }

  static Future<UserProfile> updateDisplayName(String name) async {
    final headers = {'Content-Type': 'application/json'};
    headers.addAll(await AuthService.authHeaders());

    final response = await http.put(
      Uri.parse('$baseUrl/api/core/profile/'),
      headers: headers,
      body: json.encode({'display_name': name}),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to update profile');
    }

    final data = json.decode(response.body) as Map<String, dynamic>;
    return UserProfile.fromJson(data);
  }


  static Future<DailyGoal> setDailyGoal(String goal, int target) async {
    final headers = {'Content-Type': 'application/json'};
    headers.addAll(await AuthService.authHeaders());

    final response = await http.post(
      Uri.parse('$baseUrl/api/core/daily-goal/'),
      headers: headers,
      body: json.encode({'goal': goal, 'target': target, 'type': 'daily'}),
    );

    if (response.statusCode != 200 && response.statusCode != 201) {
      throw Exception('Failed to save goal');
    }

    final data = json.decode(response.body) as Map<String, dynamic>;
    return DailyGoal.fromJson(data);
  }

  static Future<Meme> generateMeme() async {
    final headers = {'Content-Type': 'application/json'};
    headers.addAll(await AuthService.authHeaders());

    final response = await http.post(
      Uri.parse('$baseUrl/api/content/generate-meme/'),
      headers: headers,
    );
    final jsonData = jsonDecode(response.body) as Map<String, dynamic>;
    return Meme.fromJson(jsonData);
  }

  static Future<DailyGoal?> fetchDailyGoal() async {
    final headers = {'Content-Type': 'application/json'};
    headers.addAll(await AuthService.authHeaders());
    final response = await http.get(
      Uri.parse('$baseUrl/api/core/daily-goal/'),
      headers: headers,
    );
    if (response.statusCode != 200) {
      return null;
    }
    final data = json.decode(response.body);
    if (data is Map<String, dynamic> && data['goal'] != null) {
      return DailyGoal.fromJson(data);
    }
    return null;
  }

  // static Future<void> setDailyGoal(String goal, int target) async {
  //   final token = await TokenService.getToken() ?? '';
  //   await http.post(
  //     Uri.parse('$baseUrl/api/core/daily-goal/'),
  //     headers: {
  //       'Content-Type': 'application/json',
  //       if (token.isNotEmpty) 'Authorization': 'Token $token',
  //     },
  //     body: json.encode({'goal': goal, 'target': target, 'goal_type': 'daily'}),
  //   );
  // }

  // Registration and login moved to AuthService

  static Future<String> shareBadge(String badgeCode, {String message = ''}) async {
    final headers = {'Content-Type': 'application/json'};
    headers.addAll(await AuthService.authHeaders());
    final response = await http.post(
      Uri.parse('$baseUrl/api/core/share-badge/'),
      headers: headers,
      body: json.encode({'badge_code': badgeCode, 'message': message}),
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to share badge');
    }
    final data = json.decode(response.body) as Map<String, dynamic>;
    return data['message'] as String? ?? 'Badge shared.';
  }

  static Future<void> shareToHerd(Map<String, dynamic> data) async {
    final headers = {'Content-Type': 'application/json'};
    headers.addAll(await AuthService.authHeaders());
    await http.post(
      Uri.parse('$baseUrl/api/core/share-to-herd/'),
      headers: headers,
      body: json.encode(data),
    );
  }

  static Future<Map<String, dynamic>> uploadVoiceJournal(File file) async {
    final request = http.MultipartRequest(
      'POST',
      Uri.parse('$baseUrl/api/core/upload-voice/'),
    );
    final auth = await AuthService.authHeaders();
    request.headers.addAll(auth);
    request.files.add(await http.MultipartFile.fromPath('audio_file', file.path));

    final response = await request.send();
    if (response.statusCode != 200 && response.statusCode != 201) {
      throw Exception('Failed to upload voice journal');
    }

    final body = await response.stream.bytesToString();
    return json.decode(body) as Map<String, dynamic>;
  }

  static Future<void> logout() async {
    await AuthService.logout();
  }
}
