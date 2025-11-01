import js from '@eslint/js'
import vue from 'eslint-plugin-vue'
import prettier from 'eslint-plugin-prettier'

export default [
  js.configs.recommended,
  ...vue.configs['flat/recommended'],
  {
    plugins: { prettier },
    rules: {
      'vue/multi-word-component-names': 'off',
      'prettier/prettier': [
        'error',
        {
          semi: false,
          singleQuote: true,
          trailingComma: 'es5',
          printWidth: 100,
        },
      ],
    },
  },
]
