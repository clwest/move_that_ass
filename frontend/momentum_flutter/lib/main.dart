import 'package:flutter/material.dart';

import 'pages/today_page.dart';
import 'themes/app_theme.dart';


void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MoveYourAzz',
      theme: AppTheme.theme,
      home: const TodayPage(),
    );
  }
}
