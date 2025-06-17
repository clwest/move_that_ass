import 'package:flutter/material.dart';

import 'pages/today_page.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MoveYourAzz',
      theme: ThemeData.dark(),
      home: const TodayPage(),
    );
  }
}
