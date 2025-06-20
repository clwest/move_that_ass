import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:infinite_scroll_pagination/infinite_scroll_pagination.dart';

import '../models/feed_item.dart';
import '../services/api_service.dart';
import '../themes/app_theme.dart';

class HerdFeedPage extends StatefulWidget {
  const HerdFeedPage({Key? key}) : super(key: key);

  @override
  State<HerdFeedPage> createState() => _HerdFeedPageState();
}

class _HerdFeedPageState extends State<HerdFeedPage> {
  late final PagingController<int, FeedItem> _pageController =
      PagingController<int, FeedItem>(
    getNextPageKey: (state) =>
        state.lastPageIsEmpty ? null : state.nextIntPageKey,
    fetchPage: (pageKey) => ApiService.fetchHerdFeedPage(pageKey),
  );

  Future<void> _toggleLike(FeedItem item) async {
    final res = await ApiService.toggleLike(item.id);
    setState(() {
      item.likeCount = res['like_count'] as int? ?? item.likeCount;
      item.likedByMe = res['liked_by_me'] as bool? ?? item.likedByMe;
    });
  }

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Herd Feed 🫏')),
      body: RefreshIndicator(
        onRefresh: () => Future.sync(() => _pageController.refresh()),
        child: PagingListener<int, FeedItem>(
          controller: _pageController,
          builder: (context, state, fetchNextPage) => PagedListView<int, FeedItem>(
            state: state,
            fetchNextPage: fetchNextPage,
            padding: const EdgeInsets.all(16),
            builderDelegate: PagedChildBuilderDelegate<FeedItem>(
              itemBuilder: (context, item, index) => _buildCard(item),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildCard(FeedItem item) {
    final ts = DateFormat.yMMMd().add_jm().format(DateTime.now());
    return Card(
      color: AppColors.donkeyCard,
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Text(ts, style: Theme.of(context).textTheme.bodySmall),
                const Spacer(),
                IconButton(
                  icon: Icon(
                    item.likedByMe ? Icons.favorite : Icons.favorite_border,
                    color: Colors.red,
                  ),
                  onPressed: () => _toggleLike(item),
                ),
                Text(item.likeCount.toString()),
              ],
            ),
            if (item.imageUrl.isNotEmpty)
              Image.network(item.imageUrl, fit: BoxFit.cover),
            if (item.caption.isNotEmpty) ...[
              const SizedBox(height: 8),
              Text(item.caption),
            ],
          ],
        ),
      ),
    );
  }
}
