import 'package:flutter/material.dart';
import 'package:share_plus/share_plus.dart';
import 'package:gallery_saver/gallery_saver.dart';
import 'package:permission_handler/permission_handler.dart';

import '../models/meme.dart';
import '../services/api_service.dart';
import '../utils/text_utils.dart';

class MemeSharePage extends StatelessWidget {
  final Meme meme;

  const MemeSharePage({required this.meme, Key? key}) : super(key: key);

  Future<void> saveMemeToDevice(BuildContext context, Meme meme) async {
    final status = await Permission.photos.request();
    if (!status.isGranted) {
      if (!context.mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Please enable photo permissions to save memes.'),
        ),
      );
      return;
    }

    try {
      final bool? result = await GallerySaver.saveImage(meme.imageUrl);
      if (!context.mounted) return;
      final message =
          result == true ? 'Meme saved to gallery! 🫏' : 'Failed to save meme.';
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(message)),
      );
    } catch (e) {
      if (!context.mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Error saving meme to gallery.')),
      );
    }
  }

  void shareMeme(Meme meme) {
    Share.share('${meme.caption}\n${meme.imageUrl}');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Meme Preview 🫏')),
      body: SingleChildScrollView(
        child: Column(
          children: [
            Image.network(
              meme.imageUrl,
              fit: BoxFit.contain,
              errorBuilder: (context, error, stackTrace) {
                return const Center(
                  child: Text('Failed to load meme image 🫏'),
                );
              },
            ),
          Padding(
            padding: const EdgeInsets.all(12),
            child: Text(
              cleanText(meme.caption),
              style: const TextStyle(fontSize: 18, fontStyle: FontStyle.italic, inherit: true),
              textAlign: TextAlign.center,
            ),
          ),
          ElevatedButton(
            onPressed: () => saveMemeToDevice(context, meme),
            child: Text('💾 Save to Device',
                style: Theme.of(context).textTheme.labelLarge),
          ),
          ElevatedButton(
            onPressed: () => shareMeme(meme),
            child:
                Text('📤 Share Meme', style: Theme.of(context).textTheme.labelLarge),
          ),
          ElevatedButton(
            onPressed: () async {
              await ApiService.shareToHerd({
                'type': 'meme',
                'caption': meme.caption,
                'image_url': meme.imageUrl,
              });
              if (!context.mounted) return;
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Meme shared with the herd 🫏📣')),
              );
            },
            child: Text('📣 Share to Herd',
                style: Theme.of(context).textTheme.labelLarge),
          ),
          const SizedBox(height: 20),
        ],
      ),
    ),
  );
  }
}
