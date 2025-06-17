import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import '../models/herd_post.dart';
import '../services/api_service.dart';
import '../themes/app_theme.dart';

class HerdFeedPage extends StatefulWidget {
  const HerdFeedPage({super.key});

  @override
  State<HerdFeedPage> createState() => _HerdFeedPageState();
}

class _HerdFeedPageState extends State<HerdFeedPage> {
  late Future<List<HerdPost>> _future;

  @override
  void initState() {
    super.initState();
    _future = ApiService.fetchHerdFeed();
  }

  Future<void> _refresh() async {
    setState(() {
      _future = ApiService.fetchHerdFeed();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Herd Feed 🫏')),
      body: RefreshIndicator(
        onRefresh: _refresh,
        child: FutureBuilder<List<HerdPost>>(
          future: _future,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator());
            } else if (snapshot.hasError) {
              return Center(child: Text('Error: ${snapshot.error}'));
            }

            final posts = snapshot.data!..sort((a, b) => b.createdAt.compareTo(a.createdAt));
            return ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: posts!.length,
              itemBuilder: (context, index) => _buildPostCard(posts[index]),
            );
          },
        ),
      ),
    );
  }

  Widget _buildPostCard(HerdPost post) {
    final timestamp = DateFormat.yMMMd().add_jm().format(post.createdAt.toLocal());
    Widget content;
    if (post.type == 'meme') {
      content = Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (post.content['image_url'] != null)
            Image.network(post.content['image_url'] as String, fit: BoxFit.cover),
          const SizedBox(height: 8),
          Text(post.content['caption'] as String? ?? ''),
        ],
      );
    } else if (post.type == 'badge') {
      content = Row(
        children: [
          Text(
            post.content['emoji'] as String? ?? '🏅',
            style: const TextStyle(fontSize: 32, inherit: true),
          ),
          const SizedBox(width: 8),
          Text(post.content['name'] as String? ?? ''),
        ],
      );
    } else {
      content = const SizedBox.shrink();
    }

    return Card(
      color: AppColors.donkeyCard,
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                CircleAvatar(
                  child: Text(post.user.substring(0, 1).toUpperCase()),
                ),
                const SizedBox(width: 8),
                Text(post.user, style: const TextStyle(inherit: true)),
                const Spacer(),
                Text(timestamp, style: Theme.of(context).textTheme.bodySmall),
              ],
            ),
            const SizedBox(height: 8),
            content,
          ],
        ),
      ),
    );
  }
}
