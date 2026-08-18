# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development commands

- `npm install` — install dependencies
- `npm run lint` — run ESLint
- `npm run format` — apply Prettier formatting; `npm run format:check` — check without writing
- `npm test` — run tests (Node's built-in test runner via `node --test`)
- Run a single test file: `node --test index.test.js`

## Architecture

This repository is still minimal (`frmlam/claude`): a single `index.js` module (`greet`) with a matching `index.test.js`, ESLint flat config in `eslint.config.js`, and a GitHub Actions CI workflow (`.github/workflows/ci.yml`) that installs dependencies, lints, and runs tests on every push/PR to `main`. As real modules are added, expand this section with how they interact.
