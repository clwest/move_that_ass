import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';
import 'auth_service.dart';
import '../config.dart';

import '../models/dashboard_item.dart';
import '../models/badge.dart';
import '../models/meme.dart';
import '../models/herd_post.dart';
import '../models/feed_item.dart';
import '../models/profile.dart';
import '../models/daily_goal.dart';
import 'task_poller.dart';

class ApiService {
  static String get baseUrl => AppConfig.baseUrl;

  static Future<http.Response> _send(Future<http.Response> Function() req) async {
    var res = await req();
    if (res.statusCode == 401) {
      final ok = await AuthService.refresh();
      if (ok) {
        res = await req();
      } else {
        await AuthService.logout();
        throw UnauthorizedException();
      }
    }
    return res;
  }

  static Future<Map<String, dynamic>> get(String path) async {
    final response = await _send(() {
      final headers = {'Content-Type': 'application/json'};
      headers.addAll(AuthService.authHeaders());
      return http.get(Uri.parse('$baseUrl$path'), headers: headers);
    });
    if (response.statusCode != 200) {
      throw Exception('Request failed');
    }
    return json.decode(response.body) as Map<String, dynamic>;
  }

  static Future<List<DashboardItem>> fetchDashboard() async {
    final response = await _send(() {
      final headers = {'Content-Type': 'application/json'};
      headers.addAll(AuthService.authHeaders());
      return http.get(
        Uri.parse('$baseUrl/api/core/dashboard/'),
        headers: headers,
      );
    });

    if (response.statusCode != 200) {
      throw Exception('Failed to load dashboard');
    }

    final List data = json.decode(response.body) as List;
    return data
        .map((e) => DashboardItem.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  static Future<List<Badge>> fetchBadges() async {
    // ensure badges are evaluated on the server
    await _send(() {
      final headers = {'Content-Type': 'application/json'};
      headers.addAll(AuthService.authHeaders());
      return http.get(
        Uri.parse('$baseUrl/api/core/check-badges/'),
        headers: headers,
      );
    });

    final response = await _send(() {
      final headers = {'Content-Type': 'application/json'};
      headers.addAll(AuthService.authHeaders());
      return http.get(
        Uri.parse('$baseUrl/api/core/badges/'),
        headers: headers,
      );
    });

    if (response.statusCode != 200) {
      throw Exception('Failed to load badges');
    }

    final List data = json.decode(response.body) as List;
    return data.map((e) => Badge.fromJson(e as Map<String, dynamic>)).toList();
  }

  static Future<List<FeedItem>> Function(int page) fetchHerdFeedPage =
      _fetchHerdFeedPage;

  static Future<List<FeedItem>> _fetchHerdFeedPage(int page) async {
    final response = await _send(() {
      final headers = {'Content-Type': 'application/json'};
      headers.addAll(AuthService.authHeaders());
      return http.get(
        Uri.parse('$baseUrl/api/core/herd-feed/?page=$page'),
        headers: headers,
      );
    });

    if (response.statusCode != 200) {
      throw Exception('Failed to load herd feed');
    }

    final Map<String, dynamic> data = json.decode(response.body);
    final List posts = data['results'] as List? ?? [];
    return posts.map((e) => FeedItem.fromJson(e as Map<String, dynamic>)).toList();
  }

  static Future<UserProfile> fetchProfile() async {
    final response = await _send(() {
      final headers = {'Content-Type': 'application/json'};
      headers.addAll(AuthService.authHeaders());
      return http.get(
        Uri.parse('$baseUrl/api/core/profile/'),
        headers: headers,
      );
    });

    if (response.statusCode != 200) {
      throw Exception('Failed to load profile');
    }

    final data = json.decode(response.body) as Map<String, dynamic>;
    return UserProfile.fromJson(data);
  }

  static Future<UserProfile> updateDisplayName(String name) async {
    final response = await _send(() {
      final headers = {'Content-Type': 'application/json'};
      headers.addAll(AuthService.authHeaders());
      return http.put(
        Uri.parse('$baseUrl/api/core/profile/'),
        headers: headers,
        body: json.encode({'display_name': name}),
      );
    });

    if (response.statusCode != 200) {
      throw Exception('Failed to update profile');
    }

    final data = json.decode(response.body) as Map<String, dynamic>;
    return UserProfile.fromJson(data);
  }


  static Future<DailyGoal> setDailyGoal(String goal, int target) async {
    final response = await _send(() {
      final headers = {'Content-Type': 'application/json'};
      headers.addAll(AuthService.authHeaders());
      return http.post(
        Uri.parse('$baseUrl/api/core/daily-goal/'),
        headers: headers,
        body: json.encode({'goal': goal, 'target': target, 'type': 'daily'}),
      );
    });

    if (response.statusCode != 200 && response.statusCode != 201) {
      throw Exception('Failed to save goal');
    }

    final data = json.decode(response.body) as Map<String, dynamic>;
    return DailyGoal.fromJson(data);
  }

  static Future<Meme> generateMeme() async {
    final response = await _send(() {
      final headers = {'Content-Type': 'application/json'};
      headers.addAll(AuthService.authHeaders());
      return http.post(
        Uri.parse('$baseUrl/api/content/meme/'),
        headers: headers,
      );
    });
    if (response.statusCode != 202) {
      throw Exception('Failed to start meme generation');
    }
    final data = json.decode(response.body) as Map<String, dynamic>;
    final taskId = data['task_id'] as String;
    final result = await TaskPoller.poll(taskId);
    final payload = json.decode(result['data'] as String);
    return Meme.fromJson(payload as Map<String, dynamic>);
  }

  static Future<List<String>> generateWorkoutPlan(
      {String goal = '', List<String> activityTypes = const [], String tone = 'supportive'}) async {
    final response = await _send(() {
      final headers = {'Content-Type': 'application/json'};
      headers.addAll(AuthService.authHeaders());
      return http.post(
        Uri.parse('$baseUrl/api/core/workout-plan/'),
        headers: headers,
        body: json.encode({
          'goal': goal,
          'activity_types': activityTypes,
          'tone': tone,
        }),
      );
    });
    if (response.statusCode != 202) {
      throw Exception('Failed to start workout plan generation');
    }
    final data = json.decode(response.body) as Map<String, dynamic>;
    final result = await TaskPoller.poll(data['task_id'] as String);
    final payload = json.decode(result['data'] as String) as Map<String, dynamic>;
    final List<dynamic> plan = payload['plan'] as List<dynamic>? ?? [];
    return plan.map((e) => e.toString()).toList();
  }

  static Future<Map<String, dynamic>> generateMealPlan(
      {String goal = '', String tone = 'supportive', String? mood}) async {
    final response = await _send(() {
      final headers = {'Content-Type': 'application/json'};
      headers.addAll(AuthService.authHeaders());
      return http.post(
        Uri.parse('$baseUrl/api/core/meal-plan/'),
        headers: headers,
        body: json.encode({'goal': goal, 'tone': tone, 'mood': mood}),
      );
    });
    if (response.statusCode != 202) {
      throw Exception('Failed to start meal plan generation');
    }
    final data = json.decode(response.body) as Map<String, dynamic>;
    final result = await TaskPoller.poll(data['task_id'] as String);
    return json.decode(result['data'] as String) as Map<String, dynamic>;
  }

  static Future<DailyGoal?> fetchDailyGoal() async {
    final response = await _send(() {
      final headers = {'Content-Type': 'application/json'};
      headers.addAll(AuthService.authHeaders());
      return http.get(
        Uri.parse('$baseUrl/api/core/daily-goal/'),
        headers: headers,
      );
    });
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
    final response = await _send(() {
      final headers = {'Content-Type': 'application/json'};
      headers.addAll(AuthService.authHeaders());
      return http.post(
        Uri.parse('$baseUrl/api/core/share-badge/'),
        headers: headers,
        body: json.encode({'badge_code': badgeCode, 'message': message}),
      );
    });
    if (response.statusCode != 200 && response.statusCode != 201) {
      throw Exception('Failed to share badge');
    }
    final data = json.decode(response.body) as Map<String, dynamic>;
    return data['message'] as String? ?? 'Badge shared.';
  }

  static Future<void> shareToHerd(Map<String, dynamic> data) async {
    await _send(() {
      final headers = {'Content-Type': 'application/json'};
      headers.addAll(AuthService.authHeaders());
      return http.post(
        Uri.parse('$baseUrl/api/core/share-to-herd/'),
        headers: headers,
        body: json.encode(data),
      );
    });
  }

  static Future<String> Function(String path) uploadVoice = _uploadVoice;

  static Future<String> _uploadVoice(String path) async {
    final request = http.MultipartRequest(
      'POST',
      Uri.parse('$baseUrl/api/voice/upload/'),
    );
    final auth = AuthService.authHeaders();
    request.headers.addAll(auth);
    request.files.add(await http.MultipartFile.fromPath('audio_file', path));

    final response = await request.send();
    if (response.statusCode != 202 && response.statusCode != 200 &&
        response.statusCode != 201) {
      throw Exception('Failed to upload voice');
    }

    final body = await response.stream.bytesToString();
    final data = json.decode(body) as Map<String, dynamic>;
    return data['task_id'] as String;
  }

  static Future<String> Function(String url, XFile file) uploadImage = _uploadImage;

  static Future<String> _uploadImage(String url, XFile file) async {
    final req = http.MultipartRequest('POST', Uri.parse(baseUrl + url));
    req.files.add(await http.MultipartFile.fromPath('file', file.path));
    final auth = AuthService.authHeaders();
    req.headers.addAll(auth);
    final streamed = await req.send();
    final res = await http.Response.fromStream(streamed);
    if (res.statusCode == 401) {
      final refreshed = await AuthService.refresh();
      if (refreshed) {
        return _uploadImage(url, file);
      }
      await AuthService.logout();
      throw UnauthorizedException();
    }
    if (res.statusCode != 202 && res.statusCode != 200 && res.statusCode != 201) {
      throw Exception('Failed to upload image');
    }
    return jsonDecode(res.body)['task_id'] as String;
  }

  static Future<Map<String, dynamic>> completeChallenge(int id) async {
    final res = await _send(() {
      final headers = {'Content-Type': 'application/json'};
      headers.addAll(AuthService.authHeaders());
      return http.post(
        Uri.parse('$baseUrl/api/core/movement/challenges/$id/complete/'),
        headers: headers,
      );
    });
    if (res.statusCode != 200 && res.statusCode != 201) {
      throw Exception('Failed to complete challenge');
    }
    return json.decode(res.body) as Map<String, dynamic>;
  }

  static Future<Map<String, dynamic>> toggleLike(int id) async {
    final res = await _send(() {
      final headers = {'Content-Type': 'application/json'};
      headers.addAll(AuthService.authHeaders());
      return http.post(
        Uri.parse('$baseUrl/api/core/herd-feed/$id/like/'),
        headers: headers,
      );
    });
    if (res.statusCode != 200) {
      throw Exception('Failed to like');
    }
    return json.decode(res.body) as Map<String, dynamic>;
  }

  static Future<void> logout() async {
    await AuthService.logout();
  }
}

class UnauthorizedException implements Exception {}
