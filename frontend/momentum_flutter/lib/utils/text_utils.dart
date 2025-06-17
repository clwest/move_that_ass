String cleanText(String input) {
  return input
      .replaceAll('â€™', "'")
      .replaceAll('â€“', "-")
      .replaceAll('â€œ', '"')
      .replaceAll('â€', '"')
      .replaceAll('â', "'")
      .replaceAll('▒', '')
      .replaceAll(RegExp(r'[^\x00-\x7F]'), '');
}

