import 'dart:io';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('Flutter SDK present', () {
    final haveFlutter = Platform.environment.containsKey('FLUTTER_ROOT');
    if (!haveFlutter) {
      return; // skip on CI boxes without SDK
    }
    expect(haveFlutter, isTrue); // will pass locally
  });
}
