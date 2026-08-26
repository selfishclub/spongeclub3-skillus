import fs from "node:fs";
import os from "node:os";
import path from "node:path";

export function makeTempDir() {
  return fs.mkdtempSync(path.join(os.tmpdir(), "story-skills-"));
}

export function memoryIo(cwd) {
  const out = [];
  const err = [];
  return {
    cwd,
    stdout: {
      write(value) {
        out.push(String(value));
      }
    },
    stderr: {
      write(value) {
        err.push(String(value));
      }
    },
    output() {
      return out.join("");
    },
    error() {
      return err.join("");
    }
  };
}

export function writeMarkdown(filePath, frontmatter, body = "") {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, `---\n${frontmatter.trim()}\n---\n${body}`, "utf8");
}
