import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class ThemeProvider extends ChangeNotifier {
  static const _key = 'dark_mode';
  bool _isDark = false;

  bool get isDark => _isDark;

  ThemeProvider() {
    _load();
  }

  Future<void> _load() async {
    final prefs = await SharedPreferences.getInstance();
    _isDark = prefs.getBool(_key) ?? false;
    notifyListeners();
  }

  Future<void> toggle(bool value) async {
    _isDark = value;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_key, value);
  }

  // ─── Light Theme ───────────────────────────────────────
  static final light = ThemeData(
    brightness: Brightness.light,
    scaffoldBackgroundColor: const Color(0xFFF9FAFB),
    primaryColor: const Color(0xFF46166B),
    colorScheme: const ColorScheme.light(
      primary: Color(0xFF46166B),
      secondary: Color(0xFF5C2D91),
      surface: Colors.white,
      onSurface: Color(0xFF111827),
    ),
    appBarTheme: const AppBarTheme(
      backgroundColor: Color(0xFF46166B),
      foregroundColor: Colors.white,
    ),
    cardColor: Colors.white,
    dividerColor: Color(0xFFE5E7EB),
    bottomNavigationBarTheme: const BottomNavigationBarThemeData(
      backgroundColor: Colors.white,
      selectedItemColor: Color(0xFF46166B),
      unselectedItemColor: Color(0xFF9CA3AF),
    ),
  );

  // ─── Dark Theme ────────────────────────────────────────
  static final dark = ThemeData(
    brightness: Brightness.dark,
    scaffoldBackgroundColor: const Color(0xFF111827),
    primaryColor: const Color(0xFF46166B),
    colorScheme: const ColorScheme.dark(
      primary: Color(0xFF7C3AED),
      secondary: Color(0xFF5C2D91),
      surface: Color(0xFF1F2937),
      onSurface: Color(0xFFF9FAFB),
    ),
    appBarTheme: const AppBarTheme(
      backgroundColor: Color(0xFF1F2937),
      foregroundColor: Colors.white,
    ),
    cardColor: const Color(0xFF1F2937),
    dividerColor: const Color(0xFF374151),
    bottomNavigationBarTheme: const BottomNavigationBarThemeData(
      backgroundColor: Color(0xFF1F2937),
      selectedItemColor: Color(0xFF7C3AED),
      unselectedItemColor: Color(0xFF6B7280),
    ),
  );
}
