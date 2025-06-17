import 'dart:io';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:path_provider/path_provider.dart';
import 'package:share_plus/share_plus.dart';
import 'package:gallery_saver/gallery_saver.dart';

import '../models/meme.dart';

class MemeSharePage extends StatelessWidget {
  final Meme meme;

  const MemeSharePage({super.key, required this.meme});

  Future<void> saveMemeToDevice(Meme meme) async {
    try {
      final response = await http.get(Uri.parse(meme.imageUrl));
      if (response.statusCode == 200) {
        final directory = await getTemporaryDirectory();
        final path =
            '${directory.path}/meme_${DateTime.now().millisecondsSinceEpoch}.png';
        final file = File(path);
        await file.writeAsBytes(response.bodyBytes);
        await GallerySaver.saveImage(file.path);
      }
    } catch (e) {
      debugPrint('Failed to save meme: $e');
    }
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
              errorBuilder: (context, error, stackTrace) => const Center(
                child: Text('Failed to load image'),
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(12),
            child: Text(
              meme.caption,
              style:
                  const TextStyle(fontSize: 18, fontStyle: FontStyle.italic),
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
        ],
      ),
    );
  }
}

