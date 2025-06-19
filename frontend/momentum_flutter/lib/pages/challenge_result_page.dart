import 'package:flutter/material.dart';

import '../services/api_service.dart';
import '../utils/text_utils.dart';

class ChallengeResultPage extends StatefulWidget {
  const ChallengeResultPage({Key? key, required this.challengeText}) : super(key: key);
  final String challengeText;

  static const routeName = '/challenge-result';

  @override
  State<ChallengeResultPage> createState() => _ChallengeResultPageState();
}

class _ChallengeResultPageState extends State<ChallengeResultPage> {
  final TextEditingController _noteController = TextEditingController();
  bool _submitting = false;

  Future<void> _shareResult() async {
    setState(() => _submitting = true);
    try {
      await ApiService.shareToHerd({
        'type': 'meme',
        'caption': 'Completed: ${widget.challengeText}\n${_noteController.text.trim()}',
      });
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Shared with herd!')),
      );
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Failed to share')),
        );
      }
    } finally {
      if (mounted) setState(() => _submitting = false);
    }
  }

  @override
  void dispose() {
    _noteController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Challenge Result')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              cleanText(widget.challengeText),
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _noteController,
              decoration: const InputDecoration(labelText: 'How did it go?'),
              maxLines: 3,
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _submitting
                  ? null
                  : () {
                      Navigator.pop(context, true);
                    },
              child: Text('Mark Complete',
                  style: Theme.of(context).textTheme.labelLarge),
            ),
            const SizedBox(height: 8),
            OutlinedButton(
              onPressed: _submitting ? null : _shareResult,
              child: const Text('Share Result to Herd'),
            ),
          ],
        ),
      ),
    );
  }
}
