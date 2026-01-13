"""
AIVibe Firebase Knowledge Module

Complete Firebase SDK patterns for Flutter, Authentication,
Firestore, Storage, Cloud Messaging, and Analytics.
"""


class FirebaseKnowledge:
    """Comprehensive Firebase development knowledge."""

    VERSION = "3.0"
    FLUTTER_PACKAGES = {
        "firebase_core": "^3.0.0",
        "firebase_auth": "^5.0.0",
        "cloud_firestore": "^5.0.0",
        "firebase_storage": "^12.0.0",
        "firebase_messaging": "^15.0.0",
        "firebase_analytics": "^11.0.0",
        "firebase_crashlytics": "^4.0.0",
    }

    INITIALIZATION = {
        "flutter": """
// main.dart
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );

  // Optional: Enable Crashlytics collection
  FlutterError.onError = FirebaseCrashlytics.instance.recordFlutterError;

  runApp(const MyApp());
}""",
        "cli_setup": """
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Initialize FlutterFire
dart pub global activate flutterfire_cli
flutterfire configure

# Deploy rules
firebase deploy --only firestore:rules
firebase deploy --only storage:rules""",
    }

    AUTHENTICATION = {
        "providers": {
            "email_password": """
// Sign up
Future<UserCredential> signUp(String email, String password) async {
  return await FirebaseAuth.instance.createUserWithEmailAndPassword(
    email: email,
    password: password,
  );
}

// Sign in
Future<UserCredential> signIn(String email, String password) async {
  return await FirebaseAuth.instance.signInWithEmailAndPassword(
    email: email,
    password: password,
  );
}

// Sign out
Future<void> signOut() async {
  await FirebaseAuth.instance.signOut();
}""",
            "google": """
import 'package:google_sign_in/google_sign_in.dart';

Future<UserCredential> signInWithGoogle() async {
  final GoogleSignInAccount? googleUser = await GoogleSignIn().signIn();
  if (googleUser == null) throw Exception('Google sign in cancelled');

  final GoogleSignInAuthentication googleAuth = await googleUser.authentication;

  final credential = GoogleAuthProvider.credential(
    accessToken: googleAuth.accessToken,
    idToken: googleAuth.idToken,
  );

  return await FirebaseAuth.instance.signInWithCredential(credential);
}""",
            "apple": """
import 'package:sign_in_with_apple/sign_in_with_apple.dart';

Future<UserCredential> signInWithApple() async {
  final appleCredential = await SignInWithApple.getAppleIDCredential(
    scopes: [
      AppleIDAuthorizationScopes.email,
      AppleIDAuthorizationScopes.fullName,
    ],
  );

  final oauthCredential = OAuthProvider('apple.com').credential(
    idToken: appleCredential.identityToken,
    accessToken: appleCredential.authorizationCode,
  );

  return await FirebaseAuth.instance.signInWithCredential(oauthCredential);
}""",
            "phone": """
Future<void> verifyPhoneNumber(String phoneNumber) async {
  await FirebaseAuth.instance.verifyPhoneNumber(
    phoneNumber: phoneNumber,
    verificationCompleted: (PhoneAuthCredential credential) async {
      await FirebaseAuth.instance.signInWithCredential(credential);
    },
    verificationFailed: (FirebaseAuthException e) {
      throw Exception('Verification failed: ${e.message}');
    },
    codeSent: (String verificationId, int? resendToken) {
      // Store verificationId for OTP verification
      _verificationId = verificationId;
    },
    codeAutoRetrievalTimeout: (String verificationId) {
      _verificationId = verificationId;
    },
  );
}

Future<UserCredential> verifyOTP(String otp) async {
  final credential = PhoneAuthProvider.credential(
    verificationId: _verificationId,
    smsCode: otp,
  );
  return await FirebaseAuth.instance.signInWithCredential(credential);
}""",
        },
        "auth_state": """
// Stream for auth state changes
class AuthService {
  final FirebaseAuth _auth = FirebaseAuth.instance;

  Stream<User?> get authStateChanges => _auth.authStateChanges();

  User? get currentUser => _auth.currentUser;

  Future<String?> getIdToken({bool forceRefresh = false}) async {
    return await _auth.currentUser?.getIdToken(forceRefresh);
  }
}

// In Riverpod
final authStateProvider = StreamProvider<User?>((ref) {
  return FirebaseAuth.instance.authStateChanges();
});

// Guard routes based on auth
final userProvider = Provider<User?>((ref) {
  return ref.watch(authStateProvider).valueOrNull;
});""",
        "custom_claims": """
// Set custom claims (backend/cloud function)
await admin.auth().setCustomUserClaims(uid, {
  tenantId: 'tenant-123',
  role: 'admin',
});

// Read claims in Flutter
Future<Map<String, dynamic>> getClaims() async {
  final user = FirebaseAuth.instance.currentUser;
  if (user == null) return {};

  final idTokenResult = await user.getIdTokenResult(true);
  return idTokenResult.claims ?? {};
}""",
    }

    FIRESTORE = {
        "operations": {
            "create": """
final docRef = await FirebaseFirestore.instance
    .collection('users')
    .add({
      'name': 'John',
      'email': 'john@example.com',
      'createdAt': FieldValue.serverTimestamp(),
    });

// With specific ID
await FirebaseFirestore.instance
    .collection('users')
    .doc(userId)
    .set({
      'name': 'John',
      'email': 'john@example.com',
    });""",
            "read": """
// Single document
final doc = await FirebaseFirestore.instance
    .collection('users')
    .doc(userId)
    .get();

if (doc.exists) {
  final data = doc.data()!;
  return User.fromMap(data);
}

// Query documents
final snapshot = await FirebaseFirestore.instance
    .collection('users')
    .where('status', isEqualTo: 'active')
    .orderBy('createdAt', descending: true)
    .limit(20)
    .get();

final users = snapshot.docs.map((doc) => User.fromMap(doc.data())).toList();""",
            "update": """
await FirebaseFirestore.instance
    .collection('users')
    .doc(userId)
    .update({
      'name': 'Jane',
      'updatedAt': FieldValue.serverTimestamp(),
    });

// Increment field
await docRef.update({
  'credits': FieldValue.increment(10),
});

// Array operations
await docRef.update({
  'tags': FieldValue.arrayUnion(['new-tag']),
});
await docRef.update({
  'tags': FieldValue.arrayRemove(['old-tag']),
});""",
            "delete": """
await FirebaseFirestore.instance
    .collection('users')
    .doc(userId)
    .delete();

// Delete field
await docRef.update({
  'obsoleteField': FieldValue.delete(),
});""",
            "batch": """
final batch = FirebaseFirestore.instance.batch();

final userRef = FirebaseFirestore.instance.collection('users').doc(userId);
final statsRef = FirebaseFirestore.instance.collection('stats').doc('global');

batch.update(userRef, {'name': 'Updated'});
batch.update(statsRef, {'userCount': FieldValue.increment(1)});

await batch.commit();""",
            "transaction": """
await FirebaseFirestore.instance.runTransaction((transaction) async {
  final fromDoc = await transaction.get(fromRef);
  final toDoc = await transaction.get(toRef);

  final fromCredits = fromDoc.data()!['credits'] as int;
  if (fromCredits < amount) {
    throw Exception('Insufficient credits');
  }

  transaction.update(fromRef, {'credits': FieldValue.increment(-amount)});
  transaction.update(toRef, {'credits': FieldValue.increment(amount)});
});""",
        },
        "realtime": """
// Stream single document
Stream<User?> watchUser(String userId) {
  return FirebaseFirestore.instance
      .collection('users')
      .doc(userId)
      .snapshots()
      .map((doc) => doc.exists ? User.fromMap(doc.data()!) : null);
}

// Stream query
Stream<List<Message>> watchMessages(String chatId) {
  return FirebaseFirestore.instance
      .collection('chats')
      .doc(chatId)
      .collection('messages')
      .orderBy('createdAt', descending: true)
      .limit(50)
      .snapshots()
      .map((snapshot) =>
          snapshot.docs.map((doc) => Message.fromMap(doc.data())).toList());
}""",
        "pagination": """
class PaginatedQuery<T> {
  final Query<Map<String, dynamic>> query;
  final T Function(Map<String, dynamic>) fromMap;
  DocumentSnapshot? _lastDoc;
  bool _hasMore = true;

  PaginatedQuery(this.query, this.fromMap);

  bool get hasMore => _hasMore;

  Future<List<T>> fetchNext(int limit) async {
    Query<Map<String, dynamic>> q = query.limit(limit);

    if (_lastDoc != null) {
      q = q.startAfterDocument(_lastDoc!);
    }

    final snapshot = await q.get();
    _hasMore = snapshot.docs.length == limit;

    if (snapshot.docs.isNotEmpty) {
      _lastDoc = snapshot.docs.last;
    }

    return snapshot.docs.map((doc) => fromMap(doc.data())).toList();
  }

  void reset() {
    _lastDoc = null;
    _hasMore = true;
  }
}""",
        "security_rules": """
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // User profiles - only owner can read/write
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }

    // Projects - tenant isolation
    match /projects/{projectId} {
      allow read, write: if request.auth != null &&
        request.auth.token.tenantId == resource.data.tenantId;

      // Subcollections inherit parent access
      match /tasks/{taskId} {
        allow read, write: if request.auth != null &&
          request.auth.token.tenantId == get(/databases/$(database)/documents/projects/$(projectId)).data.tenantId;
      }
    }

    // Public read, authenticated write
    match /public/{docId} {
      allow read: if true;
      allow write: if request.auth != null;
    }
  }
}""",
    }

    STORAGE = {
        "upload": """
import 'package:firebase_storage/firebase_storage.dart';

Future<String> uploadFile(File file, String path) async {
  final ref = FirebaseStorage.instance.ref().child(path);

  final uploadTask = ref.putFile(
    file,
    SettableMetadata(
      contentType: 'image/jpeg',
      customMetadata: {'uploadedBy': userId},
    ),
  );

  // Listen to progress
  uploadTask.snapshotEvents.listen((event) {
    final progress = event.bytesTransferred / event.totalBytes;
    print('Upload progress: ${(progress * 100).toStringAsFixed(0)}%');
  });

  await uploadTask;
  return await ref.getDownloadURL();
}

// Upload from bytes
Future<String> uploadBytes(Uint8List data, String path) async {
  final ref = FirebaseStorage.instance.ref().child(path);
  await ref.putData(data);
  return await ref.getDownloadURL();
}""",
        "download": """
// Get download URL
Future<String> getDownloadUrl(String path) async {
  return await FirebaseStorage.instance.ref().child(path).getDownloadURL();
}

// Download to file
Future<void> downloadFile(String path, File destination) async {
  await FirebaseStorage.instance.ref().child(path).writeToFile(destination);
}

// Download as bytes
Future<Uint8List?> downloadBytes(String path) async {
  return await FirebaseStorage.instance.ref().child(path).getData();
}""",
        "delete": """
Future<void> deleteFile(String path) async {
  await FirebaseStorage.instance.ref().child(path).delete();
}""",
        "storage_rules": """
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // User uploads - only owner can read/write
    match /users/{userId}/{allPaths=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }

    // Project files - tenant access
    match /projects/{projectId}/{allPaths=**} {
      allow read, write: if request.auth != null &&
        request.auth.token.tenantId == projectId;
    }

    // Public assets
    match /public/{allPaths=**} {
      allow read: if true;
      allow write: if request.auth != null;
    }

    // Image upload validation
    match /images/{imageId} {
      allow read: if true;
      allow write: if request.auth != null
        && request.resource.size < 5 * 1024 * 1024  // 5MB
        && request.resource.contentType.matches('image/.*');
    }
  }
}""",
    }

    MESSAGING = {
        "setup": """
import 'package:firebase_messaging/firebase_messaging.dart';

class PushNotificationService {
  final FirebaseMessaging _messaging = FirebaseMessaging.instance;

  Future<void> initialize() async {
    // Request permission
    final settings = await _messaging.requestPermission(
      alert: true,
      badge: true,
      sound: true,
    );

    if (settings.authorizationStatus == AuthorizationStatus.authorized) {
      // Get FCM token
      final token = await _messaging.getToken();
      await _saveTokenToBackend(token);

      // Listen for token refresh
      _messaging.onTokenRefresh.listen(_saveTokenToBackend);

      // Handle foreground messages
      FirebaseMessaging.onMessage.listen(_handleForegroundMessage);

      // Handle background/terminated messages
      FirebaseMessaging.onBackgroundMessage(_backgroundHandler);

      // Handle notification tap
      FirebaseMessaging.onMessageOpenedApp.listen(_handleNotificationTap);
    }
  }

  void _handleForegroundMessage(RemoteMessage message) {
    // Show local notification
    showLocalNotification(
      title: message.notification?.title ?? '',
      body: message.notification?.body ?? '',
      data: message.data,
    );
  }

  void _handleNotificationTap(RemoteMessage message) {
    // Navigate based on data
    final route = message.data['route'];
    if (route != null) {
      navigatorKey.currentState?.pushNamed(route);
    }
  }
}

// Must be top-level function
@pragma('vm:entry-point')
Future<void> _backgroundHandler(RemoteMessage message) async {
  await Firebase.initializeApp();
  // Handle background message
}""",
        "topics": """
// Subscribe to topic
await FirebaseMessaging.instance.subscribeToTopic('announcements');

// Unsubscribe
await FirebaseMessaging.instance.unsubscribeFromTopic('announcements');""",
    }

    ANALYTICS = """
import 'package:firebase_analytics/firebase_analytics.dart';

class AnalyticsService {
  final FirebaseAnalytics _analytics = FirebaseAnalytics.instance;

  // Log custom event
  Future<void> logEvent(String name, Map<String, dynamic> params) async {
    await _analytics.logEvent(name: name, parameters: params);
  }

  // Set user properties
  Future<void> setUserId(String userId) async {
    await _analytics.setUserId(id: userId);
  }

  Future<void> setUserProperty(String name, String value) async {
    await _analytics.setUserProperty(name: name, value: value);
  }

  // Screen tracking
  Future<void> logScreenView(String screenName) async {
    await _analytics.logScreenView(screenName: screenName);
  }

  // Ecommerce events
  Future<void> logPurchase(String itemId, double amount) async {
    await _analytics.logPurchase(
      currency: 'USD',
      value: amount,
      items: [AnalyticsEventItem(itemId: itemId, price: amount)],
    );
  }
}

// Navigator observer for automatic screen tracking
final observer = FirebaseAnalyticsObserver(analytics: FirebaseAnalytics.instance);

MaterialApp(
  navigatorObservers: [observer],
);""",

    def get_all(self) -> dict:
        """Get complete Firebase knowledge."""
        return {
            "version": self.VERSION,
            "flutter_packages": self.FLUTTER_PACKAGES,
            "initialization": self.INITIALIZATION,
            "authentication": self.AUTHENTICATION,
            "firestore": self.FIRESTORE,
            "storage": self.STORAGE,
            "messaging": self.MESSAGING,
            "analytics": self.ANALYTICS,
        }

    def get_auth_patterns(self) -> dict:
        """Get authentication patterns."""
        return self.AUTHENTICATION

    def get_firestore_patterns(self) -> dict:
        """Get Firestore patterns."""
        return self.FIRESTORE

    def get_storage_patterns(self) -> dict:
        """Get Storage patterns."""
        return self.STORAGE
