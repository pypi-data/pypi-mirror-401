"""
AIVibe JavaScript/TypeScript Knowledge Module

Complete ES2024/TypeScript 5.5+ coding standards, React patterns,
Node.js backend development, and modern JavaScript features.
"""


class JavaScriptKnowledge:
    """Comprehensive JavaScript/TypeScript development knowledge."""

    VERSION = "ES2024"
    TYPESCRIPT_VERSION = "5.5"
    NODE_VERSION = "22"
    REACT_VERSION = "18.3"

    LANGUAGE_FEATURES = {
        "es2024": {
            "array_grouping": """
const grouped = Object.groupBy(users, user => user.role);
// { admin: [...], user: [...] }

const mapped = Map.groupBy(items, item => item.category);
// Map { 'electronics' => [...], 'books' => [...] }""",
            "promise_withResolvers": """
const { promise, resolve, reject } = Promise.withResolvers<T>();
// Use resolve/reject externally""",
            "array_toSorted": """
const sorted = array.toSorted((a, b) => a - b);  // Non-mutating
const reversed = array.toReversed();  // Non-mutating
const spliced = array.toSpliced(1, 2, 'new');  // Non-mutating""",
            "array_at": "const last = array.at(-1);  // Negative indexing",
            "object_hasOwn": "Object.hasOwn(obj, 'prop')  // Instead of hasOwnProperty",
            "regexp_v_flag": "/[\\p{Script=Greek}&&\\p{Letter}]/v  // Set notation",
        },
        "typescript_5_5": {
            "inferred_type_predicates": """
// TypeScript infers the return type as `x is number`
function isNumber(x: unknown) {
    return typeof x === 'number';
}

const nums = [1, 'a', 2, 'b'].filter(isNumber);
// nums is number[] (auto-inferred!)""",
            "const_type_parameters": """
function identity<const T>(value: T): T {
    return value;
}
// Preserves literal types""",
            "satisfies_operator": """
const config = {
    port: 3000,
    host: 'localhost'
} satisfies ServerConfig;
// Type-checks without widening""",
            "using_keyword": """
// Explicit resource management
async function process() {
    await using db = await connectDatabase();
    // db automatically disposed when scope exits
}""",
            "decorators": """
function log(originalMethod: any, context: ClassMethodDecoratorContext) {
    return function (...args: any[]) {
        console.log(`Calling ${String(context.name)}`);
        return originalMethod.apply(this, args);
    };
}

class Service {
    @log
    process() { }
}""",
        },
        "typescript_types": {
            "utility_types": {
                "Partial<T>": "All properties optional",
                "Required<T>": "All properties required",
                "Readonly<T>": "All properties readonly",
                "Pick<T, K>": "Pick specific properties",
                "Omit<T, K>": "Omit specific properties",
                "Record<K, V>": "Object type with key K and value V",
                "Extract<T, U>": "Extract types assignable to U",
                "Exclude<T, U>": "Exclude types assignable to U",
                "NonNullable<T>": "Exclude null and undefined",
                "ReturnType<T>": "Return type of function",
                "Parameters<T>": "Parameter types as tuple",
                "Awaited<T>": "Unwrap Promise type",
            },
            "conditional_types": """
type IsString<T> = T extends string ? true : false;

type ExtractArrayType<T> = T extends (infer U)[] ? U : never;

type UnwrapPromise<T> = T extends Promise<infer U> ? U : T;""",
            "mapped_types": """
type Nullable<T> = { [K in keyof T]: T[K] | null };

type Getters<T> = {
    [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};""",
            "template_literal_types": """
type EventName = `on${Capitalize<string>}`;
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';
type Endpoint = `/${string}`;
type Route = `${HttpMethod} ${Endpoint}`;""",
        },
    }

    REACT_PATTERNS = {
        "components": {
            "functional": """
interface UserCardProps {
    user: User;
    onSelect?: (user: User) => void;
}

export function UserCard({ user, onSelect }: UserCardProps) {
    return (
        <div className="user-card" onClick={() => onSelect?.(user)}>
            <h3>{user.name}</h3>
            <p>{user.email}</p>
        </div>
    );
}""",
            "with_children": """
interface ContainerProps {
    children: React.ReactNode;
    className?: string;
}

export function Container({ children, className }: ContainerProps) {
    return <div className={cn('container', className)}>{children}</div>;
}""",
            "forwardRef": """
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
    label: string;
    error?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
    ({ label, error, className, ...props }, ref) => (
        <div className="input-wrapper">
            <label>{label}</label>
            <input ref={ref} className={cn('input', className)} {...props} />
            {error && <span className="error">{error}</span>}
        </div>
    )
);
Input.displayName = 'Input';""",
        },
        "hooks": {
            "useState": "const [state, setState] = useState<T>(initial);",
            "useReducer": """
type Action = { type: 'increment' } | { type: 'set'; value: number };

function reducer(state: number, action: Action): number {
    switch (action.type) {
        case 'increment': return state + 1;
        case 'set': return action.value;
    }
}

const [count, dispatch] = useReducer(reducer, 0);""",
            "useCallback": """
const handleClick = useCallback((id: string) => {
    selectItem(id);
}, [selectItem]);""",
            "useMemo": """
const expensiveValue = useMemo(() => {
    return computeExpensiveValue(a, b);
}, [a, b]);""",
            "useRef": """
const inputRef = useRef<HTMLInputElement>(null);
const valueRef = useRef<number>(0);  // For mutable values""",
            "useEffect": """
useEffect(() => {
    const subscription = subscribe(handler);
    return () => subscription.unsubscribe();
}, [handler]);""",
            "useTransition": """
const [isPending, startTransition] = useTransition();

function handleClick() {
    startTransition(() => {
        setExpensiveState(newValue);
    });
}""",
            "useDeferredValue": """
const deferredQuery = useDeferredValue(query);
// Use deferredQuery for expensive renders""",
        },
        "custom_hooks": """
function useDebounce<T>(value: T, delay: number): T {
    const [debouncedValue, setDebouncedValue] = useState(value);

    useEffect(() => {
        const timer = setTimeout(() => setDebouncedValue(value), delay);
        return () => clearTimeout(timer);
    }, [value, delay]);

    return debouncedValue;
}

function useLocalStorage<T>(key: string, initialValue: T) {
    const [storedValue, setStoredValue] = useState<T>(() => {
        try {
            const item = window.localStorage.getItem(key);
            return item ? JSON.parse(item) : initialValue;
        } catch {
            return initialValue;
        }
    });

    const setValue = useCallback((value: T | ((val: T) => T)) => {
        const valueToStore = value instanceof Function ? value(storedValue) : value;
        setStoredValue(valueToStore);
        window.localStorage.setItem(key, JSON.stringify(valueToStore));
    }, [key, storedValue]);

    return [storedValue, setValue] as const;
}""",
        "error_boundary": """
interface ErrorBoundaryProps {
    children: React.ReactNode;
    fallback: React.ReactNode;
}

interface ErrorBoundaryState {
    hasError: boolean;
    error?: Error;
}

class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
    constructor(props: ErrorBoundaryProps) {
        super(props);
        this.state = { hasError: false };
    }

    static getDerivedStateFromError(error: Error) {
        return { hasError: true, error };
    }

    componentDidCatch(error: Error, errorInfo: ErrorInfo) {
        console.error('Error caught:', error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            return this.props.fallback;
        }
        return this.props.children;
    }
}""",
        "server_components": """
// Server Component (default in App Router)
async function UserList() {
    const users = await fetchUsers();  // Direct async in component
    return (
        <ul>
            {users.map(user => <UserItem key={user.id} user={user} />)}
        </ul>
    );
}

// Client Component
'use client';

function Counter() {
    const [count, setCount] = useState(0);
    return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}""",
    }

    NODEJS = {
        "express_alternative": """
// Use Hono for modern TypeScript-first API
import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { jwt } from 'hono/jwt';

const app = new Hono();

app.use('*', cors());
app.use('/api/*', jwt({ secret: process.env.JWT_SECRET! }));

app.get('/api/users', async (c) => {
    const users = await userService.getAll();
    return c.json(users);
});

app.post('/api/users', async (c) => {
    const body = await c.req.json();
    const user = await userService.create(body);
    return c.json(user, 201);
});

export default app;""",
        "error_handling": """
class AppError extends Error {
    constructor(
        public code: string,
        message: string,
        public statusCode: number = 400
    ) {
        super(message);
        this.name = 'AppError';
    }
}

// Global error handler
app.onError((err, c) => {
    if (err instanceof AppError) {
        return c.json({ code: err.code, message: err.message }, err.statusCode);
    }
    console.error(err);
    return c.json({ code: 'INTERNAL_ERROR', message: 'Something went wrong' }, 500);
});""",
        "validation": """
import { z } from 'zod';
import { zValidator } from '@hono/zod-validator';

const CreateUserSchema = z.object({
    name: z.string().min(1).max(100),
    email: z.string().email(),
    age: z.number().int().min(0).max(150).optional(),
});

app.post('/api/users',
    zValidator('json', CreateUserSchema),
    async (c) => {
        const data = c.req.valid('json');
        const user = await userService.create(data);
        return c.json(user, 201);
    }
);""",
        "database": """
import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';

const client = postgres(process.env.DATABASE_URL!);
const db = drizzle(client);

// Schema
import { pgTable, text, timestamp, uuid } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
    id: uuid('id').primaryKey().defaultRandom(),
    name: text('name').notNull(),
    email: text('email').notNull().unique(),
    createdAt: timestamp('created_at').defaultNow(),
});

// Queries
const allUsers = await db.select().from(users);
const user = await db.select().from(users).where(eq(users.id, id));
await db.insert(users).values({ name, email });
await db.update(users).set({ name }).where(eq(users.id, id));
await db.delete(users).where(eq(users.id, id));""",
    }

    TESTING = {
        "vitest": """
import { describe, it, expect, vi, beforeEach } from 'vitest';

describe('UserService', () => {
    let service: UserService;
    let mockRepo: MockProxy<UserRepository>;

    beforeEach(() => {
        mockRepo = mock<UserRepository>();
        service = new UserService(mockRepo);
    });

    it('should return user by id', async () => {
        const expected = { id: '1', name: 'Test' };
        mockRepo.findById.mockResolvedValue(expected);

        const result = await service.getById('1');

        expect(result).toEqual(expected);
        expect(mockRepo.findById).toHaveBeenCalledWith('1');
    });

    it('should throw when user not found', async () => {
        mockRepo.findById.mockResolvedValue(null);

        await expect(service.getById('999')).rejects.toThrow('User not found');
    });
});""",
        "react_testing": """
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('LoginForm', () => {
    it('should submit with valid credentials', async () => {
        const onSubmit = vi.fn();
        render(<LoginForm onSubmit={onSubmit} />);

        await userEvent.type(screen.getByLabelText(/email/i), 'test@example.com');
        await userEvent.type(screen.getByLabelText(/password/i), 'password123');
        await userEvent.click(screen.getByRole('button', { name: /login/i }));

        await waitFor(() => {
            expect(onSubmit).toHaveBeenCalledWith({
                email: 'test@example.com',
                password: 'password123',
            });
        });
    });

    it('should show validation errors', async () => {
        render(<LoginForm onSubmit={vi.fn()} />);

        await userEvent.click(screen.getByRole('button', { name: /login/i }));

        expect(await screen.findByText(/email is required/i)).toBeInTheDocument();
    });
});""",
        "playwright": """
import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
    test('should login successfully', async ({ page }) => {
        await page.goto('/login');
        await page.fill('[name="email"]', 'user@example.com');
        await page.fill('[name="password"]', 'password');
        await page.click('button[type="submit"]');

        await expect(page).toHaveURL('/dashboard');
        await expect(page.locator('h1')).toContainText('Welcome');
    });

    test('should show error on invalid credentials', async ({ page }) => {
        await page.goto('/login');
        await page.fill('[name="email"]', 'wrong@example.com');
        await page.fill('[name="password"]', 'wrong');
        await page.click('button[type="submit"]');

        await expect(page.locator('.error')).toContainText('Invalid credentials');
    });
});""",
    }

    CODING_STANDARDS = {
        "naming": {
            "variables": "camelCase - userName, isActive",
            "constants": "SCREAMING_SNAKE_CASE - MAX_RETRIES",
            "functions": "camelCase - getUserById, handleClick",
            "classes": "PascalCase - UserService, DataRepository",
            "interfaces": "PascalCase (no I prefix) - User, Config",
            "types": "PascalCase - UserProps, ApiResponse",
            "enums": "PascalCase with UPPER values - Status.ACTIVE",
            "files": "kebab-case or PascalCase - user-service.ts, UserCard.tsx",
            "components": "PascalCase - UserCard.tsx, LoginForm.tsx",
        },
        "formatting": {
            "tool": "prettier + eslint",
            "line_length": 100,
            "indentation": "2 spaces",
            "quotes": "single quotes for JS/TS",
            "semicolons": "required",
            "trailing_comma": "es5 or all",
        },
        "imports": {
            "order": "external, internal, relative, types",
            "barrel_exports": "Use index.ts for public API only",
            "type_imports": "import type { User } from './types';",
            "avoid": "default exports for utilities (named preferred)",
        },
        "typescript": {
            "strict": "Enable all strict options",
            "explicit_returns": "Always type function returns",
            "no_any": "Use unknown instead of any",
            "readonly": "Use readonly for immutable data",
            "const_assertion": "as const for literal types",
        },
        "documentation": {
            "jsdoc": """
/**
 * Fetches a user by their unique identifier.
 *
 * @param id - The unique user identifier
 * @returns The user object or null if not found
 * @throws {AuthError} If not authenticated
 *
 * @example
 * ```ts
 * const user = await getUserById('123');
 * ```
 */""",
        },
    }

    DEPRECATED = {
        "patterns": [
            "var (use const/let)",
            "function keyword for callbacks (use arrow)",
            "arguments object (use rest parameters)",
            "for...in for arrays (use for...of or forEach)",
            ".then().catch() (prefer async/await)",
            "require() in ESM (use import)",
            "module.exports (use export)",
            "class components in React (use functional)",
            "PropTypes (use TypeScript)",
            "enzyme (use React Testing Library)",
        ],
        "packages": [
            "moment.js (use date-fns or dayjs)",
            "lodash (use native methods when possible)",
            "request (deprecated, use fetch/axios)",
            "express for new TS projects (use Hono/Fastify)",
            "create-react-app (use Vite or Next.js)",
            "jest for new projects (prefer Vitest)",
        ],
        "react": [
            "componentWillMount/Update (use useEffect)",
            "componentWillReceiveProps (use useEffect)",
            "UNSAFE_ lifecycle methods",
            "string refs (use useRef)",
            "findDOMNode (use refs)",
            "React.createClass (use function/class)",
        ],
    }

    def get_all(self) -> dict:
        """Get complete JavaScript/TypeScript knowledge."""
        return {
            "version": self.VERSION,
            "typescript_version": self.TYPESCRIPT_VERSION,
            "language_features": self.LANGUAGE_FEATURES,
            "react_patterns": self.REACT_PATTERNS,
            "nodejs": self.NODEJS,
            "testing": self.TESTING,
            "coding_standards": self.CODING_STANDARDS,
            "deprecated": self.DEPRECATED,
        }

    def get_coding_standards(self) -> dict:
        """Get JavaScript/TypeScript coding standards."""
        return self.CODING_STANDARDS

    def get_react_patterns(self) -> dict:
        """Get React patterns."""
        return self.REACT_PATTERNS

    def get_typescript_types(self) -> dict:
        """Get TypeScript type patterns."""
        return self.LANGUAGE_FEATURES["typescript_types"]
