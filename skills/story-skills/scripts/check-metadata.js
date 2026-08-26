#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parseFrontmatter } from "../src/frontmatter.js";

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const failures = [];

const packageJson = readJson("package.json");
const codexPlugin = readJson(".codex-plugin/plugin.json");
const claudePlugin = readJson(".claude-plugin/plugin.json");

expectEqual("package.json name", packageJson.name, codexPlugin.name);
expectEqual("package.json name", packageJson.name, claudePlugin.name);
expectEqual("package/plugin version", packageJson.version, codexPlugin.version);
expectEqual("package/plugin version", packageJson.version, claudePlugin.version);

if (codexPlugin.skills !== "./skills/") {
  failures.push(".codex-plugin/plugin.json skills must point to ./skills/");
}

const skillsDir = path.join(repoRoot, "skills");
for (const skillName of fs.readdirSync(skillsDir).sort()) {
  const skillDir = path.join(skillsDir, skillName);
  if (!fs.statSync(skillDir).isDirectory()) {
    continue;
  }

  const skillPath = path.join(skillDir, "SKILL.md");
  if (!fs.existsSync(skillPath)) {
    failures.push(`skills/${skillName} is missing SKILL.md`);
    continue;
  }

  const markdown = fs.readFileSync(skillPath, "utf8");
  const frontmatter = parseFrontmatter(markdown, skillPath).data;
  expectEqual(`skills/${skillName}/SKILL.md name`, skillName, frontmatter.name);
  if (typeof frontmatter.description !== "string" || frontmatter.description.trim() === "") {
    failures.push(`skills/${skillName}/SKILL.md is missing description`);
  }
}

if (failures.length > 0) {
  console.error(`Metadata check failed:\n${failures.join("\n")}`);
  process.exit(1);
}

console.log(`Metadata is aligned for ${packageJson.name}@${packageJson.version}.`);

function readJson(relativePath) {
  return JSON.parse(fs.readFileSync(path.join(repoRoot, relativePath), "utf8"));
}

function expectEqual(label, expected, actual) {
  if (actual !== expected) {
    failures.push(`${label} mismatch: expected ${expected}, got ${actual}`);
  }
}
