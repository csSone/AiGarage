module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:vue/vue3-recommended',
    'prettier',
  ],
  parser: 'vue-eslint-parser',
  parserOptions: {
    ecmaVersion: 'latest',
    parser: '@typescript-eslint/parser',
    sourceType: 'module',
  },
  plugins: ['@typescript-eslint', 'vue'],
  rules: {
    // TypeScript specific rules
    '@typescript-eslint/no-explicit-any': 'warn',
    '@typescript-eslint/no-unused-vars': [
      'error',
      {
        argsIgnorePattern: '^_',
        varsIgnorePattern: '^_',
      },
    ],
    '@typescript-eslint/explicit-function-return-type': 'off',
    '@typescript-eslint/explicit-module-boundary-types': 'off',
    '@typescript-eslint/no-non-null-assertion': 'warn',

    // Vue specific rules
    'vue/multi-word-component-names': 'off',
    'vue/no-v-html': 'warn',
    'vue/require-default-prop': 'off',
    'vue/require-explicit-emits': 'error',
    'vue/component-name-in-template-casing': ['error', 'PascalCase'],
    'vue/component-definition-name-casing': ['error', 'PascalCase'],
    'vue/no-setup-props-destructure': 'warn',

    // General rules
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'prefer-const': 'error',
    'no-var': 'error',
  },
  globals: {
    // Auto-imported by unplugin-auto-import
    computed: 'readonly',
    createApp: 'readonly',
    customRef: 'readonly',
    defineComponent: 'readonly',
    defineProps: 'readonly',
    defineEmits: 'readonly',
    effectScope: 'readonly',
    getCurrentInstance: 'readonly',
    h: 'readonly',
    inject: 'readonly',
    isReadonly: 'readonly',
    isRef: 'readonly',
    markRaw: 'readonly',
    nextTick: 'readonly',
    onActivated: 'readonly',
    onBeforeMount: 'readonly',
    onBeforeUnmount: 'readonly',
    onBeforeUpdate: 'readonly',
    onDeactivated: 'readonly',
    onErrorCaptured: 'readonly',
    onMounted: 'readonly',
    onRenderTracked: 'readonly',
    onRenderTriggered: 'readonly',
    onScopeDispose: 'readonly',
    onServerPrefetch: 'readonly',
    onUnmounted: 'readonly',
    onUpdated: 'readonly',
    provide: 'readonly',
    reactive: 'readonly',
    readonly: 'readonly',
    ref: 'readonly',
    resolveComponent: 'readonly',
    shallowReactive: 'readonly',
    shallowReadonly: 'readonly',
    shallowRef: 'readonly',
    toRaw: 'readonly',
    toRef: 'readonly',
    toRefs: 'readonly',
    toValue: 'readonly',
    triggerRef: 'readonly',
    unref: 'readonly',
    useAttrs: 'readonly',
    useCssModule: 'readonly',
    useCssVars: 'readonly',
    useSlots: 'readonly',
    watch: 'readonly',
    watchEffect: 'readonly',
    watchPostEffect: 'readonly',
    watchSyncEffect: 'readonly',
  },
};

/*
 * Required dependencies:
 * npm install -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin eslint-plugin-vue eslint-config-prettier
 *
 * After installing, add these scripts to package.json:
 * "lint": "eslint . --ext .vue,.js,.jsx,.cjs,.mjs,.ts,.tsx,.cts,.mts --fix --ignore-path .gitignore"
 * "lint:check": "eslint . --ext .vue,.js,.jsx,.cjs,.mjs,.ts,.tsx,.cts,.mts --ignore-path .gitignore"
 */
