"""
Dart Knowledge Module

Complete Dart 3.5+ knowledge including:
- Language features and patterns
- Null safety
- Records and patterns
- Async programming
- Collections and extensions
"""


class DartKnowledge:
    """Complete Dart expertise for AI agent training."""

    VERSION = "3.5.0"

    # =========================================================================
    # MODERN DART FEATURES (3.x)
    # =========================================================================

    LANGUAGE_FEATURES = {
        "records": '''
/// Records - Lightweight data structures
// Named record type
typedef UserRecord = ({String name, int age, String email});

UserRecord createUser() {
  return (name: 'John', age: 30, email: 'john@example.com');
}

// Positional record
(int, String, bool) getStatus() {
  return (200, 'OK', true);
}

// Destructuring
void main() {
  final user = createUser();
  print(user.name); // Access by name

  final (code, message, success) = getStatus();
  print('Status: $code - $message');

  // Pattern matching with records
  switch (getStatus()) {
    case (200, _, true):
      print('Success!');
    case (int code, String msg, false) when code >= 400:
      print('Error $code: $msg');
    default:
      print('Unknown status');
  }
}
''',
        "patterns": '''
/// Pattern Matching
// Switch expressions
String describeNumber(int n) => switch (n) {
  0 => 'zero',
  1 => 'one',
  2 => 'two',
  < 0 => 'negative',
  >= 100 => 'large',
  _ => 'other',
};

// Object destructuring
class Point {
  final int x, y;
  Point(this.x, this.y);
}

String describePoint(Point p) => switch (p) {
  Point(x: 0, y: 0) => 'origin',
  Point(x: var a, y: 0) => 'on x-axis at $a',
  Point(x: 0, y: var b) => 'on y-axis at $b',
  Point(x: var a, y: var b) when a == b => 'diagonal at $a',
  Point(x: var a, y: var b) => 'point ($a, $b)',
};

// List patterns
void processCommand(List<String> args) {
  switch (args) {
    case ['help']:
      showHelp();
    case ['add', var item]:
      addItem(item);
    case ['remove', var item, ...var rest]:
      removeItem(item);
      processCommand(rest);
    case []:
      print('No command');
    default:
      print('Unknown command');
  }
}

// If-case
void example(Object? value) {
  if (value case int n when n > 0) {
    print('Positive integer: $n');
  }

  if (value case {'name': String name, 'age': int age}) {
    print('User: $name, $age years old');
  }
}
''',
        "sealed_classes": '''
/// Sealed Classes - Exhaustive pattern matching
sealed class Result<T> {
  const Result();
}

class Success<T> extends Result<T> {
  final T value;
  const Success(this.value);
}

class Failure<T> extends Result<T> {
  final Exception error;
  const Failure(this.error);
}

class Loading<T> extends Result<T> {
  const Loading();
}

// Exhaustive switch (compiler enforces all cases)
String handleResult<T>(Result<T> result) => switch (result) {
  Success(value: var v) => 'Success: $v',
  Failure(error: var e) => 'Error: $e',
  Loading() => 'Loading...',
  // No default needed - all cases covered
};

/// Sealed for state machines
sealed class AuthState {}

class AuthInitial extends AuthState {}

class AuthLoading extends AuthState {}

class AuthAuthenticated extends AuthState {
  final User user;
  AuthAuthenticated(this.user);
}

class AuthUnauthenticated extends AuthState {}

class AuthError extends AuthState {
  final String message;
  AuthError(this.message);
}
''',
        "class_modifiers": '''
/// Class Modifiers (Dart 3.0+)

// base - Can be extended but not implemented
base class Animal {
  void breathe() => print('breathing');
}

class Dog extends Animal {} // OK
// class Cat implements Animal {} // ERROR

// interface - Can be implemented but not extended
interface class Flyable {
  void fly();
}

// class Bird extends Flyable {} // ERROR
class Airplane implements Flyable {
  @override
  void fly() => print('flying');
}

// final - Cannot be extended or implemented outside library
final class SecureToken {
  final String value;
  SecureToken(this.value);
}

// sealed - Exhaustive in library, closed outside
sealed class Shape {}
class Circle extends Shape {}
class Square extends Shape {}

// mixin - Behavior only, no constructors
mixin Loggable {
  void log(String message) => print('[LOG] $message');
}

class Service with Loggable {
  void doWork() {
    log('Starting work');
  }
}
''',
    }

    # =========================================================================
    # NULL SAFETY
    # =========================================================================

    NULL_SAFETY = {
        "basics": '''
/// Null Safety Fundamentals

// Non-nullable by default
String name = 'John'; // Cannot be null
// name = null; // Compile error

// Nullable types
String? nullableName; // Can be null
nullableName = null; // OK

// Null-aware operators
String display = nullableName ?? 'Unknown'; // Default if null
int? length = nullableName?.length; // Null if nullableName is null
nullableName ??= 'Default'; // Assign if null

// Assertion operator (use sparingly!)
String definitelyNotNull = nullableName!; // Throws if null

// Late initialization
late String lateInit;
void init() {
  lateInit = 'Initialized';
}

// Late final with lazy initialization
late final String lazyValue = computeExpensiveValue();
''',
        "best_practices": '''
/// Null Safety Best Practices

// 1. PREFER non-nullable types
class User {
  final String id; // Not String?
  final String name;
  final String? bio; // Only nullable when truly optional

  User({required this.id, required this.name, this.bio});
}

// 2. Use required for non-optional named parameters
void createUser({
  required String name,
  required String email,
  String? phone, // Optional
}) {}

// 3. Avoid ! operator - use null-aware alternatives
// BAD
// String getName(User? user) => user!.name;

// GOOD
String getName(User? user) => user?.name ?? 'Unknown';

// 4. Use late only when necessary
class WidgetState {
  // GOOD: Late for framework-initialized fields
  late final TextEditingController controller;

  void initState() {
    controller = TextEditingController();
  }
}

// 5. Leverage flow analysis
void process(String? value) {
  if (value == null) return;
  // Dart knows value is non-null here
  print(value.length); // No error
}

// 6. Use collection if/for for conditional elements
List<Widget> buildWidgets(User? user) => [
  const Header(),
  if (user != null) UserInfo(user: user),
  if (user?.bio case String bio) BioSection(bio: bio),
];
''',
    }

    # =========================================================================
    # ASYNC PROGRAMMING
    # =========================================================================

    ASYNC = {
        "futures": '''
/// Future Patterns

// Basic async/await
Future<User> fetchUser(String id) async {
  final response = await http.get(Uri.parse('/users/$id'));
  if (response.statusCode != 200) {
    throw HttpException('Failed to fetch user');
  }
  return User.fromJson(jsonDecode(response.body));
}

// Parallel execution
Future<(User, List<Post>)> fetchUserWithPosts(String userId) async {
  final results = await (
    fetchUser(userId),
    fetchUserPosts(userId),
  ).wait;
  return results;
}

// Sequential with error handling
Future<void> processSequentially() async {
  try {
    final user = await fetchUser('123');
    final posts = await fetchUserPosts(user.id);
    await saveToCache(user, posts);
  } on HttpException catch (e) {
    print('Network error: $e');
  } on FormatException catch (e) {
    print('Parse error: $e');
  }
}

// Timeout
Future<User> fetchWithTimeout(String id) async {
  return fetchUser(id).timeout(
    const Duration(seconds: 10),
    onTimeout: () => throw TimeoutException('Request timed out'),
  );
}

// Retry pattern
Future<T> retry<T>(
  Future<T> Function() operation, {
  int maxAttempts = 3,
  Duration delay = const Duration(seconds: 1),
}) async {
  for (var attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await operation();
    } catch (e) {
      if (attempt == maxAttempts) rethrow;
      await Future.delayed(delay * attempt);
    }
  }
  throw StateError('Should not reach here');
}
''',
        "streams": '''
/// Stream Patterns

// Creating streams
Stream<int> countDown(int from) async* {
  for (var i = from; i >= 0; i--) {
    await Future.delayed(const Duration(seconds: 1));
    yield i;
  }
}

// Stream transformation
Stream<String> formatNumbers(Stream<int> numbers) {
  return numbers
      .where((n) => n > 0)
      .map((n) => 'Number: $n')
      .handleError((e) => print('Error: $e'));
}

// Stream controller for events
class EventBus {
  final _controller = StreamController<AppEvent>.broadcast();

  Stream<AppEvent> get stream => _controller.stream;

  void emit(AppEvent event) {
    if (!_controller.isClosed) {
      _controller.add(event);
    }
  }

  Stream<T> on<T extends AppEvent>() {
    return stream.whereType<T>();
  }

  void dispose() {
    _controller.close();
  }
}

// Listen with subscription management
class MyWidget extends StatefulWidget {
  @override
  State<MyWidget> createState() => _MyWidgetState();
}

class _MyWidgetState extends State<MyWidget> {
  late final StreamSubscription<User> _subscription;

  @override
  void initState() {
    super.initState();
    _subscription = userStream.listen(
      (user) => setState(() => _user = user),
      onError: (e) => showError(e),
      cancelOnError: false,
    );
  }

  @override
  void dispose() {
    _subscription.cancel();
    super.dispose();
  }
}
''',
        "isolates": '''
/// Isolate Patterns (Dart 3.x)

// compute() for simple operations
Future<List<User>> parseUsers(String json) async {
  return compute(_parseUsersSync, json);
}

List<User> _parseUsersSync(String json) {
  final list = jsonDecode(json) as List;
  return list.map((e) => User.fromJson(e)).toList();
}

// Isolate.run for one-off tasks
Future<Image> processImage(Uint8List bytes) async {
  return Isolate.run(() {
    // Heavy image processing
    return decodeAndProcess(bytes);
  });
}

// Long-running isolate with communication
class BackgroundProcessor {
  Isolate? _isolate;
  SendPort? _sendPort;
  final _receivePort = ReceivePort();

  Future<void> start() async {
    _isolate = await Isolate.spawn(
      _isolateEntry,
      _receivePort.sendPort,
    );
    _sendPort = await _receivePort.first as SendPort;
  }

  static void _isolateEntry(SendPort mainSendPort) {
    final receivePort = ReceivePort();
    mainSendPort.send(receivePort.sendPort);

    receivePort.listen((message) {
      // Process message
      final result = processMessage(message);
      mainSendPort.send(result);
    });
  }

  void send(dynamic message) {
    _sendPort?.send(message);
  }

  void dispose() {
    _receivePort.close();
    _isolate?.kill();
  }
}
''',
    }

    # =========================================================================
    # COLLECTIONS
    # =========================================================================

    COLLECTIONS = {
        "list_operations": '''
/// List Operations

final numbers = [1, 2, 3, 4, 5];

// Transform
final doubled = numbers.map((n) => n * 2).toList();

// Filter
final evens = numbers.where((n) => n.isEven).toList();

// Find
final firstEven = numbers.firstWhere((n) => n.isEven, orElse: () => -1);
final maybeEven = numbers.cast<int?>().firstWhere((n) => n!.isEven, orElse: () => null);

// Reduce
final sum = numbers.reduce((a, b) => a + b);
final product = numbers.fold(1, (acc, n) => acc * n);

// Any/Every
final hasEven = numbers.any((n) => n.isEven);
final allPositive = numbers.every((n) => n > 0);

// Sort (in-place)
final sorted = [...numbers]..sort((a, b) => b.compareTo(a)); // Descending

// Group by
final users = [User('Alice', 25), User('Bob', 30), User('Charlie', 25)];
final byAge = users.groupListsBy((u) => u.age);
// {25: [Alice, Charlie], 30: [Bob]}
''',
        "map_operations": '''
/// Map Operations

final scores = {'Alice': 95, 'Bob': 87, 'Charlie': 92};

// Transform values
final curved = scores.map((k, v) => MapEntry(k, (v * 1.1).round()));

// Filter entries
final passed = Map.fromEntries(
  scores.entries.where((e) => e.value >= 90),
);

// Get with default
final score = scores['Unknown'] ?? 0;

// Update
scores.update('Alice', (v) => v + 5, ifAbsent: () => 100);

// Merge maps
final merged = {...scores, 'David': 88, 'Alice': 100}; // Alice overwritten

// Null-safe access
final maybeScores = {'Alice': 95} as Map<String, int>?;
final aliceScore = maybeScores?['Alice'] ?? 0;
''',
        "spread_collection": '''
/// Spread and Collection If/For

// Spread operator
final list1 = [1, 2, 3];
final list2 = [0, ...list1, 4, 5];

// Null-aware spread
final nullable = null as List<int>?;
final safe = [1, ...?nullable, 2]; // [1, 2]

// Collection if
final isAdmin = true;
final menu = [
  'Home',
  'Profile',
  if (isAdmin) 'Admin Panel',
];

// Collection for
final squares = [
  for (var i = 1; i <= 5; i++) i * i,
]; // [1, 4, 9, 16, 25]

// Combining patterns
Widget build(BuildContext context) {
  return Column(
    children: [
      const Header(),
      for (final item in items)
        if (item.isVisible)
          ItemCard(item: item),
      if (isLoading)
        const CircularProgressIndicator()
      else if (items.isEmpty)
        const EmptyState(),
    ],
  );
}
''',
    }

    # =========================================================================
    # EXTENSIONS
    # =========================================================================

    EXTENSIONS = '''
/// Extension Methods

// String extensions
extension StringExtension on String {
  String capitalize() =>
      isEmpty ? this : '${this[0].toUpperCase()}${substring(1)}';

  String truncate(int maxLength, {String suffix = '...'}) {
    if (length <= maxLength) return this;
    return '${substring(0, maxLength - suffix.length)}$suffix';
  }

  bool get isEmail =>
      RegExp(r'^[\\w-.]+@([\\w-]+\\.)+[\\w-]{2,}$').hasMatch(this);

  bool get isNumeric => double.tryParse(this) != null;
}

// DateTime extensions
extension DateTimeExtension on DateTime {
  bool get isToday {
    final now = DateTime.now();
    return year == now.year && month == now.month && day == now.day;
  }

  bool get isFuture => isAfter(DateTime.now());

  String get timeAgo {
    final diff = DateTime.now().difference(this);
    if (diff.inDays > 0) return '${diff.inDays}d ago';
    if (diff.inHours > 0) return '${diff.inHours}h ago';
    if (diff.inMinutes > 0) return '${diff.inMinutes}m ago';
    return 'Just now';
  }

  DateTime get startOfDay => DateTime(year, month, day);
  DateTime get endOfDay => DateTime(year, month, day, 23, 59, 59);
}

// List extensions
extension ListExtension<T> on List<T> {
  T? get firstOrNull => isEmpty ? null : first;
  T? get lastOrNull => isEmpty ? null : last;

  List<T> distinctBy<K>(K Function(T) keyOf) {
    final seen = <K>{};
    return where((e) => seen.add(keyOf(e))).toList();
  }

  Map<K, List<T>> groupBy<K>(K Function(T) keyOf) {
    return fold(<K, List<T>>{}, (map, element) {
      (map[keyOf(element)] ??= []).add(element);
      return map;
    });
  }
}

// Nullable extensions
extension NullableExtension<T> on T? {
  R? let<R>(R Function(T) transform) {
    final self = this;
    return self != null ? transform(self) : null;
  }

  T orElse(T defaultValue) => this ?? defaultValue;
}

// Context extensions (Flutter)
extension BuildContextExtension on BuildContext {
  ThemeData get theme => Theme.of(this);
  TextTheme get textTheme => theme.textTheme;
  ColorScheme get colorScheme => theme.colorScheme;
  MediaQueryData get mediaQuery => MediaQuery.of(this);
  Size get screenSize => mediaQuery.size;
  bool get isDarkMode => theme.brightness == Brightness.dark;

  void showSnackBar(String message) {
    ScaffoldMessenger.of(this).showSnackBar(
      SnackBar(content: Text(message)),
    );
  }
}
'''

    # =========================================================================
    # CODING STANDARDS
    # =========================================================================

    CODING_STANDARDS = {
        "naming_conventions": {
            "classes": "UpperCamelCase (PascalCase): UserProfile, HttpClient",
            "extensions": "UpperCamelCase: StringExtension, ListExtension",
            "libraries_packages": "lowercase_with_underscores: my_package",
            "files": "lowercase_with_underscores: user_profile.dart",
            "variables": "lowerCamelCase: userName, itemCount",
            "constants": "lowerCamelCase: defaultTimeout (prefer over SCREAMING_CAPS)",
            "parameters": "lowerCamelCase: required String userName",
            "type_parameters": "Single uppercase: T, E, K, V or descriptive: TResult",
        },
        "style_rules": [
            "Use 2 spaces for indentation",
            "Max line length: 80 characters (recommended), 120 (max)",
            "Use trailing commas for multi-line constructs",
            "Order members: static fields, instance fields, constructors, methods",
            "Prefer const constructors for immutable widgets",
            "Use final for variables that don't change",
            "Prefer expression bodies for simple getters/methods",
        ],
        "import_rules": '''
/// Import ordering
// 1. dart: imports
import 'dart:async';
import 'dart:io';

// 2. package: imports
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

// 3. Relative imports (same package)
import '../models/user.dart';
import 'widgets/custom_button.dart';

/// Import best practices
// Use show/hide for selective imports
import 'package:flutter/material.dart' show Widget, BuildContext;

// Use as for conflicting names
import 'package:http/http.dart' as http;
import 'dart:io' as io;

// Avoid relative imports across packages
// BAD: import '../../other_package/file.dart';
// GOOD: import 'package:other_package/file.dart';
''',
        "documentation_rules": '''
/// Documentation Rules

// Use /// for public APIs
/// Fetches a user by their unique identifier.
///
/// Returns null if the user is not found.
///
/// Throws [NetworkException] if the request fails.
Future<User?> fetchUser(String id) async { }

// Use // for implementation comments
void processData() {
  // Transform the data first
  final transformed = transform(data);

  // Then validate
  validate(transformed);
}

// Document parameters and return values
/// Creates a new user account.
///
/// [email] must be a valid email address.
/// [password] must be at least 8 characters.
///
/// Returns the created [User] with their assigned ID.
///
/// Example:
/// ```dart
/// final user = await createUser(
///   email: 'test@example.com',
///   password: 'securePass123',
/// );
/// print(user.id);
/// ```
Future<User> createUser({
  required String email,
  required String password,
}) async { }
''',
    }

    # =========================================================================
    # DART FIX / ANALYZER
    # =========================================================================

    DART_FIX = {
        "common_fixes": [
            "prefer_const_constructors: Add const to constructors",
            "prefer_const_literals_to_create_immutables: Use const for lists/maps",
            "prefer_final_fields: Use final for unmodified fields",
            "prefer_final_locals: Use final for unmodified local variables",
            "unnecessary_this: Remove unnecessary this.",
            "use_super_parameters: Use super.key instead of Key? key",
            "avoid_print: Use logger instead of print",
            "prefer_single_quotes: Use single quotes for strings",
        ],
        "analyzer_config": '''
# analysis_options.yaml
include: package:flutter_lints/flutter.yaml

analyzer:
  language:
    strict-casts: true
    strict-inference: true
    strict-raw-types: true
  errors:
    missing_required_param: error
    missing_return: error
    todo: ignore
  exclude:
    - "**/*.g.dart"
    - "**/*.freezed.dart"

linter:
  rules:
    # Error rules
    - avoid_dynamic_calls
    - avoid_returning_null_for_future
    - avoid_slow_async_io
    - cancel_subscriptions
    - close_sinks
    - literal_only_boolean_expressions
    - throw_in_finally

    # Style rules
    - always_declare_return_types
    - always_put_required_named_parameters_first
    - avoid_annotating_with_dynamic
    - avoid_bool_literals_in_conditional_expressions
    - avoid_catches_without_on_clauses
    - avoid_catching_errors
    - avoid_double_and_int_checks
    - avoid_equals_and_hash_code_on_mutable_classes
    - avoid_escaping_inner_quotes
    - avoid_field_initializers_in_const_classes
    - avoid_final_parameters
    - avoid_implementing_value_types
    - avoid_multiple_declarations_per_line
    - avoid_positional_boolean_parameters
    - avoid_private_typedef_functions
    - avoid_redundant_argument_values
    - avoid_returning_null
    - avoid_returning_this
    - avoid_setters_without_getters
    - avoid_types_on_closure_parameters
    - avoid_unused_constructor_parameters
    - avoid_void_async
    - cascade_invocations
    - cast_nullable_to_non_nullable
    - combinators_ordering
    - conditional_uri_does_not_exist
    - deprecated_consistency
    - directives_ordering
    - eol_at_end_of_file
    - flutter_style_todos
    - join_return_with_assignment
    - leading_newlines_in_multiline_strings
    - lines_longer_than_80_chars
    - missing_whitespace_between_adjacent_strings
    - no_adjacent_strings_in_list
    - no_runtimeType_toString
    - noop_primitive_operations
    - omit_local_variable_types
    - one_member_abstracts
    - only_throw_errors
    - parameter_assignments
    - prefer_asserts_in_initializer_lists
    - prefer_constructors_over_static_methods
    - prefer_final_in_for_each
    - prefer_foreach
    - prefer_if_elements_to_conditional_expressions
    - prefer_int_literals
    - prefer_mixin
    - prefer_null_aware_method_calls
    - prefer_single_quotes
    - require_trailing_commas
    - sort_constructors_first
    - sort_unnamed_constructors_first
    - tighten_type_of_initializing_formals
    - type_annotate_public_apis
    - unawaited_futures
    - unnecessary_await_in_return
    - unnecessary_breaks
    - unnecessary_lambdas
    - unnecessary_null_aware_assignments
    - unnecessary_null_checks
    - unnecessary_parenthesis
    - unnecessary_raw_strings
    - unnecessary_statements
    - unnecessary_to_list_in_spreads
    - unreachable_from_main
    - use_colored_box
    - use_decorated_box
    - use_enums
    - use_if_null_to_convert_nulls_to_bools
    - use_is_even_rather_than_modulo
    - use_late_for_private_fields_and_variables
    - use_named_constants
    - use_raw_strings
    - use_setters_to_change_properties
    - use_string_buffers
    - use_string_in_part_of_directives
    - use_super_parameters
    - use_test_throws_matchers
    - use_to_and_as_if_applicable
''',
    }

    def get_all(self) -> dict:
        """Get all Dart knowledge."""
        return {
            "version": self.VERSION,
            "language_features": self.LANGUAGE_FEATURES,
            "null_safety": self.NULL_SAFETY,
            "async": self.ASYNC,
            "collections": self.COLLECTIONS,
            "extensions": self.EXTENSIONS,
            "coding_standards": self.CODING_STANDARDS,
            "dart_fix": self.DART_FIX,
        }

    def get_coding_standards(self) -> dict:
        """Get coding standards only."""
        return self.CODING_STANDARDS

    def get_analyzer_config(self) -> str:
        """Get recommended analyzer configuration."""
        return self.DART_FIX["analyzer_config"]
