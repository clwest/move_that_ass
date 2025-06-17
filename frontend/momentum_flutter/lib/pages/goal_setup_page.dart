import 'package:flutter/material.dart';

import '../services/api_service.dart';
import 'today_page.dart';

class GoalSetupPage extends StatefulWidget {
  const GoalSetupPage({super.key});

  @override
  State<GoalSetupPage> createState() => _GoalSetupPageState();
}

class _GoalSetupPageState extends State<GoalSetupPage> {
  final TextEditingController _goalController = TextEditingController();
  final TextEditingController _targetController = TextEditingController(text: '1');

  Future<void> _save() async {
    final goal = _goalController.text.trim();
    final target = int.tryParse(_targetController.text) ?? 1;
    if (goal.isEmpty) return;
    await ApiService.setDailyGoal(goal, target);
    if (!mounted) return;
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (_) => const TodayPage()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Set Daily Goal')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: _goalController,
              decoration: const InputDecoration(labelText: 'Activity'),
            ),
            TextField(
              controller: _targetController,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(labelText: 'Target'),
            ),
            const SizedBox(height: 16),
            ElevatedButton(onPressed: _save, child: const Text('Save Goal')),
          ],
        ),
      ),
    );
  }
}
