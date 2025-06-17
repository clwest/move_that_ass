import 'dart:convert';
import 'package:http/http.dart' as http;
import 'token_service.dart';

import '../models/today_dashboard.dart';
import '../models/badge.dart';
import '../models/meme.dart';
import '../models/herd_post.dart';
import '../models/profile.dart';
import '../models/daily_goal.dart';

class ApiService {
  static const String baseUrl = 'http://localhost:8000';

  static Future<TodayDashboard> fetchTodayDashboard() async {
    final token = await TokenService.getToken() ?? '';

    final response = await http.get(
      Uri.parse('$baseUrl/api/core/dashboard-today/'),
      headers: {
        'Content-Type': 'application/json',
        if (token.isNotEmpty) 'Authorization': 'Token $token',
      },
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to load dashboard');
    }

    final data = json.decode(response.body) as Map<String, dynamic>;
    return TodayDashboard.fromJson(data);
  }

  static Future<List<Badge>> fetchBadges() async {
    final token = await TokenService.getToken() ?? '';
    // ensure badges are evaluated on the server
    await http.get(
      Uri.parse('$baseUrl/api/core/check-badges/'),
      headers: {
        'Content-Type': 'application/json',
        if (token.isNotEmpty) 'Authorization': 'Token $token',
      },
    );

    final response = await http.get(
      Uri.parse('$baseUrl/api/core/badges/'),
      headers: {
        'Content-Type': 'application/json',
        if (token.isNotEmpty) 'Authorization': 'Token $token',
      },
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to load badges');
    }

    final List data = json.decode(response.body) as List;
    return data.map((e) => Badge.fromJson(e as Map<String, dynamic>)).toList();
  }

  static Future<List<HerdPost>> fetchHerdFeed() async {
    final token = await TokenService.getToken() ?? '';

    final response = await http.get(
      Uri.parse('$baseUrl/api/core/herd-feed/'),
      headers: {
        'Content-Type': 'application/json',
        if (token.isNotEmpty) 'Authorization': 'Token $token',
      },
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to load herd feed');
    }

    final List data = json.decode(response.body) as List;
    return data.map((e) => HerdPost.fromJson(e as Map<String, dynamic>)).toList();
  }

  static Future<UserProfile> fetchProfile() async {
    final token = await TokenService.getToken() ?? '';

    final response = await http.get(
      Uri.parse('$baseUrl/api/core/profile/'),
      headers: {
        'Content-Type': 'application/json',
        if (token.isNotEmpty) 'Authorization': 'Token $token',
      },
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to load profile');
    }

    final data = json.decode(response.body) as Map<String, dynamic>;
    return UserProfile.fromJson(data);
  }

  static Future<UserProfile> updateDisplayName(String name) async {
    final token = await TokenService.getToken() ?? '';

    final response = await http.put(
      Uri.parse('$baseUrl/api/core/profile/'),
      headers: {
        'Content-Type': 'application/json',
        if (token.isNotEmpty) 'Authorization': 'Token $token',
      },
      body: json.encode({'display_name': name}),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to update profile');
    }

    final data = json.decode(response.body) as Map<String, dynamic>;
    return UserProfile.fromJson(data);
  }

  static Future<DailyGoal?> getDailyGoal() async {
    final token = await TokenService.getToken() ?? '';

    final response = await http.get(
      Uri.parse('$baseUrl/api/core/daily-goal/'),
      headers: {
        'Content-Type': 'application/json',
        if (token.isNotEmpty) 'Authorization': 'Token $token',
      },
    );

    if (response.statusCode != 200) {
      return null;
    }

    final data = json.decode(response.body);
    if (data is Map<String, dynamic> && data.isNotEmpty) {
      return DailyGoal.fromJson(data);
    }
    return null;
  }

  static Future<DailyGoal> setDailyGoal(String goal, int target) async {
    final token = await TokenService.getToken() ?? '';

    final response = await http.post(
      Uri.parse('$baseUrl/api/core/daily-goal/'),
      headers: {
        'Content-Type': 'application/json',
        if (token.isNotEmpty) 'Authorization': 'Token $token',
      },
      body: json.encode({'goal': goal, 'target': target, 'type': 'daily'}),
    );

    if (response.statusCode != 200 && response.statusCode != 201) {
      throw Exception('Failed to save goal');
    }

    final data = json.decode(response.body) as Map<String, dynamic>;
    return DailyGoal.fromJson(data);
  }

  static Future<Meme> generateMeme({String tone = 'funny'}) async {
    final token = await TokenService.getToken() ?? '';

    final response = await http.post(
      Uri.parse('$baseUrl/api/content/generate-meme/'),
      headers: {
        'Content-Type': 'application/json',
        if (token.isNotEmpty) 'Authorization': 'Token $token',
      },
      body: json.encode({'tone': tone}),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to generate meme');
    }

    final data = json.decode(response.body) as Map<String, dynamic>;
    return Meme.fromJson(data);
  }

  static Future<Map<String, dynamic>?> fetchDailyGoal() async {
    final token = await TokenService.getToken() ?? '';
    final response = await http.get(
      Uri.parse('$baseUrl/api/core/daily-goal/'),
      headers: {
        'Content-Type': 'application/json',
        if (token.isNotEmpty) 'Authorization': 'Token $token',
      },
    );
    if (response.statusCode != 200) {
      return null;
    }
    final data = json.decode(response.body) as Map<String, dynamic>;
    if (data['goal'] == null) return null;
    return data;
  }

  static Future<void> setDailyGoal(String goal, int target) async {
    final token = await TokenService.getToken() ?? '';
    await http.post(
      Uri.parse('$baseUrl/api/core/daily-goal/'),
      headers: {
        'Content-Type': 'application/json',
        if (token.isNotEmpty) 'Authorization': 'Token $token',
      },
      body: json.encode({'goal': goal, 'target': target, 'goal_type': 'daily'}),
    );
  }

  static Future<void> register(String username, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/core/register/'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'username': username, 'password': password}),
    );
    if (response.statusCode != 201) {
      throw Exception('Failed to register');
    }
  }

  static Future<String> login(String username, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/core/login/'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'username': username, 'password': password}),
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to login');
    }
    final data = json.decode(response.body) as Map<String, dynamic>;
    final token = data['token'] as String;
    await TokenService.saveToken(token);
    return token;
  }

  static Future<void> shareToHerd(Map<String, dynamic> data) async {
    final token = await TokenService.getToken();
    await http.post(
      Uri.parse('$baseUrl/api/core/share-to-herd/'),
      headers: {
        'Authorization': 'Token $token',
        'Content-Type': 'application/json',
      },
      body: json.encode(data),
    );
  }
}
