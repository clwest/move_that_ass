import 'package:flutter/material.dart';
import 'package:share_plus/share_plus.dart';
import 'package:gallery_saver/gallery_saver.dart';

import '../models/meme.dart';

class MemeSharePage extends StatelessWidget {
  final Meme meme;

  const MemeSharePage({required this.meme, Key? key}) : super(key: key);

  Future<void> saveMemeToDevice(Meme meme) async {
    await GallerySaver.saveImage(meme.imageUrl);
  }

  void shareMeme(Meme meme) {
    Share.share('${meme.caption}\n${meme.imageUrl}');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Meme Preview 🫏')),
      body: Column(
        children: [
          Expanded(
            child: Image.network(
              meme.imageUrl,
              fit: BoxFit.contain,
              errorBuilder: (context, error, stackTrace) {
                return const Center(
                  child: Text('Failed to load meme image 🫏'),
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(12),
            child: Text(
              meme.caption,
              style: const TextStyle(fontSize: 18, fontStyle: FontStyle.italic),
              textAlign: TextAlign.center,
            ),
          ),
          ElevatedButton(
            onPressed: () => saveMemeToDevice(meme),
            child: const Text('💾 Save to Device'),
          ),
          ElevatedButton(
            onPressed: () => shareMeme(meme),
            child: const Text('📤 Share Meme'),
          ),
          const SizedBox(height: 20),
        ],
      ),
    );
  }
}
