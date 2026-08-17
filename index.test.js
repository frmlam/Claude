import test from "node:test";
import assert from "node:assert/strict";
import { greet } from "./index.js";

test("greet returns a greeting with the given name", () => {
  assert.equal(greet("World"), "Hello, World!");
});
