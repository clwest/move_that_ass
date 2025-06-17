import 'package:flutter/material.dart';

import '../models/profile.dart';
import '../services/api_service.dart';
import '../services/token_service.dart';
import 'badge_grid_page.dart';
import 'login_page.dart';

class ProfilePage extends StatefulWidget {
  const ProfilePage({super.key});

  @override
  State<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  late Future<UserProfile> _future;
  bool _editing = false;
  final _nameController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _future = ApiService.fetchProfile();
  }

  Future<void> _refresh() async {
    setState(() => _future = ApiService.fetchProfile());
  }

  Future<void> _saveName() async {
    final newName = _nameController.text.trim();
    final updated = await ApiService.updateDisplayName(newName);
    setState(() {
      _editing = false;
      _future = Future.value(updated);
    });
  }

  @override
  void dispose() {
    _nameController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('My Profile 🫏')),
      body: RefreshIndicator(
        onRefresh: _refresh,
        child: FutureBuilder<UserProfile>(
          future: _future,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator());
            } else if (snapshot.hasError) {
              return Center(child: Text('Error: ${snapshot.error}'));
            }

            final profile = snapshot.data!;
            _nameController.text = profile.displayName;
            return ListView(
              padding: const EdgeInsets.all(16),
              children: [
                Card(
                  child: ListTile(
                    leading: Text(
                      profile.moodAvatar.isNotEmpty ? profile.moodAvatar : '😶',
                      style: const TextStyle(fontSize: 32, inherit: true),
                    ),
                    title: Text('Current Mood: ${profile.mood}'),
                  ),
                ),
                const SizedBox(height: 12),
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Row(
                      children: [
                        Expanded(
                          child: TextField(
                            controller: _nameController,
                            readOnly: !_editing,
                            decoration:
                                const InputDecoration(labelText: 'Display Name'),
                          ),
                        ),
                        IconButton(
                          icon: Icon(_editing ? Icons.save : Icons.edit),
                          onPressed: () {
                            if (_editing) {
                              _saveName();
                            } else {
                              setState(() => _editing = true);
                            }
                          },
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 12),
                Card(
                  child: ListTile(
                    title: Text(
                      profile.herdName != null
                          ? 'Member of: ${profile.herdName} (${profile.herdSize} members)'
                          : 'Not in a herd',
                    ),
                  ),
                ),
                const SizedBox(height: 12),
                Card(
                  child: ListTile(
                    title: Text('You\'ve unlocked ${profile.badges} badges'),
                    trailing: TextButton(
                      onPressed: () {
                        Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (_) => const BadgeGridPage(),
                          ),
                        );
                      },
                      child: const Text('View Badges'),
                    ),
                  ),
                ),
                const SizedBox(height: 20),
                ElevatedButton(
                  onPressed: () async {
                    await TokenService.clearToken();
                    if (!mounted) return;
                    Navigator.pushReplacement(
                      context,
                      MaterialPageRoute(builder: (_) => const LoginPage()),
                    );
                  },
                  child: const Text('Logout'),
                ),
              ],
            );
          },
        ),
      ),
    );
  }
}
