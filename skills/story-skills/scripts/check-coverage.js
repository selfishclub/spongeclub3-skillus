#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

const [lcovPath, sourceDir] = process.argv.slice(2);
if (!lcovPath || !sourceDir) {
  console.error("Usage: check-coverage <lcov.info> <source-dir>");
  process.exit(1);
}

const lcov = fs.readFileSync(lcovPath, "utf8");
const requiredFiles = fs.readdirSync(sourceDir)
  .filter((file) => file.endsWith(".js"))
  .map((file) => path.resolve(sourceDir, file));
const records = parseLcov(lcov);
const failures = [];

for (const filePath of requiredFiles) {
  const record = records.get(filePath);
  if (!record) {
    failures.push(`${filePath} has no coverage record`);
    continue;
  }

  if (record.lines.found !== record.lines.hit) {
    failures.push(`${filePath} line coverage ${record.lines.hit}/${record.lines.found}`);
  }

  if (record.functions.found !== record.functions.hit) {
    failures.push(`${filePath} function coverage ${record.functions.hit}/${record.functions.found}`);
  }
}

if (failures.length > 0) {
  console.error(`Coverage is below 100%:\n${failures.join("\n")}`);
  process.exit(1);
}

console.log("Coverage is 100% for src line and function coverage.");

function parseLcov(source) {
  const records = new Map();
  let current = null;

  for (const line of source.split(/\r?\n/)) {
    if (line.startsWith("SF:")) {
      current = {
        file: path.resolve(line.slice(3)),
        lines: { found: 0, hit: 0 },
        functions: { found: 0, hit: 0 }
      };
      records.set(current.file, current);
    } else if (line.startsWith("LF:")) {
      current.lines.found = Number(line.slice(3));
    } else if (line.startsWith("LH:")) {
      current.lines.hit = Number(line.slice(3));
    } else if (line.startsWith("FNF:")) {
      current.functions.found = Number(line.slice(4));
    } else if (line.startsWith("FNH:")) {
      current.functions.hit = Number(line.slice(4));
    }
  }

  return records;
}
