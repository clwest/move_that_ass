import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import '../models/today_dashboard.dart';
import '../services/api_service.dart';
import 'badge_grid_page.dart';
import 'herd_feed_page.dart';
import 'profile_page.dart';
import 'meme_share_page.dart';
import '../services/token_service.dart';
import 'login_page.dart';

class TodayPage extends StatefulWidget {
  const TodayPage({super.key});

  @override
  State<TodayPage> createState() => _TodayPageState();
}

class _TodayPageState extends State<TodayPage> {
  late Future<TodayDashboard> _future;

  Map<String, dynamic>? _dailyGoal;

  final TextEditingController _goalController = TextEditingController();
  final TextEditingController _targetController = TextEditingController(text: '1');

  @override
  void initState() {
    super.initState();
    _future = ApiService.fetchTodayDashboard();

    ApiService.fetchDailyGoal().then((data) {
      if (data != null) {
        setState(() {
          _dailyGoal = data;
        });
      }
    });
    Future.delayed(Duration.zero, () {
      showDialog(
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
    });

  }

  Future<void> _loadGoal() async {
    final data = await ApiService.fetchDailyGoal();
    if (!mounted) return;
    setState(() {
      _dailyGoal = data;
    });
  }

  Future<void> _refresh() async {
    setState(() {
      _future = ApiService.fetchTodayDashboard();
    });
    await _loadGoal();
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
              await TokenService.clearToken();
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
        child: FutureBuilder<TodayDashboard>(
          future: _future,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator());
            } else if (snapshot.hasError) {
              return Center(child: Text('Error: ${snapshot.error}'));
            }

            final dashboard = snapshot.data!;
            return ListView(
              padding: const EdgeInsets.all(16),
              children: [
                _buildGoalCard(),
                _buildMood(dashboard),
                _buildChallenge(dashboard.challenge),
                _buildWorkout(dashboard.workoutPlan),
                _buildMeal(dashboard.mealPlan),
                _buildRecap(dashboard.recap),
              ],
            );
          },
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          try {
            final meme = await ApiService.generateMeme();
            if (!mounted) return;
            Navigator.of(context).push(
              MaterialPageRoute(
                builder: (_) => MemeSharePage(meme: meme),
              ),
            );
          } catch (e) {
            if (!mounted) return;
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Failed to generate meme')),
            );
          }
        },

        child: const Icon(Icons.photo),
      ),
    );
  }

  Future<void> _saveGoal() async {
    final goal = _goalController.text.trim();
    final target = int.tryParse(_targetController.text) ?? 1;
    if (goal.isEmpty) return;
    await ApiService.setDailyGoal(goal, target);
    if (mounted) {
      setState(() {
        _dailyGoal = {'goal': goal, 'target': target};
      });
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
              child: const Text('Save Goal'),
            ),
            if (_dailyGoal != null)
              Padding(
                padding: const EdgeInsets.only(top: 8),
                child: Text(
                    'Today\'s goal: ${_dailyGoal!['goal']} x${_dailyGoal!['target']}'),
              ),
          ],
        ),

      ),
    );
  }

  Widget _buildMood(TodayDashboard dashboard) {
    return Card(
      child: ListTile(
        leading: Text(
          dashboard.moodAvatar.isNotEmpty ? dashboard.moodAvatar : '😶',
          style: const TextStyle(fontSize: 32, inherit: true),
        ),
        title: Text('Current Mood: ${dashboard.mood}'),
      ),
    );
  }

  Widget _buildChallenge(Challenge? challenge) {
    if (challenge == null) {
      return const SizedBox.shrink();
    }
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              challenge.text,
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 8),
            Text(
              'Deadline: ${DateFormat.yMMMMd().add_jm().format(challenge.expiresAt)}',
              style: Theme.of(context).textTheme.bodySmall,
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                ElevatedButton(
                  onPressed: () {},
                  child: const Text('Mark Complete'),
                ),
                const SizedBox(width: 8),
                OutlinedButton(
                  onPressed: () {},
                  child: const Text('Share to Herd'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildWorkout(List<String>? plan) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Workout Plan',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 8),
            if (plan == null || plan.isEmpty)
              const Text('No plan set today')
            else
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: plan.map((e) => Text(e)).toList(),
              ),
          ],
        ),
      ),
    );
  }

  Widget _buildMeal(Map<String, dynamic>? mealPlan) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Meal Plan',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 8),
            if (mealPlan == null || mealPlan.isEmpty)
              const Text('No meal plan today')
            else
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  if (mealPlan['breakfast'] != null)
                    Text('🍳 Breakfast: ${mealPlan['breakfast']}'),
                  if (mealPlan['lunch'] != null)
                    Text('🥪 Lunch: ${mealPlan['lunch']}'),
                  if (mealPlan['dinner'] != null)
                    Text('🍜 Dinner: ${mealPlan['dinner']}'),
                  if (mealPlan['snacks'] != null) ...[
                    const Text('🍏 Snacks:'),
                    ...List<Widget>.from(
                      (mealPlan['snacks'] as List).map((s) => Text('• $s')),
                    ),
                  ],
                ],
              ),
          ],
        ),
      ),
    );
  }

  Widget _buildRecap(String recap) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Donkey Recap',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 8),
            Text(
              recap,
              style: const TextStyle(fontStyle: FontStyle.italic, inherit: true),
            ),
          ],
        ),
      ),
    );
  }

}
