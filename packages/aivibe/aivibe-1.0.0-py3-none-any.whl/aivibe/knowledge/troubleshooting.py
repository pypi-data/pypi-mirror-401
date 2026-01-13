"""
AIVibe Troubleshooting Knowledge Module

Common build errors, deployment issues, and debugging
patterns for Flutter, Dart, and cloud services.
"""


class TroubleshootingKnowledge:
    """Comprehensive troubleshooting knowledge."""

    VERSION = "1.0"

    FLUTTER_BUILD = {
        "gradle_errors": {
            "sdk_version_mismatch": {
                "error": "Minimum supported Gradle version is X.X",
                "solution": """
1. Update gradle/wrapper/gradle-wrapper.properties:
   distributionUrl=https://services.gradle.org/distributions/gradle-8.4-all.zip

2. Update android/build.gradle:
   classpath 'com.android.tools.build:gradle:8.2.0'

3. Clean and rebuild:
   cd android && ./gradlew clean && cd .. && flutter clean && flutter pub get""",
            },
            "kotlin_version": {
                "error": "Cannot find or load main class kotlin",
                "solution": """
1. Update android/build.gradle kotlin version:
   ext.kotlin_version = '1.9.22'

2. Ensure Kotlin plugin is applied:
   classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version"

3. Clean rebuild:
   flutter clean && flutter pub get && flutter build apk""",
            },
            "multidex": {
                "error": "Cannot fit requested classes in a single dex file",
                "solution": """
1. Enable multidex in android/app/build.gradle:
   defaultConfig {
       multiDexEnabled true
   }

2. Add dependency:
   implementation 'androidx.multidex:multidex:2.0.1'""",
            },
            "namespace_required": {
                "error": "Namespace not specified",
                "solution": """
1. Add namespace to android/app/build.gradle:
   android {
       namespace 'com.example.app'
   }

2. This is required for AGP 8.0+""",
            },
        },
        "ios_errors": {
            "pod_install": {
                "error": "CocoaPods could not find compatible versions",
                "solution": """
1. Update CocoaPods:
   sudo gem install cocoapods

2. Clear cache and reinstall:
   cd ios && rm -rf Pods Podfile.lock && pod install --repo-update

3. If still failing, try:
   pod deintegrate && pod setup && pod install""",
            },
            "signing": {
                "error": "Signing for X requires a development team",
                "solution": """
1. Open ios/Runner.xcworkspace in Xcode
2. Select Runner target -> Signing & Capabilities
3. Select your development team
4. Ensure bundle identifier is unique

Or in command line:
flutter build ios --no-codesign (for testing)""",
            },
            "min_ios_version": {
                "error": "The iOS deployment target is set to X.X, but the range of supported deployment target is Y.Y to Z.Z",
                "solution": """
1. Update ios/Podfile:
   platform :ios, '13.0'

2. Update Runner target in Xcode:
   Set minimum deployment target to 13.0

3. Run: cd ios && pod install""",
            },
            "module_not_found": {
                "error": "Module 'X' not found",
                "solution": """
1. Ensure the plugin is in pubspec.yaml
2. Run: flutter pub get
3. Run: cd ios && pod install
4. Clean and rebuild: flutter clean && flutter build ios""",
            },
        },
        "web_errors": {
            "cors": {
                "error": "Access to XMLHttpRequest has been blocked by CORS policy",
                "solution": """
1. For development, use flutter run -d chrome --web-browser-flag "--disable-web-security"

2. For production, configure CORS headers on your API server:
   Access-Control-Allow-Origin: https://your-domain.com
   Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
   Access-Control-Allow-Headers: Content-Type, Authorization

3. If using AWS API Gateway, enable CORS in the console or add OPTIONS method""",
            },
            "wasm_not_supported": {
                "error": "WebAssembly is not supported",
                "solution": """
1. Ensure browser supports WebAssembly (Chrome 57+, Firefox 52+, Safari 11+)
2. For older browsers, use CanvasKit renderer:
   flutter build web --web-renderer canvaskit""",
            },
        },
    }

    DART_ERRORS = {
        "null_safety": {
            "non_nullable_error": {
                "error": "A value of type 'X?' can't be assigned to a variable of type 'X'",
                "solution": """
Options:
1. Use null check: value!
2. Use default value: value ?? defaultValue
3. Use conditional access: value?.property
4. Make variable nullable: X? variable

Best practice: Handle null at boundaries, avoid ! operator in business logic""",
            },
            "late_initialization": {
                "error": "LateInitializationError: Field 'X' has not been initialized",
                "solution": """
1. Ensure late variable is initialized before use
2. Consider using nullable type instead of late
3. Use late final for constants that need runtime initialization

Pattern:
late final ValueNotifier<User> _user;

@override
void initState() {
  super.initState();
  _user = ValueNotifier(initialUser);  // Initialize before use
}""",
            },
        },
        "async_errors": {
            "unawaited_future": {
                "error": "Future not awaited",
                "solution": """
1. Add await: await asyncFunction();
2. If intentionally fire-and-forget, use unawaited():
   unawaited(asyncFunction());
3. For side effects, use .then():
   asyncFunction().then((_) => print('done'));""",
            },
            "stream_error": {
                "error": "Bad state: Stream has already been listened to",
                "solution": """
1. Use broadcast stream for multiple listeners:
   final controller = StreamController<T>.broadcast();

2. Create new stream for each listener:
   Stream<T> get stream => controller.stream;

3. Use .asBroadcastStream() on existing stream""",
            },
        },
        "type_errors": {
            "type_cast": {
                "error": "type 'X' is not a subtype of type 'Y'",
                "solution": """
1. Use proper type checking:
   if (value is TargetType) { use(value); }

2. Use safe cast:
   final result = value as TargetType?;

3. For JSON parsing, use proper type:
   final map = json.decode(response) as Map<String, dynamic>;
   final list = (map['items'] as List).cast<Map<String, dynamic>>();""",
            },
        },
    }

    CLOUD_ERRORS = {
        "aws": {
            "credentials": {
                "error": "Unable to locate credentials",
                "solution": """
1. Configure AWS CLI: aws configure
2. Set environment variables:
   export AWS_ACCESS_KEY_ID=xxx
   export AWS_SECRET_ACCESS_KEY=xxx
3. For Lambda, ensure execution role has correct permissions
4. For ECS/EKS, use IAM roles for service accounts""",
            },
            "lambda_timeout": {
                "error": "Task timed out after X seconds",
                "solution": """
1. Increase Lambda timeout (max 15 minutes):
   timeout: 900

2. Optimize cold start:
   - Reduce package size
   - Use provisioned concurrency
   - Initialize SDK clients outside handler

3. For long tasks, use Step Functions or SQS""",
            },
            "dynamodb_throughput": {
                "error": "ProvisionedThroughputExceededException",
                "solution": """
1. Enable on-demand capacity mode
2. Increase provisioned capacity
3. Implement exponential backoff:
   for i in range(max_retries):
       try:
           result = table.get_item(Key=key)
           break
       except ClientError as e:
           if e.response['Error']['Code'] == 'ProvisionedThroughputExceededException':
               time.sleep(2 ** i)
           else:
               raise""",
            },
        },
        "firebase": {
            "permission_denied": {
                "error": "PERMISSION_DENIED: Missing or insufficient permissions",
                "solution": """
1. Check Firestore/Storage security rules
2. Verify user is authenticated
3. Check custom claims match rule requirements
4. Debug with:
   firebase emulators:start
   Test rules in Firebase Console Rules Playground""",
            },
            "quota_exceeded": {
                "error": "Quota exceeded",
                "solution": """
1. Check usage in Firebase Console
2. For Firestore:
   - Optimize queries with proper indexes
   - Use pagination
   - Cache results locally
3. For Storage:
   - Compress images before upload
   - Use CDN for frequently accessed files
4. Upgrade billing plan if needed""",
            },
        },
    }

    DEBUGGING = {
        "flutter": {
            "logs": """
# Debug logging
import 'package:flutter/foundation.dart';

if (kDebugMode) {
  debugPrint('Debug message');
}

# View logs
flutter logs

# Verbose output
flutter run -v""",
            "inspector": """
# Open DevTools
flutter pub global activate devtools
flutter pub global run devtools

# Or via IDE debugger
# VS Code: Cmd+Shift+P -> Flutter: Open DevTools
# Android Studio: View -> Tool Windows -> Flutter Inspector""",
            "performance": """
# Enable performance overlay
MaterialApp(
  showPerformanceOverlay: true,
)

# Profile mode build
flutter run --profile

# Check for jank
# - Green bars: good
# - Red bars: exceeding 16ms budget""",
        },
        "backend": {
            "lambda_logs": """
# View logs via CLI
aws logs tail /aws/lambda/function-name --follow

# Filter by request ID
aws logs filter-log-events \\
    --log-group-name /aws/lambda/function-name \\
    --filter-pattern "REQUEST_ID"

# Local testing
sam local invoke FunctionName -e event.json""",
            "api_testing": """
# Test with curl
curl -X POST https://api.example.com/endpoint \\
    -H "Content-Type: application/json" \\
    -H "Authorization: Bearer TOKEN" \\
    -d '{"key": "value"}'

# View response headers
curl -i https://api.example.com/endpoint

# Debug mode
curl -v https://api.example.com/endpoint""",
        },
    }

    COMMON_FIXES = {
        "clean_rebuild": """
# Flutter clean rebuild
flutter clean
flutter pub get
cd ios && pod install && cd ..
flutter build

# Dart clean
dart pub get

# Android specific
cd android && ./gradlew clean && cd ..

# iOS specific
cd ios && rm -rf Pods Podfile.lock && pod install && cd ..""",
        "dependency_conflicts": """
# View dependency tree
flutter pub deps

# Force resolution
# In pubspec.yaml, add dependency_overrides:
dependency_overrides:
  package_name: ^1.2.3

# Or upgrade all packages
flutter pub upgrade --major-versions""",
        "cache_issues": """
# Clear all caches
flutter pub cache repair
flutter clean
rm -rf ~/.pub-cache/hosted/pub.dev/
flutter pub get

# Clear iOS cache
cd ios && rm -rf ~/Library/Developer/Xcode/DerivedData
pod cache clean --all

# Clear Android cache
cd android && ./gradlew cleanBuildCache""",
    }

    def get_all(self) -> dict:
        """Get complete troubleshooting knowledge."""
        return {
            "version": self.VERSION,
            "flutter_build": self.FLUTTER_BUILD,
            "dart_errors": self.DART_ERRORS,
            "cloud_errors": self.CLOUD_ERRORS,
            "debugging": self.DEBUGGING,
            "common_fixes": self.COMMON_FIXES,
        }

    def get_flutter_build_errors(self) -> dict:
        """Get Flutter build error solutions."""
        return self.FLUTTER_BUILD

    def get_dart_errors(self) -> dict:
        """Get Dart error solutions."""
        return self.DART_ERRORS

    def get_cloud_errors(self) -> dict:
        """Get cloud service error solutions."""
        return self.CLOUD_ERRORS

    def get_debugging_tips(self) -> dict:
        """Get debugging tips."""
        return self.DEBUGGING
