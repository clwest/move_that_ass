import 'dart:async';

import 'api_service.dart';

class TaskPoller {
  static Future<Map<String, dynamic>> Function(String id,
      {Duration interval}) poll = _poll;

  static Future<Map<String, dynamic>> _poll(String id,
      {Duration interval = const Duration(seconds: 2)}) async {
    while (true) {
      final res = await ApiService.get('/api/core/tasks/$id/');
      if (res['state'] == 'SUCCESS' || res['state'] == 'FAILURE') return res;
      await Future.delayed(interval);
    }
  }
}
