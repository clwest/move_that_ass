# momentum_flutter

A new Flutter project.

## Getting Started

This project is a starting point for a Flutter application.

A few resources to get you started if this is your first Flutter project:

- [Lab: Write your first Flutter app](https://docs.flutter.dev/get-started/codelab)
- [Cookbook: Useful Flutter samples](https://docs.flutter.dev/cookbook)

For help getting started with Flutter development, view the
[online documentation](https://docs.flutter.dev/), which offers tutorials,
samples, guidance on mobile development, and a full API reference.

## Configuration

The app reads the API base URL from the `API_BASE_URL` environment variable.
When running locally you can override it with:

```bash
flutter run --dart-define=API_BASE_URL=http://localhost:8000
```

If you programmatically embed the app you may also supply a `baseUrl` argument
to `main()` which will take precedence.
