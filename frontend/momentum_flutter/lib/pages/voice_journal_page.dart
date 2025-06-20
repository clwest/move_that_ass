import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:record/record.dart';
import 'package:audioplayers/audioplayers.dart';
import 'package:permission_handler/permission_handler.dart';

import '../services/api_service.dart';
import '../services/task_poller.dart';
import '../utils/text_utils.dart';

class VoiceJournalPage extends StatefulWidget {
  const VoiceJournalPage({Key? key, this.recorder}) : super(key: key);
  final Record? recorder;

  static const routeName = '/voice-journal';

  @override
  State<VoiceJournalPage> createState() => _VoiceJournalPageState();
}

class _VoiceJournalPageState extends State<VoiceJournalPage> {
  late final Record _record;
  final AudioPlayer _player = AudioPlayer();
  bool _isRecording = false;
  Map<String, dynamic>? _result;
  bool _loading = false;

  @override
  void initState() {
    super.initState();
    _record = widget.recorder ?? Record();
  }

  Future<void> _startRec() async {
    final perm = await Permission.microphone.request();
    if (!perm.isGranted) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Microphone permission denied')),
        );
      }
      return;
    }
    await _record.start();
    setState(() => _isRecording = true);
  }

  Future<void> _stopRec() async {
    final path = await _record.stop();
    setState(() => _isRecording = false);
    if (path == null) return;
    setState(() => _loading = true);
    try {
      final taskId = await ApiService.uploadVoice(path);
      final res = await TaskPoller.poll(taskId);
      final data = json.decode(res['data'] as String) as Map<String, dynamic>;
      if (!mounted) return;
      setState(() => _result = data);
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context)
            .showSnackBar(const SnackBar(content: Text('Upload failed')));
      }
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  void dispose() {
    _record.dispose();
    _player.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Voice Journal')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (_result != null) ...[
              Text(cleanText(_result!['summary'] as String? ?? '')),
              const SizedBox(height: 12),
              ElevatedButton(
                onPressed: () async {
                  final url = '${ApiService.baseUrl}${_result!['audio_url']}';
                  await _player.play(UrlSource(url));
                },
                child:
                    Text('Play', style: Theme.of(context).textTheme.labelLarge),
              ),
            ],
            if (_loading) const Center(child: CircularProgressIndicator()),
          ],
        ),
      ),
      floatingActionButton: _isRecording
          ? FloatingActionButton(
              onPressed: _stopRec,
              child: const Icon(Icons.stop),
            )
          : GestureDetector(
              onLongPress: _startRec,
              child: const CircleAvatar(
                radius: 28,
                child: Icon(Icons.mic),
              ),
            ),
    );
  }
}
