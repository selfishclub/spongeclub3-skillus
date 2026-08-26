#!/usr/bin/env node

import { execSync } from "node:child_process";
import { existsSync, mkdirSync, cpSync, rmSync, readFileSync } from "node:fs";
import { readdirSync } from "node:fs";
import { join } from "node:path";
import { homedir, tmpdir } from "node:os";

const REPO = "https://github.com/OpenClaudia/openclaudia-skills.git";
const SKILLS_DIR = join(homedir(), ".claude", "skills");

const args = process.argv.slice(2);
const command = args[0];

function printHelp() {
  console.log(`
  openclaudia - Marketing skills for Claude Code

  Usage:
    npx openclaudia install --all          Install all skills
    npx openclaudia install <skill-name>   Install a specific skill
    npx openclaudia list                   List available skills
    npx openclaudia remove <skill-name>    Remove a skill
    npx openclaudia remove --all           Remove all OpenClaudia skills

  Examples:
    npx openclaudia install --all
    npx openclaudia install seo-audit
    npx openclaudia install write-blog keyword-research
    npx openclaudia list

  Website: https://openclaudia.com
  GitHub:  https://github.com/OpenClaudia/openclaudia-skills
`);
}

function cloneRepo() {
  const tmpDir = join(tmpdir(), `openclaudia-${Date.now()}`);
  console.log("Fetching skills from GitHub...");
  execSync(`git clone --depth 1 ${REPO} ${tmpDir}`, { stdio: "pipe" });
  return tmpDir;
}

function getAvailableSkills(repoDir) {
  const skillsDir = join(repoDir, "skills");
  return readdirSync(skillsDir).filter((f) => {
    return existsSync(join(skillsDir, f, "SKILL.md"));
  });
}

function getSkillDescription(repoDir, skillName) {
  const skillFile = join(repoDir, "skills", skillName, "SKILL.md");
  try {
    const content = readFileSync(skillFile, "utf-8");
    const match = content.match(/^---\s*\n([\s\S]*?)\n---/);
    if (match) {
      const descMatch = match[1].match(/^description:\s*(.+)$/m);
      if (descMatch) return descMatch[1].trim().replace(/^["']|["']$/g, "");
    }
  } catch {}
  return "";
}

function installSkillsFromDir(repoDir, skillNames) {
  const repoSkillsDir = join(repoDir, "skills");
  const available = getAvailableSkills(repoDir);

  if (!existsSync(SKILLS_DIR)) {
    mkdirSync(SKILLS_DIR, { recursive: true });
  }

  let installed = 0;
  for (const name of skillNames) {
    if (!available.includes(name)) {
      console.log(`  ! Skill "${name}" not found. Skipping.`);
      continue;
    }
    const src = join(repoSkillsDir, name);
    const dest = join(SKILLS_DIR, name);
    if (existsSync(dest)) {
      console.log(`  ~ ${name} (updated)`);
    } else {
      console.log(`  + ${name}`);
    }
    cpSync(src, dest, { recursive: true });
    installed++;
  }

  return installed;
}

if (!command || command === "help" || command === "--help" || command === "-h") {
  printHelp();
  process.exit(0);
}

if (command === "list") {
  const tmpDir = cloneRepo();
  const skills = getAvailableSkills(tmpDir);
  console.log(`\n  ${skills.length} available skills:\n`);
  for (const s of skills.sort()) {
    const installed = existsSync(join(SKILLS_DIR, s));
    const desc = getSkillDescription(tmpDir, s);
    const status = installed ? "[installed]" : "          ";
    const descStr = desc ? `  ${desc}` : "";
    console.log(`  ${status} ${s.padEnd(24)}${descStr}`);
  }
  console.log();
  rmSync(tmpDir, { recursive: true, force: true });
  process.exit(0);
}

if (command === "install") {
  const targets = args.slice(1);

  if (targets.length === 0) {
    console.log("Usage: npx openclaudia install --all | <skill-name> ...");
    process.exit(1);
  }

  const tmpDir = cloneRepo();

  if (targets.includes("--all")) {
    const all = getAvailableSkills(tmpDir);
    console.log(`\nInstalling all ${all.length} skills to ${SKILLS_DIR}...\n`);
    const count = installSkillsFromDir(tmpDir, all);
    console.log(`\nDone! ${count} skills installed.`);
    console.log(`Skills directory: ${SKILLS_DIR}`);
    console.log(`\nRun "claude" and try /write-blog or /seo-audit to get started.\n`);
  } else {
    console.log(`\nInstalling ${targets.length} skill(s) to ${SKILLS_DIR}...\n`);
    const count = installSkillsFromDir(tmpDir, targets);
    console.log(`\nDone! ${count} skill(s) installed.\n`);
  }

  rmSync(tmpDir, { recursive: true, force: true });
  process.exit(0);
}

if (command === "remove") {
  const targets = args.slice(1);

  if (targets.length === 0) {
    console.log("Usage: npx openclaudia remove --all | <skill-name> ...");
    process.exit(1);
  }

  if (targets.includes("--all")) {
    const tmpDir = cloneRepo();
    const all = getAvailableSkills(tmpDir);
    rmSync(tmpDir, { recursive: true, force: true });
    let removed = 0;
    for (const name of all) {
      const dest = join(SKILLS_DIR, name);
      if (existsSync(dest)) {
        rmSync(dest, { recursive: true, force: true });
        console.log(`  - ${name}`);
        removed++;
      }
    }
    console.log(`\nRemoved ${removed} skill(s).\n`);
  } else {
    for (const name of targets) {
      const dest = join(SKILLS_DIR, name);
      if (existsSync(dest)) {
        rmSync(dest, { recursive: true, force: true });
        console.log(`  - ${name}`);
      } else {
        console.log(`  ! ${name} not installed. Skipping.`);
      }
    }
  }
  process.exit(0);
}

console.log(`Unknown command: ${command}`);
printHelp();
process.exit(1);
