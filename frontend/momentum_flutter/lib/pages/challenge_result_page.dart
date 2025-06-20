import 'package:flutter/material.dart';

import '../services/api_service.dart';
import '../utils/text_utils.dart';

class ChallengeResultPage extends StatefulWidget {
  const ChallengeResultPage({Key? key, required this.challengeId, required this.challengeText}) : super(key: key);
  final int challengeId;
  final String challengeText;

  static const routeName = '/challenge-result';

  @override
  State<ChallengeResultPage> createState() => _ChallengeResultPageState();
}

class _ChallengeResultPageState extends State<ChallengeResultPage> {
  final TextEditingController _noteController = TextEditingController();
  bool _submitting = false;

  Future<void> _complete() async {
    setState(() => _submitting = true);
    try {
      final res = await ApiService.completeChallenge(widget.challengeId);
      if (!mounted) return;
      if (res['badge_code'] != null) {
        await showDialog(
          context: context,
          builder: (_) => AlertDialog(
            title: const Text('Badge Earned!'),
            content: Text(res['badge_name'] as String? ?? ''),
            actions: [
              TextButton(
                onPressed: () async {
                  await ApiService.shareBadge(res['badge_code'] as String);
                  if (mounted) {
                    Navigator.pop(context);
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Badge shared!')),
                    );
                  }
                },
                child: const Text('Share'),
              ),
              TextButton(
                onPressed: () => Navigator.pop(context),
                child: const Text('Close'),
              ),
            ],
          ),
        );
      }
      Navigator.pop(context, true);
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context)
            .showSnackBar(const SnackBar(content: Text('Failed')));
      }
    } finally {
      if (mounted) setState(() => _submitting = false);
    }
  }

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
              onPressed: _submitting ? null : _complete,
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
