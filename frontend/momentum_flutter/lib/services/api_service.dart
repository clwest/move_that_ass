import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

import '../models/today_dashboard.dart';
import '../models/badge.dart';
import '../models/meme.dart';

class ApiService {
  static const String baseUrl = 'http://localhost:8000';

  static Future<TodayDashboard> fetchTodayDashboard() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('auth_token') ?? '';

    final response = await http.get(
      Uri.parse('$baseUrl/api/core/dashboard-today/'),
      headers: {
        'Content-Type': 'application/json',
        if (token.isNotEmpty) 'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to load dashboard');
    }

    final data = json.decode(response.body) as Map<String, dynamic>;
    return TodayDashboard.fromJson(data);
  }

  static Future<List<Badge>> fetchBadges() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('auth_token') ?? '';

    final response = await http.get(
      Uri.parse('$baseUrl/api/core/badges/'),
      headers: {
        'Content-Type': 'application/json',
        if (token.isNotEmpty) 'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to load badges');
    }

    final List data = json.decode(response.body) as List;
    return data.map((e) => Badge.fromJson(e as Map<String, dynamic>)).toList();
  }

  static Future<Meme> generateMeme({String tone = 'funny'}) async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('auth_token') ?? '';

    final response = await http.post(
      Uri.parse('$baseUrl/api/content/generate-meme/'),
      headers: {
        'Content-Type': 'application/json',
        if (token.isNotEmpty) 'Authorization': 'Bearer $token',
      },
      body: json.encode({'tone': tone}),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to generate meme');
    }

    final data = json.decode(response.body) as Map<String, dynamic>;
    return Meme.fromJson(data);
  }
}
