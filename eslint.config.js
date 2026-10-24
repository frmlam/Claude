import js from "@eslint/js";
import prettier from "eslint-config-prettier";

export default [
  { ignores: ["skills/unlazy/**"] },
  js.configs.recommended,
  {
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      globals: {
        console: "readonly",
        process: "readonly",
      },
    },
  },
  prettier,
];
