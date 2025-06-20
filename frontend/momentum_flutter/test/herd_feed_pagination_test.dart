import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:momentum_flutter/models/feed_item.dart';
import 'package:momentum_flutter/pages/herd_feed_page.dart';
import 'package:momentum_flutter/services/api_service.dart';
import 'package:infinite_scroll_pagination/infinite_scroll_pagination.dart';

void main() {
  const MethodChannel channel = MethodChannel('plugins.flutter.io/flutter_secure_storage');
  TestWidgetsFlutterBinding.ensureInitialized();
  channel.setMockMethodCallHandler((MethodCall methodCall) async => null);

  testWidgets('Scrolling fetches next page', (tester) async {
    bool calledPage2 = false;
    bool likeCalled = false;
    ApiService.fetchHerdFeedPage = (int page) async {
      if (page == 1) {
        return List.generate(
            10,
            (i) => FeedItem(
                id: i,
                type: 'meme',
                imageUrl: '',
                caption: 'c$i',
                likeCount: 0,
                likedByMe: false));
      }
      calledPage2 = true;
      return <FeedItem>[];
    };
    ApiService.toggleLike = (int id) async {
      likeCalled = true;
      return {'like_count': 1, 'liked_by_me': true};
    };

    await tester.pumpWidget(const MaterialApp(home: HerdFeedPage()));
    await tester.pumpAndSettle();

    await tester.drag(find.byType(PagedListView<int, FeedItem>), const Offset(0, -1000));
    await tester.pumpAndSettle();

    await tester.tap(find.byIcon(Icons.favorite_border).first);
    await tester.pump();

    expect(calledPage2, true);
    expect(likeCalled, true);
  });
}
