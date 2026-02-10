/* eslint-env node */
require('@rushstack/eslint-patch/modern-module-resolution')

module.exports = {
  root: true,
  'extends': [
    'plugin:vue/vue3-essential',
    'eslint:recommended',
    '@vue/eslint-config-prettier/skip-formatting'
  ],
  parserOptions: {
    ecmaVersion: 'latest'
  },
  rules:{
    'prettier/prettier': [
      'warn',
      {
        'singleQuote': true,
        'printWidth': 80,
        'tabWidth': 2,
        'semi': false,
        'trailingComma': 'none',
        'bracketSpacing': true,
        'arrowParens': 'always',
        'endOfLine': 'auto'
      }
    ],
    'vue/multi-word-component-names':[
      'warn',
      {
        ignores:['index']
      }
    ],
    'vue/no-setup-props-destructure':['off'],
    'no-undef': 'ereror',
  },
  globals: {
    ElMessage: 'readonly',
    ElMessageBox: 'readonly',
    ELLoading: 'readonly'
   
  
  }
}
