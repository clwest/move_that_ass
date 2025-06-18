import 'dart:io';

import 'package:flutter/material.dart';
import 'package:record/record.dart';
import 'package:audioplayers/audioplayers.dart';

import '../services/api_service.dart';
import '../utils/text_utils.dart';

class VoiceJournalPage extends StatefulWidget {
  const VoiceJournalPage({super.key});

  static const routeName = '/voice-journal';

  @override
  State<VoiceJournalPage> createState() => _VoiceJournalPageState();
}

class _VoiceJournalPageState extends State<VoiceJournalPage> {
  final AudioRecorder _record = AudioRecorder();
  final AudioPlayer _player = AudioPlayer();

  bool _isRecording = false;
  String? _summary;
  String? _audioUrl;
  List<dynamic>? _tags;
  bool _uploading = false;

  Future<void> _startRecording() async {
    if (await _record.hasPermission()) {
      await _record.start();
      setState(() => _isRecording = true);
    }
  }

  Future<void> _stopAndUpload() async {
    final path = await _record.stop();
    setState(() => _isRecording = false);
    if (path == null) return;

    setState(() => _uploading = true);
    try {
      final result = await ApiService.uploadVoiceJournal(File(path));
      if (!mounted) return;
      setState(() {
        _summary = cleanText(result['summary'] as String? ?? '');
        _audioUrl = result['playback_audio_url'] as String?;
        _tags = result['tags'] as List<dynamic>?;
      });
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context)
          .showSnackBar(const SnackBar(content: Text('Upload failed')));
    } finally {
      if (mounted) setState(() => _uploading = false);
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
            if (_summary != null) ...[
              Text(
                _summary!,
                style:
                    const TextStyle(fontStyle: FontStyle.italic, inherit: true),
              ),
              const SizedBox(height: 12),
            ],
            if (_tags != null) ...[
              Wrap(
                spacing: 8,
                children:
                    _tags!.map((t) => Chip(label: Text(t.toString()))).toList(),
              ),
              const SizedBox(height: 12),
            ],
            if (_audioUrl != null)
              ElevatedButton(
                onPressed: () async {
                  final url = '${ApiService.baseUrl}$_audioUrl';
                  await _player.play(UrlSource(url));
                },
                child: const Text('Play Summary'),
              ),
            if (_uploading) ...[
              const SizedBox(height: 20),
              const Center(child: CircularProgressIndicator()),
            ]
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _isRecording ? _stopAndUpload : _startRecording,
        child: Icon(_isRecording ? Icons.stop : Icons.mic),
      ),
    );
  }
}
