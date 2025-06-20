import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:momentum_flutter/pages/voice_journal_page.dart';
import 'package:momentum_flutter/services/api_service.dart';
import 'package:momentum_flutter/services/task_poller.dart';
import 'package:record/record.dart';
import 'package:shared_preferences/shared_preferences.dart';

class FakeRecord extends Fake implements Record {
  @override
  Future<void> start({RecordConfig? config, String? path}) async {}

  @override
  Future<String?> stop() async => '/tmp/test.m4a';
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  SharedPreferences.setMockInitialValues({});

  testWidgets('VoiceJournalPage shows result after upload', (tester) async {
    ApiService.uploadVoice = (String path) async => '1';
    TaskPoller.poll = (String id, {Duration interval = const Duration(seconds: 2)}) async {
      return {
        'state': 'SUCCESS',
        'data': jsonEncode({'summary': 'hello', 'audio_url': '/a'})
      };
    };

    await tester.pumpWidget(MaterialApp(home: VoiceJournalPage(recorder: FakeRecord())));
    await tester.pump();

    await tester.longPress(find.byIcon(Icons.mic));
    await tester.pump();
    await tester.tap(find.byIcon(Icons.stop));
    await tester.pump();

    expect(find.text('hello'), findsOneWidget);
  });
}
