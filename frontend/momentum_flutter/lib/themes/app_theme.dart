import 'package:flutter/material.dart';

class AppColors {
  static const Color donkeyBlue = Color(0xFF0E7490);       // Primary theme color
  static const Color donkeyGold = Color(0xFFDAA520);       // Accent for badges, buttons
  static const Color donkeyBackground = Color(0xFF1F2937); // App background
  static const Color donkeyCard = Color(0xFF374151);       // Surface elements
  static const Color donkeyText = Color(0xFFF1F5F9);        // Main text color
}

class AppTheme {
  static ThemeData get theme {
    return ThemeData.dark().copyWith(
      scaffoldBackgroundColor: AppColors.donkeyBackground,
      cardColor: AppColors.donkeyCard,
      primaryColor: AppColors.donkeyBlue,
      hintColor: AppColors.donkeyGold,
      appBarTheme: AppBarTheme(
        backgroundColor: AppColors.donkeyCard,
        iconTheme: IconThemeData(color: AppColors.donkeyText),
        titleTextStyle: TextStyle(
          color: AppColors.donkeyText,
          fontWeight: FontWeight.bold,
          fontSize: 20,
        ),
      ),
      textTheme: ThemeData.dark().textTheme.apply(
            bodyColor: AppColors.donkeyText,
            displayColor: AppColors.donkeyText,
          ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.donkeyGold,
          foregroundColor: Colors.black,
          textStyle: TextStyle(fontWeight: FontWeight.bold),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: AppColors.donkeyCard,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8.0),
          borderSide: BorderSide(color: AppColors.donkeyGold),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8.0),
          borderSide: BorderSide(color: AppColors.donkeyGold, width: 2),
        ),
        labelStyle: TextStyle(color: AppColors.donkeyGold),
      ),
    );
  }
}