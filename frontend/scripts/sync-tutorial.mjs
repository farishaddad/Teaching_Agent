#!/usr/bin/env node
/**
 * Sync tutorial content into the frontend's public assets.
 *
 * The canonical tutorial markdown lives in `<repo>/tutorial/` (this is what the
 * backend serves and what you should EDIT). The React SPA renders the copies in
 * `frontend/public/tutorial/`. To avoid the two drifting apart, this script
 * copies every `.md` from the canonical directory into `public/tutorial/` and
 * removes any stale files that no longer exist in the source.
 *
 * It runs automatically before `npm run build` and `npm run dev` (see the
 * prebuild/predev scripts in package.json), so `frontend/public/tutorial/` is
 * always regenerated from `tutorial/` — never edit the public copy by hand.
 */

import { readdirSync, mkdirSync, copyFileSync, rmSync, existsSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(__dirname, '..', '..');
const srcDir = join(repoRoot, 'tutorial');
const destDir = join(repoRoot, 'frontend', 'public', 'tutorial');

if (!existsSync(srcDir)) {
  console.error(`[sync-tutorial] source directory not found: ${srcDir}`);
  process.exit(1);
}

mkdirSync(destDir, { recursive: true });

const isMd = (f) => f.toLowerCase().endsWith('.md');
const srcFiles = readdirSync(srcDir).filter(isMd);
const destFiles = existsSync(destDir) ? readdirSync(destDir).filter(isMd) : [];

// Remove stale .md files that no longer exist in the canonical source.
for (const f of destFiles) {
  if (!srcFiles.includes(f)) {
    rmSync(join(destDir, f));
    console.log(`[sync-tutorial] removed stale ${f}`);
  }
}

// Copy every canonical .md into public/.
for (const f of srcFiles) {
  copyFileSync(join(srcDir, f), join(destDir, f));
}

console.log(`[sync-tutorial] synced ${srcFiles.length} chapter file(s) → frontend/public/tutorial/`);
