export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',     // New feature
        'fix',      // Bug fix
        'docs',     // Documentation only
        'style',    // Formatting, missing semi colons
        'refactor', // Code change that neither fixes a bug nor adds a feature
        'perf',     // Performance improvement
        'test',     // Adding tests
        'chore',    // Updating build tasks, package manager configs
        'revert',   // Reverting a previous commit
        'build',    // Changes to build system or dependencies
        'ci',       // CI configuration changes
        'deps',     // Dependency updates
      ],
    ],
    'scope-enum': [
      2,
      'always',
      [
        'client',      // Main SDK client
        'resources',   // Resource classes (memories, spaces, audio, etc.)
        'models',      // Pydantic models and type definitions
        'auth',        // Authentication and API key handling
        'http',        // HTTP client and request handling
        'errors',      // Error handling and exceptions
        'types',       // Type hints and typing utilities
        'telemetry',   // OpenTelemetry integration
        'examples',    // Example code and usage demos
        'tests',       // Test suite
        'deps',        // Dependencies
        'config',      // Configuration
        'docs',        // Documentation
        'build',       // Build system (setuptools, pyproject.toml)
      ],
    ],
    'subject-case': [2, 'always', 'sentence-case'],
    'body-max-line-length': [1, 'always', 100],
  },
};
