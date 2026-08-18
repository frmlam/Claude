import { execFileSync } from "node:child_process";
import { writeFileSync } from "node:fs";

const output = execFileSync(
  process.execPath,
  ["--test", "--experimental-test-coverage"],
  { encoding: "utf8", env: { ...process.env, NO_COLOR: "1" } },
);

const match = output.match(/^# all files\s*\|\s*([\d.]+)/m);
if (!match) {
  console.error(output);
  throw new Error("Could not find coverage percentage in test output");
}

const pct = Number(match[1]);
const color =
  pct >= 90
    ? "brightgreen"
    : pct >= 75
      ? "green"
      : pct >= 50
        ? "yellow"
        : pct >= 25
          ? "orange"
          : "red";

writeFileSync(
  "coverage-badge.json",
  JSON.stringify({
    schemaVersion: 1,
    label: "coverage",
    message: `${pct.toFixed(0)}%`,
    color,
  }) + "\n",
);

console.log(`Coverage: ${pct.toFixed(2)}%`);
