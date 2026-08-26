import { describe, expect, test } from "bun:test";
import { chapterProse, extractSection, kebabCase, titleCaseSlug, wordCount } from "../src/markdown.js";

describe("markdown utilities", () => {
  test("normalizes labels and counts prose words", () => {
    expect(kebabCase(" Sera's Last Ember! ")).toBe("seras-last-ember");
    expect(titleCaseSlug("seras-last-ember")).toBe("Seras Last Ember");
    expect(wordCount("# Title\n\nSera's [lost heir](x.md) `code` **returns**.")).toBe(3);
  });

  test("extracts chapter prose from template, outline, and natural formats", () => {
    expect(chapterProse("# Chapter\n\n## Chapter Text\n\nActual prose.").trim()).toBe("Actual prose.");
    expect(chapterProse("# Chapter\n\n## Outline\n\n1. Beat\n\n---\n\nActual prose.").trim()).toBe("Actual prose.");
    expect(chapterProse("# Chapter\n\n## Outline\n\n1. Beat").trim()).toBe("1. Beat");
    expect(chapterProse("# Chapter\n\nNo outline.").trim()).toBe("No outline.");
    expect(chapterProse("No leading heading.").trim()).toBe("No leading heading.");
  });

  test("extracts named sections", () => {
    const markdown = "# Index\n\n## Registry\n\nRows\n\n## Family Trees\n\nTrees\n\n## Notes\n\nEnd";
    expect(extractSection(markdown, "Family Trees")).toBe("Trees");
    expect(extractSection(markdown, "Missing")).toBe("");
  });
});
