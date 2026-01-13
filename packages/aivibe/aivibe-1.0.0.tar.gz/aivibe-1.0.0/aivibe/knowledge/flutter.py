"""
Flutter Knowledge Module

Complete Flutter 3.24+ knowledge including:
- Widget architecture and lifecycle
- State management patterns
- Platform integrations (iOS 18, Android API 36, Web)
- Performance optimization
- Production-ready patterns
"""


class FlutterKnowledge:
    """Complete Flutter expertise for AI agent training."""

    VERSION = "3.24.0"
    MIN_IOS_VERSION = "13.0"
    MIN_ANDROID_SDK = "24"
    TARGET_IOS_SDK = "18.0"
    TARGET_ANDROID_API = "36"

    # =========================================================================
    # CORE WIDGET PATTERNS
    # =========================================================================

    WIDGET_PATTERNS = {
        "stateless_widget": '''
/// CORRECT: Stateless widget with const constructor
class UserAvatar extends StatelessWidget {
  final String imageUrl;
  final double size;
  final VoidCallback? onTap;

  const UserAvatar({
    super.key,
    required this.imageUrl,
    this.size = 48.0,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: CircleAvatar(
        radius: size / 2,
        backgroundImage: CachedNetworkImageProvider(imageUrl),
      ),
    );
  }
}
''',
        "stateful_widget": '''
/// CORRECT: Stateful widget with proper lifecycle
class AnimatedCounter extends StatefulWidget {
  final int value;
  final Duration duration;

  const AnimatedCounter({
    super.key,
    required this.value,
    this.duration = const Duration(milliseconds: 300),
  });

  @override
  State<AnimatedCounter> createState() => _AnimatedCounterState();
}

class _AnimatedCounterState extends State<AnimatedCounter>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<int> _animation;
  int _previousValue = 0;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this, duration: widget.duration);
    _updateAnimation();
  }

  @override
  void didUpdateWidget(AnimatedCounter oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.value != widget.value) {
      _previousValue = oldWidget.value;
      _updateAnimation();
      _controller.forward(from: 0);
    }
  }

  void _updateAnimation() {
    _animation = IntTween(begin: _previousValue, end: widget.value)
        .animate(CurvedAnimation(parent: _controller, curve: Curves.easeOut));
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _animation,
      builder: (context, child) => Text(
        _animation.value.toString(),
        style: Theme.of(context).textTheme.headlineLarge,
      ),
    );
  }
}
''',
        "hook_widget": '''
/// CORRECT: Flutter Hooks pattern (with hooks_riverpod)
class UserProfileScreen extends HookConsumerWidget {
  final String userId;

  const UserProfileScreen({super.key, required this.userId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final userAsync = ref.watch(userProvider(userId));
    final isEditing = useState(false);
    final formKey = useMemoized(() => GlobalKey<FormState>());

    return Scaffold(
      appBar: AppBar(
        title: const Text('Profile'),
        actions: [
          IconButton(
            icon: Icon(isEditing.value ? Icons.check : Icons.edit),
            onPressed: () => isEditing.value = !isEditing.value,
          ),
        ],
      ),
      body: userAsync.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, st) => ErrorWidget(error: e.toString()),
        data: (user) => UserProfileForm(
          key: formKey,
          user: user,
          enabled: isEditing.value,
        ),
      ),
    );
  }
}
''',
    }

    # =========================================================================
    # STATE MANAGEMENT (RIVERPOD 2.x)
    # =========================================================================

    STATE_MANAGEMENT = {
        "provider_types": {
            "Provider": "For computed/derived values that don't change",
            "StateProvider": "For simple mutable state",
            "FutureProvider": "For async values loaded once",
            "StreamProvider": "For real-time data streams",
            "NotifierProvider": "For complex mutable state with methods",
            "AsyncNotifierProvider": "For complex async state with methods",
        },
        "notifier_pattern": '''
/// CORRECT: AsyncNotifier for complex async state
@riverpod
class UserNotifier extends _$UserNotifier {
  @override
  FutureOr<User?> build() => null;

  Future<void> loadUser(String userId) async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      final repository = ref.read(userRepositoryProvider);
      return repository.getUser(userId);
    });
  }

  Future<void> updateProfile(UserUpdate update) async {
    final currentUser = state.valueOrNull;
    if (currentUser == null) return;

    // Optimistic update
    state = AsyncData(currentUser.copyWith(
      name: update.name ?? currentUser.name,
      bio: update.bio ?? currentUser.bio,
    ));

    try {
      final repository = ref.read(userRepositoryProvider);
      final updated = await repository.updateUser(currentUser.id, update);
      state = AsyncData(updated);
    } catch (e, st) {
      // Revert on failure
      state = AsyncData(currentUser);
      state = AsyncError(e, st);
    }
  }

  Future<void> logout() async {
    await ref.read(authServiceProvider).logout();
    state = const AsyncData(null);
    ref.invalidate(authStateProvider);
  }
}
''',
        "family_provider": '''
/// CORRECT: Family provider for parameterized data
@riverpod
Future<Post> post(PostRef ref, String postId) async {
  final repository = ref.watch(postRepositoryProvider);

  // Auto-dispose after 5 minutes of no listeners
  ref.keepAlive();
  final timer = Timer(const Duration(minutes: 5), () {
    ref.invalidateSelf();
  });
  ref.onDispose(timer.cancel);

  return repository.getPost(postId);
}

/// Usage in widget
final postAsync = ref.watch(postProvider(postId));
''',
    }

    # =========================================================================
    # NAVIGATION (GO_ROUTER)
    # =========================================================================

    NAVIGATION = {
        "router_config": '''
/// CORRECT: GoRouter configuration with guards
final goRouter = GoRouter(
  initialLocation: '/',
  debugLogDiagnostics: kDebugMode,
  refreshListenable: authNotifier,
  redirect: (context, state) {
    final isAuthenticated = authNotifier.isAuthenticated;
    final isAuthRoute = state.matchedLocation.startsWith('/auth');

    if (!isAuthenticated && !isAuthRoute) {
      return '/auth/login?redirect=${state.matchedLocation}';
    }
    if (isAuthenticated && isAuthRoute) {
      return state.uri.queryParameters['redirect'] ?? '/home';
    }
    return null;
  },
  routes: [
    GoRoute(
      path: '/',
      redirect: (_, __) => '/home',
    ),
    ShellRoute(
      builder: (context, state, child) => MainShell(child: child),
      routes: [
        GoRoute(
          path: '/home',
          name: 'home',
          pageBuilder: (context, state) => NoTransitionPage(
            key: state.pageKey,
            child: const HomeScreen(),
          ),
        ),
        GoRoute(
          path: '/profile/:userId',
          name: 'profile',
          builder: (context, state) => ProfileScreen(
            userId: state.pathParameters['userId']!,
          ),
        ),
      ],
    ),
    GoRoute(
      path: '/auth/login',
      name: 'login',
      builder: (context, state) => const LoginScreen(),
    ),
  ],
  errorBuilder: (context, state) => ErrorScreen(error: state.error),
);
''',
        "deep_linking": '''
/// CORRECT: Deep link handling
class DeepLinkHandler {
  static final _uniLinks = UniLinks();

  static Future<void> init() async {
    // Handle initial deep link
    try {
      final initialLink = await _uniLinks.getInitialLink();
      if (initialLink != null) {
        _handleDeepLink(initialLink);
      }
    } catch (e) {
      debugPrint('Failed to get initial link: $e');
    }

    // Listen for new deep links
    _uniLinks.linkStream.listen(
      _handleDeepLink,
      onError: (e) => debugPrint('Deep link error: $e'),
    );
  }

  static void _handleDeepLink(String link) {
    final uri = Uri.parse(link);
    final path = uri.path;

    // Navigate using GoRouter
    goRouter.go(path);
  }
}
''',
    }

    # =========================================================================
    # FORM HANDLING
    # =========================================================================

    FORMS = {
        "form_pattern": '''
/// CORRECT: Form with validation and state management
class LoginForm extends ConsumerStatefulWidget {
  const LoginForm({super.key});

  @override
  ConsumerState<LoginForm> createState() => _LoginFormState();
}

class _LoginFormState extends ConsumerState<LoginForm> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _obscurePassword = true;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _handleSubmit() async {
    if (!_formKey.currentState!.validate()) return;

    final authNotifier = ref.read(authNotifierProvider.notifier);
    try {
      await authNotifier.login(
        email: _emailController.text.trim(),
        password: _passwordController.text,
      );
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(e.toString())),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final authState = ref.watch(authNotifierProvider);
    final isLoading = authState.isLoading;

    return Form(
      key: _formKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          TextFormField(
            controller: _emailController,
            decoration: const InputDecoration(
              labelText: 'Email',
              prefixIcon: Icon(Icons.email_outlined),
            ),
            keyboardType: TextInputType.emailAddress,
            textInputAction: TextInputAction.next,
            autocorrect: false,
            validator: Validators.email,
            enabled: !isLoading,
          ),
          const SizedBox(height: 16),
          TextFormField(
            controller: _passwordController,
            decoration: InputDecoration(
              labelText: 'Password',
              prefixIcon: const Icon(Icons.lock_outlined),
              suffixIcon: IconButton(
                icon: Icon(
                  _obscurePassword ? Icons.visibility : Icons.visibility_off,
                ),
                onPressed: () => setState(() => _obscurePassword = !_obscurePassword),
              ),
            ),
            obscureText: _obscurePassword,
            textInputAction: TextInputAction.done,
            validator: Validators.password,
            enabled: !isLoading,
            onFieldSubmitted: (_) => _handleSubmit(),
          ),
          const SizedBox(height: 24),
          FilledButton(
            onPressed: isLoading ? null : _handleSubmit,
            child: isLoading
                ? const SizedBox(
                    height: 20,
                    width: 20,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  )
                : const Text('Sign In'),
          ),
        ],
      ),
    );
  }
}
''',
        "validators": '''
/// CORRECT: Reusable validators
class Validators {
  static String? required(String? value) {
    if (value == null || value.trim().isEmpty) {
      return 'This field is required';
    }
    return null;
  }

  static String? email(String? value) {
    if (value == null || value.isEmpty) {
      return 'Email is required';
    }
    final emailRegex = RegExp(r'^[\\w-.]+@([\\w-]+\\.)+[\\w-]{2,}$');
    if (!emailRegex.hasMatch(value)) {
      return 'Enter a valid email address';
    }
    return null;
  }

  static String? password(String? value) {
    if (value == null || value.isEmpty) {
      return 'Password is required';
    }
    if (value.length < 8) {
      return 'Password must be at least 8 characters';
    }
    if (!RegExp(r'[A-Z]').hasMatch(value)) {
      return 'Password must contain an uppercase letter';
    }
    if (!RegExp(r'[a-z]').hasMatch(value)) {
      return 'Password must contain a lowercase letter';
    }
    if (!RegExp(r'[0-9]').hasMatch(value)) {
      return 'Password must contain a number';
    }
    return null;
  }

  static String? phone(String? value) {
    if (value == null || value.isEmpty) {
      return 'Phone number is required';
    }
    final phoneRegex = RegExp(r'^\\+?[1-9]\\d{6,14}$');
    if (!phoneRegex.hasMatch(value.replaceAll(RegExp(r'[\\s-]'), ''))) {
      return 'Enter a valid phone number';
    }
    return null;
  }

  static String? Function(String?) minLength(int min) {
    return (value) {
      if (value == null || value.length < min) {
        return 'Must be at least $min characters';
      }
      return null;
    };
  }

  static String? Function(String?) maxLength(int max) {
    return (value) {
      if (value != null && value.length > max) {
        return 'Must be no more than $max characters';
      }
      return null;
    };
  }
}
''',
    }

    # =========================================================================
    # API INTEGRATION
    # =========================================================================

    API_PATTERNS = {
        "dio_client": '''
/// CORRECT: Dio HTTP client with interceptors
class ApiClient {
  late final Dio _dio;
  final TokenStorage _tokenStorage;

  ApiClient({required TokenStorage tokenStorage})
      : _tokenStorage = tokenStorage {
    _dio = Dio(
      BaseOptions(
        baseUrl: Environment.apiBaseUrl,
        connectTimeout: const Duration(seconds: 30),
        receiveTimeout: const Duration(seconds: 30),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      ),
    );

    _dio.interceptors.addAll([
      _AuthInterceptor(_tokenStorage),
      _LoggingInterceptor(),
      _ErrorInterceptor(),
      _RetryInterceptor(_dio),
    ]);
  }

  Future<T> get<T>(
    String path, {
    Map<String, dynamic>? queryParameters,
    T Function(dynamic)? fromJson,
  }) async {
    final response = await _dio.get(path, queryParameters: queryParameters);
    return fromJson != null ? fromJson(response.data) : response.data as T;
  }

  Future<T> post<T>(
    String path, {
    dynamic data,
    T Function(dynamic)? fromJson,
  }) async {
    final response = await _dio.post(path, data: data);
    return fromJson != null ? fromJson(response.data) : response.data as T;
  }

  Future<T> put<T>(
    String path, {
    dynamic data,
    T Function(dynamic)? fromJson,
  }) async {
    final response = await _dio.put(path, data: data);
    return fromJson != null ? fromJson(response.data) : response.data as T;
  }

  Future<void> delete(String path) async {
    await _dio.delete(path);
  }
}
''',
        "auth_interceptor": '''
/// CORRECT: Auth interceptor with token refresh
class _AuthInterceptor extends Interceptor {
  final TokenStorage _tokenStorage;
  bool _isRefreshing = false;
  final _refreshCompleter = <Completer<String>>[];

  _AuthInterceptor(this._tokenStorage);

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    final token = _tokenStorage.accessToken;
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    handler.next(options);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) async {
    if (err.response?.statusCode == 401) {
      try {
        final newToken = await _refreshToken();
        err.requestOptions.headers['Authorization'] = 'Bearer $newToken';

        final response = await Dio().fetch(err.requestOptions);
        handler.resolve(response);
        return;
      } catch (e) {
        _tokenStorage.clear();
        handler.reject(err);
        return;
      }
    }
    handler.next(err);
  }

  Future<String> _refreshToken() async {
    if (_isRefreshing) {
      final completer = Completer<String>();
      _refreshCompleter.add(completer);
      return completer.future;
    }

    _isRefreshing = true;
    try {
      final refreshToken = _tokenStorage.refreshToken;
      if (refreshToken == null) throw Exception('No refresh token');

      final response = await Dio().post(
        '${Environment.apiBaseUrl}/auth/refresh',
        data: {'refresh_token': refreshToken},
      );

      final newToken = response.data['access_token'] as String;
      _tokenStorage.accessToken = newToken;

      for (final completer in _refreshCompleter) {
        completer.complete(newToken);
      }
      _refreshCompleter.clear();

      return newToken;
    } finally {
      _isRefreshing = false;
    }
  }
}
''',
    }

    # =========================================================================
    # PLATFORM INTEGRATIONS
    # =========================================================================

    PLATFORM_INTEGRATIONS = {
        "ios_18_features": '''
/// iOS 18 SDK Features
// 1. Live Activities
import ActivityKit

extension LiveActivityManager {
  func startOrderTracking(order: Order) async throws -> Activity<OrderActivityAttributes> {
    let attributes = OrderActivityAttributes(orderId: order.id)
    let state = OrderActivityAttributes.ContentState(
      status: .preparing,
      estimatedDelivery: order.estimatedDelivery
    )
    return try Activity.request(attributes: attributes, content: .init(state: state, staleDate: nil))
  }
}

// 2. App Intents (Siri/Shortcuts)
@available(iOS 16.0, *)
struct OrderFoodIntent: AppIntent {
  static var title: LocalizedStringResource = "Order Food"

  @Parameter(title: "Restaurant")
  var restaurant: RestaurantEntity

  func perform() async throws -> some IntentResult {
    // Implementation
  }
}

// 3. Widget Extensions
struct OrderTrackingWidget: Widget {
  var body: some WidgetConfiguration {
    ActivityConfiguration(for: OrderActivityAttributes.self) { context in
      OrderTrackingView(state: context.state)
    } dynamicIsland: { context in
      DynamicIsland {
        // Expanded regions
      } compactLeading: {
        // Compact leading
      } compactTrailing: {
        // Compact trailing
      } minimal: {
        // Minimal view
      }
    }
  }
}
''',
        "android_api_36": '''
/// Android API 36 Features
// 1. Predictive Back Gesture
class MainActivity : FlutterFragmentActivity() {
  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)

    // Enable predictive back
    onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
      override fun handleOnBackPressed() {
        // Handle back with animation preview
      }
    })
  }
}

// 2. Per-App Language Preferences
val appLocale = LocaleListCompat.forLanguageTags("hi")
AppCompatDelegate.setApplicationLocales(appLocale)

// 3. Photo Picker
val pickMedia = registerForActivityResult(ActivityResultContracts.PickVisualMedia()) { uri ->
  if (uri != null) {
    // Handle selected media
  }
}
pickMedia.launch(PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageAndVideo))

// 4. Credential Manager (Passkeys)
val credentialManager = CredentialManager.create(context)
val request = GetCredentialRequest(listOf(
  GetPasswordOption(),
  GetPublicKeyCredentialOption(requestJson)
))
''',
        "platform_channels": '''
/// CORRECT: Platform channel implementation
// Dart side
class NativeFeatures {
  static const _channel = MethodChannel('com.vibekaro.app/native');
  static const _eventChannel = EventChannel('com.vibekaro.app/events');

  /// Get device haptic feedback
  static Future<void> hapticFeedback(HapticType type) async {
    await _channel.invokeMethod('hapticFeedback', {'type': type.name});
  }

  /// Stream battery level updates
  static Stream<int> get batteryLevelStream {
    return _eventChannel
        .receiveBroadcastStream()
        .map((event) => event as int);
  }

  /// Get biometric authentication
  static Future<bool> authenticateWithBiometrics({
    required String reason,
  }) async {
    try {
      final result = await _channel.invokeMethod<bool>(
        'authenticateWithBiometrics',
        {'reason': reason},
      );
      return result ?? false;
    } on PlatformException catch (e) {
      if (e.code == 'NOT_AVAILABLE') {
        throw BiometricNotAvailableException();
      }
      rethrow;
    }
  }
}

enum HapticType { light, medium, heavy, selection, success, warning, error }
''',
    }

    # =========================================================================
    # PERFORMANCE OPTIMIZATION
    # =========================================================================

    PERFORMANCE = {
        "widget_optimization": '''
/// CORRECT: Optimized widget patterns
// 1. Use const constructors
class OptimizedCard extends StatelessWidget {
  final String title;
  final String subtitle;

  const OptimizedCard({
    super.key,
    required this.title,
    required this.subtitle,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16), // const!
        child: Column(
          children: [
            Text(title),
            const SizedBox(height: 8), // const!
            Text(subtitle),
          ],
        ),
      ),
    );
  }
}

// 2. Use RepaintBoundary for complex animations
Widget build(BuildContext context) {
  return Stack(
    children: [
      // Static background - won't repaint
      RepaintBoundary(
        child: _buildComplexBackground(),
      ),
      // Animated overlay - repaints independently
      AnimatedOverlay(),
    ],
  );
}

// 3. Use ListView.builder for long lists
ListView.builder(
  itemCount: items.length,
  cacheExtent: 500, // Pre-render items
  itemBuilder: (context, index) => ItemTile(item: items[index]),
)

// 4. Use const callbacks with tear-offs
IconButton(
  icon: const Icon(Icons.add),
  onPressed: controller.increment, // Tear-off, not () => controller.increment()
)
''',
        "image_optimization": '''
/// CORRECT: Optimized image loading
// 1. Use cached_network_image
CachedNetworkImage(
  imageUrl: url,
  memCacheWidth: 300, // Resize in memory
  maxWidthDiskCache: 600, // Resize on disk
  placeholder: (_, __) => const ShimmerPlaceholder(),
  errorWidget: (_, __, ___) => const Icon(Icons.error),
  fadeInDuration: const Duration(milliseconds: 200),
)

// 2. Precache critical images
Future<void> precacheImages(BuildContext context) async {
  await Future.wait([
    precacheImage(const AssetImage('assets/logo.png'), context),
    precacheImage(const AssetImage('assets/hero.webp'), context),
  ]);
}

// 3. Use appropriate image formats
// - WebP for photos (smaller, supports transparency)
// - SVG for icons (scalable, tiny file size)
// - Lottie for animations (vector-based)

// 4. Lazy load below-fold images
Visibility(
  visible: isVisible,
  maintainState: false, // Don't keep state when not visible
  child: CachedNetworkImage(imageUrl: url),
)
''',
    }

    # =========================================================================
    # CODING STANDARDS
    # =========================================================================

    CODING_STANDARDS = {
        "naming_conventions": {
            "files": "snake_case.dart (e.g., user_profile_screen.dart)",
            "classes": "PascalCase (e.g., UserProfileScreen)",
            "variables": "camelCase (e.g., userName, isLoading)",
            "constants": "lowerCamelCase or SCREAMING_SNAKE_CASE",
            "private": "_prefixWithUnderscore (e.g., _privateMethod)",
            "boolean": "is/has/can prefix (e.g., isLoading, hasError, canSubmit)",
        },
        "file_organization": '''
/// CORRECT: File organization
// 1. Imports - sorted and grouped
import 'dart:async';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:my_app/core/constants.dart';
import 'package:my_app/features/auth/auth.dart';

import 'widgets/custom_button.dart';

// 2. Part directives (if using)
part 'user_state.dart';
part 'user_notifier.dart';

// 3. Top-level constants
const kAnimationDuration = Duration(milliseconds: 300);

// 4. Class definition
class UserScreen extends ConsumerWidget {
  // Static members first
  static const routeName = '/user';

  // Instance fields
  final String userId;

  // Constructor
  const UserScreen({super.key, required this.userId});

  // Build method
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // ...
  }

  // Other methods (alphabetically or by importance)
  void _handleTap() {}
}
''',
        "documentation": '''
/// CORRECT: Documentation standards
/// A widget that displays user profile information.
///
/// This widget fetches user data and displays it in a card format.
/// It handles loading, error, and success states.
///
/// Example:
/// ```dart
/// UserProfileCard(
///   userId: 'user-123',
///   onTap: () => print('Tapped'),
/// )
/// ```
///
/// See also:
/// * [UserAvatar], which displays just the user's avatar.
/// * [UserListTile], for displaying users in a list.
class UserProfileCard extends StatelessWidget {
  /// The unique identifier of the user to display.
  final String userId;

  /// Called when the card is tapped.
  ///
  /// If null, the card is not tappable.
  final VoidCallback? onTap;

  /// Creates a user profile card.
  const UserProfileCard({
    super.key,
    required this.userId,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    // Implementation
  }
}
''',
        "error_handling": '''
/// CORRECT: Error handling patterns
// 1. Define specific exceptions
sealed class AppException implements Exception {
  final String message;
  final String? code;
  final StackTrace? stackTrace;

  const AppException(this.message, [this.code, this.stackTrace]);

  @override
  String toString() => 'AppException: $message (code: $code)';
}

class NetworkException extends AppException {
  const NetworkException([super.message = 'Network error occurred']);
}

class AuthException extends AppException {
  const AuthException([super.message = 'Authentication failed']);
}

class ValidationException extends AppException {
  final Map<String, String> fieldErrors;
  const ValidationException(this.fieldErrors, [super.message = 'Validation failed']);
}

// 2. Use Result type pattern
sealed class Result<T> {
  const Result();

  factory Result.success(T data) = Success<T>;
  factory Result.failure(AppException error) = Failure<T>;

  R when<R>({
    required R Function(T data) success,
    required R Function(AppException error) failure,
  });
}

class Success<T> extends Result<T> {
  final T data;
  const Success(this.data);

  @override
  R when<R>({
    required R Function(T data) success,
    required R Function(AppException error) failure,
  }) => success(data);
}

class Failure<T> extends Result<T> {
  final AppException error;
  const Failure(this.error);

  @override
  R when<R>({
    required R Function(T data) success,
    required R Function(AppException error) failure,
  }) => failure(error);
}
''',
        "testing": '''
/// CORRECT: Testing standards
// 1. Unit test
void main() {
  group('UserRepository', () {
    late MockApiClient mockApiClient;
    late UserRepository repository;

    setUp(() {
      mockApiClient = MockApiClient();
      repository = UserRepositoryImpl(mockApiClient);
    });

    test('getUser returns user when API call succeeds', () async {
      // Arrange
      const userId = 'user-123';
      final expectedUser = User(id: userId, name: 'Test User');
      when(() => mockApiClient.get('/users/$userId'))
          .thenAnswer((_) async => expectedUser.toJson());

      // Act
      final result = await repository.getUser(userId);

      // Assert
      expect(result, equals(expectedUser));
      verify(() => mockApiClient.get('/users/$userId')).called(1);
    });

    test('getUser throws NetworkException when API fails', () async {
      // Arrange
      when(() => mockApiClient.get(any()))
          .thenThrow(DioException.connectionError(
            requestOptions: RequestOptions(),
            reason: 'Connection failed',
          ));

      // Act & Assert
      expect(
        () => repository.getUser('user-123'),
        throwsA(isA<NetworkException>()),
      );
    });
  });
}

// 2. Widget test
testWidgets('LoginForm shows error on invalid email', (tester) async {
  await tester.pumpWidget(
    const ProviderScope(
      child: MaterialApp(home: LoginForm()),
    ),
  );

  // Enter invalid email
  await tester.enterText(find.byType(TextFormField).first, 'invalid');
  await tester.tap(find.byType(FilledButton));
  await tester.pumpAndSettle();

  // Verify error is shown
  expect(find.text('Enter a valid email address'), findsOneWidget);
});
''',
    }

    # =========================================================================
    # DEPRECATED PATTERNS (AVOID)
    # =========================================================================

    DEPRECATED = {
        "packages": [
            {"name": "provider", "reason": "Use Riverpod 2.x instead", "alternative": "flutter_riverpod: ^2.5.0"},
            {"name": "flutter_bloc", "reason": "Riverpod is preferred for new projects", "alternative": "flutter_riverpod: ^2.5.0"},
            {"name": "get", "reason": "Use Riverpod + GoRouter", "alternative": "go_router: ^14.0.0"},
            {"name": "http", "reason": "Use Dio for better features", "alternative": "dio: ^5.4.0"},
            {"name": "shared_preferences_typed", "reason": "Deprecated", "alternative": "shared_preferences: ^2.2.0"},
        ],
        "patterns": [
            {"pattern": "setState() in complex state", "reason": "Use Riverpod for complex state"},
            {"pattern": "Navigator 1.0", "reason": "Use GoRouter for declarative navigation"},
            {"pattern": "FutureBuilder/StreamBuilder", "reason": "Use Riverpod AsyncValue"},
            {"pattern": "InheritedWidget directly", "reason": "Use Riverpod providers"},
        ],
    }

    def get_all(self) -> dict:
        """Get all Flutter knowledge."""
        return {
            "version": self.VERSION,
            "widget_patterns": self.WIDGET_PATTERNS,
            "state_management": self.STATE_MANAGEMENT,
            "navigation": self.NAVIGATION,
            "forms": self.FORMS,
            "api_patterns": self.API_PATTERNS,
            "platform_integrations": self.PLATFORM_INTEGRATIONS,
            "performance": self.PERFORMANCE,
            "coding_standards": self.CODING_STANDARDS,
            "deprecated": self.DEPRECATED,
        }

    def get_coding_standards(self) -> dict:
        """Get coding standards only."""
        return self.CODING_STANDARDS

    def get_widget_patterns(self) -> dict:
        """Get widget patterns."""
        return self.WIDGET_PATTERNS

    def get_state_management(self) -> dict:
        """Get state management patterns."""
        return self.STATE_MANAGEMENT

    def get_deprecated_list(self) -> list:
        """Get list of deprecated packages."""
        return self.DEPRECATED["packages"]

    def validate_package(self, package_name: str) -> tuple[bool, str]:
        """Check if a package is deprecated."""
        for pkg in self.DEPRECATED["packages"]:
            if pkg["name"] == package_name:
                return False, f"Deprecated: {pkg['reason']}. Use {pkg['alternative']}"
        return True, "Package is acceptable"
