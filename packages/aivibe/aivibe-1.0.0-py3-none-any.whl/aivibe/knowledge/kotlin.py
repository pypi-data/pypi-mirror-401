"""
AIVibe Kotlin Knowledge Module

Complete Kotlin 2.0+ coding standards, Android development patterns,
Jetpack Compose, coroutines, and backend development with Ktor.
"""


class KotlinKnowledge:
    """Comprehensive Kotlin development knowledge."""

    VERSION = "2.0.0"
    TARGET_ANDROID_API = 36
    MIN_ANDROID_API = 24
    COMPOSE_BOM = "2024.06.00"

    LANGUAGE_FEATURES = {
        "null_safety": {
            "nullable_types": "String? for nullable, String for non-null",
            "safe_call": "obj?.property - returns null if obj is null",
            "elvis_operator": "value ?: default - provides default if null",
            "not_null_assertion": "value!! - throws NPE if null (avoid)",
            "let_scope": "value?.let { use(it) } - execute only if non-null",
            "also_scope": "value.also { log(it) } - side effects, returns original",
            "apply_scope": "obj.apply { prop = value } - configure and return",
            "run_scope": "obj.run { compute() } - compute and return result",
            "with_scope": "with(obj) { prop } - context object access",
            "lateinit": "lateinit var name: String - deferred initialization",
            "lazy": "val prop by lazy { expensive() } - lazy initialization",
        },
        "data_classes": {
            "definition": "data class User(val id: String, val name: String)",
            "copy": "user.copy(name = 'New Name') - immutable update",
            "destructuring": "val (id, name) = user",
            "component_functions": "user.component1(), user.component2()",
            "equals_hashcode": "Auto-generated based on properties",
            "toString": "Auto-generated: User(id=1, name=John)",
        },
        "sealed_classes": {
            "definition": """
sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val message: String) : Result<Nothing>()
    data object Loading : Result<Nothing>()
}""",
            "when_exhaustive": "when(result) must handle all cases",
            "sealed_interface": "sealed interface Event for interface hierarchies",
        },
        "value_classes": {
            "definition": "@JvmInline value class UserId(val value: String)",
            "type_safety": "Compile-time type distinction with zero overhead",
            "restrictions": "Single property, no init block",
        },
        "context_receivers": {
            "definition": "context(LogContext, DbContext) fun process()",
            "usage": "Implicit receivers for cleaner APIs",
        },
        "k2_compiler": {
            "benefits": "2x faster compilation, better type inference",
            "enable": "kotlin.experimental.tryK2=true in gradle.properties",
        },
    }

    COROUTINES = {
        "basics": {
            "launch": "launch { } - fire and forget, returns Job",
            "async": "async { } - returns Deferred<T> with await()",
            "runBlocking": "runBlocking { } - blocks thread (tests only)",
            "withContext": "withContext(Dispatchers.IO) { } - switch context",
            "suspend": "suspend fun fetch(): Data - suspending function",
        },
        "dispatchers": {
            "Main": "UI thread for Android",
            "IO": "Optimized for I/O operations (network, disk)",
            "Default": "CPU-intensive work (sorting, parsing)",
            "Unconfined": "Starts in caller thread (use carefully)",
        },
        "flow": {
            "cold_flow": """
fun dataFlow(): Flow<Data> = flow {
    emit(fetchData())
    delay(1000)
    emit(fetchMoreData())
}""",
            "state_flow": """
private val _state = MutableStateFlow(UiState())
val state: StateFlow<UiState> = _state.asStateFlow()""",
            "shared_flow": """
private val _events = MutableSharedFlow<Event>()
val events: SharedFlow<Event> = _events.asSharedFlow()""",
            "operators": {
                "map": "flow.map { transform(it) }",
                "filter": "flow.filter { it.isValid }",
                "flatMapConcat": "flow.flatMapConcat { innerFlow(it) }",
                "combine": "combine(flow1, flow2) { a, b -> merge(a, b) }",
                "debounce": "flow.debounce(300) for search input",
                "distinctUntilChanged": "Emit only when value changes",
                "catch": "flow.catch { emit(fallback) }",
                "onEach": "flow.onEach { log(it) }",
            },
            "collecting": {
                "collect": "flow.collect { handle(it) }",
                "collectLatest": "Cancel previous on new emission",
                "first": "flow.first() - first emission",
                "toList": "flow.toList() - collect all",
            },
        },
        "structured_concurrency": {
            "coroutine_scope": """
coroutineScope {
    val a = async { fetchA() }
    val b = async { fetchB() }
    Result(a.await(), b.await())
}""",
            "supervisor_scope": "supervisorScope { } - child failures don't cancel siblings",
            "cancellation": "job.cancel(), isActive check, ensureActive()",
            "exception_handling": """
val handler = CoroutineExceptionHandler { _, e ->
    log.error("Coroutine failed", e)
}
scope.launch(handler) { }""",
        },
    }

    JETPACK_COMPOSE = {
        "composables": {
            "stateless": """
@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Text(
        text = "Hello, $name!",
        modifier = modifier
    )
}""",
            "stateful": """
@Composable
fun Counter() {
    var count by remember { mutableStateOf(0) }

    Button(onClick = { count++ }) {
        Text("Count: $count")
    }
}""",
            "hoisted_state": """
@Composable
fun Counter(
    count: Int,
    onCountChange: (Int) -> Unit,
    modifier: Modifier = Modifier
) {
    Button(
        onClick = { onCountChange(count + 1) },
        modifier = modifier
    ) {
        Text("Count: $count")
    }
}""",
        },
        "state": {
            "remember": "remember { mutableStateOf(initial) }",
            "rememberSaveable": "Survives configuration changes",
            "derivedStateOf": "remember { derivedStateOf { expensive(state) } }",
            "produceState": "Convert Flow to State",
            "collectAsState": "flow.collectAsState(initial)",
            "collectAsStateWithLifecycle": "Lifecycle-aware collection",
        },
        "side_effects": {
            "LaunchedEffect": """
LaunchedEffect(key1) {
    // Runs when key1 changes
    val result = fetchData()
}""",
            "DisposableEffect": """
DisposableEffect(key1) {
    val listener = createListener()
    onDispose { listener.remove() }
}""",
            "SideEffect": "Run on every successful recomposition",
            "rememberCoroutineScope": "val scope = rememberCoroutineScope()",
            "rememberUpdatedState": "Capture latest value in long-running effect",
        },
        "navigation": {
            "setup": """
val navController = rememberNavController()
NavHost(navController, startDestination = "home") {
    composable("home") { HomeScreen(navController) }
    composable("detail/{id}") { backStackEntry ->
        DetailScreen(backStackEntry.arguments?.getString("id"))
    }
}""",
            "navigate": "navController.navigate('detail/$id')",
            "pop_back": "navController.popBackStack()",
            "deep_link": "composable('item/{id}', deepLinks = listOf(navDeepLink { }))",
        },
        "theming": {
            "material3": """
MaterialTheme(
    colorScheme = if (darkTheme) darkColorScheme() else lightColorScheme(),
    typography = Typography,
    content = content
)""",
            "custom_colors": "LocalContentColor, CompositionLocalProvider",
        },
        "performance": {
            "stable": "@Stable annotation for skip optimization",
            "immutable": "@Immutable for data classes",
            "key": "key(id) { Item(data) } for list recomposition",
            "derivedStateOf": "Avoid unnecessary recomposition",
            "remember_lambda": "remember { { onClick() } }",
        },
    }

    ANDROID_ARCHITECTURE = {
        "mvvm": {
            "viewmodel": """
@HiltViewModel
class HomeViewModel @Inject constructor(
    private val repository: DataRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(HomeUiState())
    val uiState: StateFlow<HomeUiState> = _uiState.asStateFlow()

    fun loadData() {
        viewModelScope.launch {
            _uiState.update { it.copy(loading = true) }
            repository.getData()
                .onSuccess { data ->
                    _uiState.update { it.copy(loading = false, data = data) }
                }
                .onFailure { error ->
                    _uiState.update { it.copy(loading = false, error = error.message) }
                }
        }
    }
}""",
            "ui_state": """
data class HomeUiState(
    val loading: Boolean = false,
    val data: List<Item> = emptyList(),
    val error: String? = null
)""",
        },
        "repository": {
            "interface": """
interface DataRepository {
    suspend fun getData(): Result<List<Item>>
    suspend fun saveItem(item: Item): Result<Unit>
    fun observeItems(): Flow<List<Item>>
}""",
            "implementation": """
class DataRepositoryImpl @Inject constructor(
    private val remoteDataSource: RemoteDataSource,
    private val localDataSource: LocalDataSource,
    private val dispatcher: CoroutineDispatcher
) : DataRepository {

    override suspend fun getData(): Result<List<Item>> = withContext(dispatcher) {
        runCatching {
            val remote = remoteDataSource.fetch()
            localDataSource.cache(remote)
            remote
        }.recoverCatching {
            localDataSource.getAll()
        }
    }
}""",
        },
        "hilt": {
            "module": """
@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {
    @Binds
    @Singleton
    abstract fun bindRepository(impl: DataRepositoryImpl): DataRepository
}""",
            "provides": """
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    @Provides
    @Singleton
    fun provideOkHttpClient(): OkHttpClient = OkHttpClient.Builder()
        .addInterceptor(HttpLoggingInterceptor())
        .build()
}""",
        },
    }

    KTOR_BACKEND = {
        "server": {
            "setup": """
fun main() {
    embeddedServer(Netty, port = 8080, module = Application::module).start(wait = true)
}

fun Application.module() {
    configureSerialization()
    configureRouting()
    configureSecurity()
}""",
            "routing": """
fun Application.configureRouting() {
    routing {
        get("/") { call.respondText("Hello") }

        route("/api/v1") {
            userRoutes()
            itemRoutes()
        }
    }
}

fun Route.userRoutes() {
    route("/users") {
        get {
            val users = userService.getAll()
            call.respond(users)
        }
        get("/{id}") {
            val id = call.parameters["id"] ?: throw BadRequestException("Missing id")
            val user = userService.getById(id)
            call.respond(user)
        }
        post {
            val request = call.receive<CreateUserRequest>()
            val user = userService.create(request)
            call.respond(HttpStatusCode.Created, user)
        }
    }
}""",
            "serialization": """
fun Application.configureSerialization() {
    install(ContentNegotiation) {
        json(Json {
            prettyPrint = true
            isLenient = true
            ignoreUnknownKeys = true
        })
    }
}""",
        },
        "authentication": """
fun Application.configureSecurity() {
    install(Authentication) {
        jwt("auth-jwt") {
            realm = "app"
            verifier(
                JWT.require(Algorithm.HMAC256(secret))
                    .withAudience(audience)
                    .withIssuer(issuer)
                    .build()
            )
            validate { credential ->
                if (credential.payload.audience.contains(audience)) {
                    JWTPrincipal(credential.payload)
                } else null
            }
        }
    }
}

// Protected route
authenticate("auth-jwt") {
    get("/protected") {
        val principal = call.principal<JWTPrincipal>()
        val userId = principal!!.payload.getClaim("userId").asString()
        call.respond(mapOf("userId" to userId))
    }
}""",
    }

    CODING_STANDARDS = {
        "naming": {
            "classes": "PascalCase - UserRepository, DataManager",
            "functions": "camelCase - fetchData, processItems",
            "properties": "camelCase - userName, isActive",
            "constants": "SCREAMING_SNAKE_CASE - MAX_RETRY_COUNT",
            "backing_properties": "_camelCase - private val _state",
            "type_parameters": "Single uppercase - T, K, V or descriptive",
            "packages": "lowercase.with.dots - com.company.feature",
        },
        "formatting": {
            "indentation": "4 spaces, no tabs",
            "line_length": "120 characters max",
            "blank_lines": "Single between functions, double between classes",
            "trailing_comma": "Always use in multi-line collections",
            "imports": "No wildcards, organize by package",
        },
        "functions": {
            "single_expression": "fun double(x: Int) = x * 2",
            "default_parameters": "fun greet(name: String = 'World')",
            "named_arguments": "createUser(name = 'John', age = 30)",
            "extension_functions": "fun String.isEmail() = contains('@')",
            "infix_functions": "infix fun Int.times(str: String) = str.repeat(this)",
            "operator_overloading": "operator fun plus(other: Point): Point",
        },
        "classes": {
            "primary_constructor": "class User(val name: String, private val id: String)",
            "init_blocks": "init { require(name.isNotBlank()) }",
            "companion_object": "companion object { fun create(): User }",
            "object_declaration": "object Singleton { fun instance() }",
        },
        "documentation": {
            "kdoc": """
/**
 * Fetches user data from the remote server.
 *
 * @param userId The unique identifier of the user
 * @return [Result] containing [User] on success or error details
 * @throws NetworkException if connection fails
 * @see UserRepository.cacheUser
 */
suspend fun fetchUser(userId: String): Result<User>""",
        },
        "error_handling": {
            "result_type": """
sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val exception: Throwable) : Result<Nothing>()
}

// Usage
when (val result = repository.fetch()) {
    is Result.Success -> handleData(result.data)
    is Result.Error -> handleError(result.exception)
}""",
            "runCatching": """
val result = runCatching { riskyOperation() }
    .onSuccess { data -> log("Got: $data") }
    .onFailure { e -> log("Failed: ${e.message}") }
    .getOrDefault(fallback)""",
        },
    }

    DEPRECATED = {
        "packages": [
            "kotlin-android-extensions (use ViewBinding or Compose)",
            "kotlinx.android.synthetic (use ViewBinding)",
            "kapt (migrate to KSP where possible)",
        ],
        "patterns": [
            "GlobalScope.launch (use structured concurrency)",
            "runBlocking in production code",
            "Thread.sleep in coroutines (use delay)",
            "callback-based APIs (convert to suspend/Flow)",
            "LiveData in new code (use StateFlow)",
            "findViewById (use ViewBinding or Compose)",
        ],
        "android": [
            "AsyncTask (use coroutines)",
            "Loader (use ViewModel + Flow)",
            "LocalBroadcastManager (use Flow/SharedFlow)",
            "IntentService (use WorkManager)",
        ],
    }

    def get_all(self) -> dict:
        """Get complete Kotlin knowledge."""
        return {
            "version": self.VERSION,
            "target_android_api": self.TARGET_ANDROID_API,
            "language_features": self.LANGUAGE_FEATURES,
            "coroutines": self.COROUTINES,
            "jetpack_compose": self.JETPACK_COMPOSE,
            "android_architecture": self.ANDROID_ARCHITECTURE,
            "ktor_backend": self.KTOR_BACKEND,
            "coding_standards": self.CODING_STANDARDS,
            "deprecated": self.DEPRECATED,
        }

    def get_coding_standards(self) -> dict:
        """Get Kotlin coding standards."""
        return self.CODING_STANDARDS

    def get_coroutines_guide(self) -> dict:
        """Get coroutines best practices."""
        return self.COROUTINES

    def get_compose_patterns(self) -> dict:
        """Get Jetpack Compose patterns."""
        return self.JETPACK_COMPOSE
