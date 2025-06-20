import 'package:flutter/material.dart';

import '../services/api_service.dart';
import '../main.dart';

class GoalSetupPage extends StatefulWidget {
  const GoalSetupPage({super.key});

  @override
  State<GoalSetupPage> createState() => _GoalSetupPageState();
}

class _GoalSetupPageState extends State<GoalSetupPage> {
  final GlobalKey<FormState> _goalFormKey = GlobalKey<FormState>();
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
      MaterialPageRoute(builder: (_) => const MyApp()),
    );
  }

  @override
  void dispose() {
    _goalController.dispose();
    _targetController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Set Daily Goal')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _goalFormKey,
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
              ElevatedButton(
                onPressed: _save,
                child:
                    Text('Save Goal', style: Theme.of(context).textTheme.labelLarge),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
