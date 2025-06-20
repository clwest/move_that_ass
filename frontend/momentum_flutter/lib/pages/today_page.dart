import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:intl/intl.dart';

import '../models/dashboard_item.dart';
import '../services/api_service.dart';
import '../models/daily_goal.dart';
import 'badge_grid_page.dart';
import '../utils/text_utils.dart';
import 'herd_feed_page.dart';
import 'profile_page.dart';
import 'meme_share_page.dart';
import '../services/auth_service.dart';
import 'login_page.dart';
import '../themes/app_theme.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'voice_journal_page.dart';
import 'package:image_picker/image_picker.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:url_launcher/url_launcher.dart';
import '../services/task_poller.dart';

class TodayPage extends StatefulWidget {
  const TodayPage({super.key});

  @override
  State<TodayPage> createState() => _TodayPageState();
}

class _TodayPageState extends State<TodayPage> {
  late Future<void> _future;

  List<DashboardItem> _items = [];
  DailyGoal? _dailyGoal;
  final ImagePicker _picker = ImagePicker();

  final TextEditingController _goalController = TextEditingController();
  final TextEditingController _targetController = TextEditingController(text: '1');

  @override
  void initState() {
    super.initState();
    _future = _loadAll();
    Future(() async {
      final prefs = await SharedPreferences.getInstance();
      final shown = prefs.getBool('has_seen_welcome') ?? false;
      if (!shown && mounted) {
        await showDialog(
          context: context,
          builder: (context) => AlertDialog(
            title: const Text('Welcome to MoveYourAzz 🫏'),
            content: const Text('Move that azz and share your progress!'),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(context),
                child: const Text('Let\'s go'),
              ),
            ],
          ),
        );
        await prefs.setBool('has_seen_welcome', true);
      }
    });

  }

  Future<void> _loadAll() async {
    final results = await Future.wait([
      ApiService.fetchProfile(),
      ApiService.fetchDailyGoal(),
      ApiService.fetchDashboard(),
    ]);
    if (!mounted) return;
    _dailyGoal = results[1] as DailyGoal?;
    _items = results[2] as List<DashboardItem>;
  }

  Future<void> _refresh() async {
    setState(() {
      _future = _loadAll();
    });
  }

  Future<void> _showImageOptions() async {
    showModalBottomSheet(
      context: context,
      builder: (context) => SafeArea(
        child: Wrap(
          children: [
            ListTile(
              leading: const Icon(Icons.camera_alt),
              title: const Text('Take photo'),
              onTap: () async {
                Navigator.pop(context);
                final status = await Permission.camera.request();
                if (!status.isGranted) {
                  if (!mounted) return;
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Camera permission needed')),
                  );
                  return;
                }
                final file = await _picker.pickImage(source: ImageSource.camera);
                if (file != null) {
                  await _handleImage(file);
                }
              },
            ),
            ListTile(
              leading: const Icon(Icons.photo_library),
              title: const Text('Choose from gallery'),
              onTap: () async {
                Navigator.pop(context);
                final status = await Permission.photos.request();
                if (!status.isGranted) {
                  if (!mounted) return;
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Camera permission needed')),
                  );
                  return;
                }
                final file = await _picker.pickImage(source: ImageSource.gallery);
                if (file != null) {
                  await _handleImage(file);
                }
              },
            ),
          ],
        ),
      ),
    );
  }

  Future<void> _handleImage(XFile file) async {
    String id;
    try {
      id = await ApiService.uploadImage('/api/vision/identify/', file);
    } on UnauthorizedException {
      if (!mounted) return;
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (_) => const LoginPage()),
      );
      return;
    }
    final result = await TaskPoller.poll(id);
    if (!mounted) return;
    final data = jsonDecode(result['data'] as String) as Map<String, dynamic>;
    showModalBottomSheet(
      context: context,
      builder: (context) => SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('🏷  Name: ${data['label']}'),
              Text('☠️ Dangerous: ${data['is_dangerous'] ? 'Yes' : 'No'}'),
              InkWell(
                onTap: () => launchUrl(Uri.parse(data['wiki_url'] as String)),
                child: const Text('🔗 Wikipedia', style: TextStyle(color: Colors.blue)),
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('MoveYourAzz 🫏'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () async {
              await AuthService.logout();
              if (!mounted) return;
              Navigator.pushReplacement(
                context,
                MaterialPageRoute(builder: (_) => const LoginPage()),
              );
            },
          ),
          IconButton(
            icon: const Icon(Icons.emoji_events),
            onPressed: () {
              Navigator.of(context).push(
                MaterialPageRoute(
                  builder: (_) => const BadgeGridPage(),
                ),
              );
            },
          ),
          IconButton(
            icon: const Icon(Icons.group),
            onPressed: () {
              Navigator.of(context).push(
                MaterialPageRoute(
                  builder: (_) => const HerdFeedPage(),
                ),
              );
            },
          ),
          IconButton(
            icon: const Icon(Icons.mic),
            onPressed: () async {
              final result = await Navigator.of(context)
                  .pushNamed(VoiceJournalPage.routeName);
              if (result == true && mounted) {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Journal uploaded!')),
                );
                await _refresh();
              }
            },
          ),
          IconButton(
            icon: const Icon(Icons.person),
            onPressed: () {
              Navigator.of(context).push(
                MaterialPageRoute(
                  builder: (_) => const ProfilePage(),
                ),
              );
            },
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: _refresh,
        child: FutureBuilder<void>(
          future: _future,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator());
            } else if (snapshot.hasError) {
              return Center(child: Text('Error: ${snapshot.error}'));
            }
            final items = _items;
            return ListView(
              padding: const EdgeInsets.all(16),
              children: [
                _buildGoalCard(),
                ...items.map(_buildItem).toList(),
              ],
            );
          },
        ),
      ),
      floatingActionButton: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          FloatingActionButton(
            heroTag: 'vision',
            backgroundColor: Colors.purple,
            onPressed: _showImageOptions,
            child: const Icon(Icons.camera_alt),
          ),
          const SizedBox(height: 12),
          FloatingActionButton(
            heroTag: 'meme',
            onPressed: () async {
              final meme = await ApiService.generateMeme();
              if (!mounted) return;
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => MemeSharePage(meme: meme)),
              );
            },
            child: const Icon(Icons.image),
            backgroundColor: AppColors.donkeyGold,
          ),
        ],
      ),
    );
  }

  Future<void> _saveGoal() async {
    final goal = _goalController.text.trim();
    final target = int.tryParse(_targetController.text) ?? 1;
    if (goal.isEmpty) return;
    await ApiService.setDailyGoal(goal, target);
    if (mounted) {
      await _refresh();
    }
  }

  Widget _buildGoalCard() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Set Your Goal'),
            const SizedBox(height: 8),
            TextField(
              controller: _goalController,
              decoration: const InputDecoration(labelText: 'Activity'),
            ),
            const SizedBox(height: 8),
            TextField(
              controller: _targetController,
              decoration: const InputDecoration(labelText: 'Target'),
              keyboardType: TextInputType.number,
            ),
            const SizedBox(height: 8),
            ElevatedButton(
              onPressed: _saveGoal,
              child:
                  Text('Save Goal', style: Theme.of(context).textTheme.labelLarge),
            ),
            if (_dailyGoal != null)
              Padding(
                padding: const EdgeInsets.only(top: 8),
                child: Text(
                    'Today\'s goal: ${_dailyGoal!.goal} x${_dailyGoal!.target}'),
              ),
          ],
        ),

      ),
    );
  }

}

  Widget _buildItem(DashboardItem item) {
    Widget content;
    switch (item.type) {
      case 'meme':
        content = Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if ((item.content['image_url'] as String?)?.isNotEmpty ?? false)
              Image.network(item.content['image_url'] as String),
            if (item.content['caption'] != null) ...[
              const SizedBox(height: 8),
              Text(cleanText(item.content['caption'])),
            ],
          ],
        );
        break;
      case 'shame':
        content = Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if ((item.content['image_url'] as String?)?.isNotEmpty ?? false)
              Image.network(item.content['image_url'] as String),
            if (item.content['text'] != null) ...[
              const SizedBox(height: 8),
              Text(cleanText(item.content['text'])),
            ],
          ],
        );
        break;
      case 'voice':
        content = Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (item.content['text'] != null)
              Text(cleanText(item.content['text'])),
            if ((item.content['tags'] as List?)?.isNotEmpty ?? false) ...[
              const SizedBox(height: 4),
              Wrap(
                spacing: 4,
                children: [
                  ...(item.content['tags'] as List)
                      .map((t) => Chip(label: Text(cleanText(t.toString()))))
                ],
              ),
            ],
          ],
        );
        break;
      default:
        content = Text(item.content.toString());
    }

    final ts = DateFormat.yMMMd().add_jm().format(item.createdAt);

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(ts, style: Theme.of(context).textTheme.bodySmall),
            const SizedBox(height: 8),
            content,
          ],
        ),
      ),
    );
  }
}
