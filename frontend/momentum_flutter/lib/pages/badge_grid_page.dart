import 'package:flutter/material.dart';

import '../models/badge.dart' as app_models;
import '../services/api_service.dart';
import '../themes/app_theme.dart';

class BadgeGridPage extends StatefulWidget {
  const BadgeGridPage({super.key});

  @override
  State<BadgeGridPage> createState() => _BadgeGridPageState();
}

class _BadgeGridPageState extends State<BadgeGridPage> {
  late Future<List<app_models.Badge>> _future;
  bool _earnedOnly = false;

  @override
  void initState() {
    super.initState();
    _future = ApiService.fetchBadges();
  }

  Future<void> _refresh() async {
    setState(() {
      _future = ApiService.fetchBadges();
    });
  }

  void _showBadgeDetails(app_models.Badge badge) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('${badge.emoji} ${badge.name}'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(badge.description),
            if (badge.earnedAt != null)
              Padding(
                padding: const EdgeInsets.only(top: 8.0),
                child: Text('Unlocked on: ${badge.earnedAt}'),
              ),
          ],
        ),
        actions: [
          if (badge.isEarned)
            TextButton(
              onPressed: () async {
                try {
                  final message = await ApiService.shareBadge(badge.code);
                  if (context.mounted) {
                    Navigator.of(context).pop();
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text(message)),
                    );
                  }
                } catch (e) {
                  if (context.mounted) {
                    Navigator.of(context).pop();
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Failed to share badge')),
                    );
                  }
                }
              },
              child: const Text('📣 Share to Herd'),
            ),
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Close'),
          ),
        ],
      ),
    );
  }

  Widget _buildBadge(app_models.Badge badge) {
    final isEarned = badge.isEarned;
    return GestureDetector(
      onTap: () => _showBadgeDetails(badge),
      child: Card(
        color: isEarned ? AppColors.donkeyCard : Theme.of(context).cardColor,
        shape: RoundedRectangleBorder(
          side: BorderSide(
            color: isEarned ? AppColors.donkeyGold : Colors.transparent,
          ),
          borderRadius: BorderRadius.circular(8),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Opacity(
              opacity: isEarned ? 1.0 : 0.4,
              child: Text(
                badge.emoji,
                style: const TextStyle(fontSize: 36, inherit: true),
              ),
            ),
            const SizedBox(height: 8),
            Text(
              badge.name,
              style: TextStyle(color: AppColors.donkeyText, inherit: true),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final crossAxisCount = MediaQuery.of(context).size.width > 600 ? 3 : 2;
    return Scaffold(
      appBar: AppBar(
        title: FutureBuilder<List<app_models.Badge>>(
          future: _future,
          builder: (context, snapshot) {
            final count = snapshot.hasData
                ? snapshot.data!.where((b) => b.isEarned).length
                : 0;
            return Text('Badges ($count)');
          },
        ),
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ChoiceChip(
                  label: const Text('All'),
                  selected: !_earnedOnly,
                  onSelected: (_) => setState(() => _earnedOnly = false),
                ),
                const SizedBox(width: 8),
                ChoiceChip(
                  label: const Text('Earned Only'),
                  selected: _earnedOnly,
                  onSelected: (_) => setState(() => _earnedOnly = true),
                ),
              ],
            ),
          ),
          Expanded(
            child: RefreshIndicator(
              onRefresh: _refresh,
              child: FutureBuilder<List<app_models.Badge>>(
                future: _future,
                builder: (context, snapshot) {
                  if (snapshot.connectionState == ConnectionState.waiting) {
                    return const Center(child: CircularProgressIndicator());
                  } else if (snapshot.hasError) {
                    return Center(child: Text('Error: ${snapshot.error}'));
                  }

                  var badges = snapshot.data ?? [];
                  if (_earnedOnly) {
                    badges = badges.where((b) => b.isEarned).toList();
                  }

                  return GridView.builder(
                    padding: const EdgeInsets.all(16),
                    gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                      crossAxisCount: crossAxisCount,
                      mainAxisSpacing: 16,
                      crossAxisSpacing: 16,
                      childAspectRatio: 0.8,
                    ),
                    itemCount: badges.length,
                    itemBuilder: (context, index) => _buildBadge(badges[index]),
                  );
                },
              ),
            ),
          ),
        ],
      ),
    );
  }
}
