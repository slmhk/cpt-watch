# CPT Policy Watch — setup instructions for the session that owns the slmhk/cpt-watch repository

Read this whole file first, then do every step without asking the owner anything. Work on branch **main** (not a claude/* branch): the site is served from main.

## What this is
A tracker of how US universities are responding to the August 2026 SEVP guidance on Curricular Practical Training (CPT). It has run since 4 Sept as a scheduled Claude task that kept its state in Cowork memory and published to a claude.ai artifact; both of those need the owner's tap for every update, so the tracker is moving here. From now on the repository IS the tracker: `data/snapshot.json` (all state), `state/sources.md` (how to research), `state/log.md` (run log), `cpt-watch.template.html` + `tools/bake.py` (build `index.html`), `prompts/research.md` (the prompt the scheduled task runs). The page is served by GitHub Pages at https://slmhk.github.io/cpt-watch/.

## Steps
1. Unpack the attached kit into the repository root so the layout is exactly: `HANDOVER.md`, `index.html`, `.nojekyll`, `cpt-watch.template.html`, `data/snapshot.json`, `data/history/*.json`, `state/sources.md`, `state/log.md`, `tools/bake.py`, `prompts/research.md`. Keep the existing README.md (append one line pointing to the page URL).
2. Run `python3 tools/bake.py` from the repository root; it must print `OK: baked index.html …`.
3. Commit everything and push to **main**: `git add -A && git -c user.name="CPT Policy Watch" -c user.email="slmhk@users.noreply.github.com" commit -m "Move CPT Policy Watch into the repository" && git push origin HEAD:main`. If you are on a claude/* branch, push to main anyway (`git push origin HEAD:main`); do not open a pull request.
4. Verify the site: wait 90 seconds, then `curl -s -o /dev/null -w "%{http_code}" https://slmhk.github.io/cpt-watch/` should be 200 and the body should contain "CPT Policy Watch". If it is 404 after 5 minutes, GitHub Pages is not enabled — try enabling it via the GitHub tool/API (source: branch main, path /); if that is not possible, tell the owner to open the repository on github.com → Settings → Pages → "Deploy from a branch" → main, / (root) → Save, and re-check.
5. Create the scheduled task with the scheduled-task tool available in this session (create_trigger): name `CPT Policy Watch (4x daily)`, cron `0 0,6,12,18 * * *` (UTC = 08:00/14:00/20:00/02:00 Hong Kong), prompt = the full contents of `prompts/research.md` verbatim, model claude-sonnet-5 if the tool accepts a model (otherwise leave the default), push notifications on, automatic approval if offered. The task must run with this repository attached (it inherits this session's environment); it uses only web search/fetch, file edits, python and git push.
6. Fire the task once now (fire_trigger) to test it end to end. Wait for it to finish (10–25 minutes; poll with list_triggers or by watching `git log origin/main`). Success = a new commit on main whose message starts with "Run", `data/snapshot.json` carrying a new updatedAt, and the live page showing "Last updated" within the last hour (Hong Kong time is displayed).
7. If the test run failed, read its output, fix the cause (usually a path or a git detail), push the fix, and fire it once more. Do not loop more than three times — report what is wrong instead.
8. Report to the owner in a few plain sentences, Hong Kong time only: the page URL, that the schedule is in place, and the test run's verdict. Then tell him that the OLD tasks can be retired: the Cowork task "CPT/SEVP Policy Check (4x daily)" and the in-session "CPT dashboard sync" reminders in his other conversation — he should ask that conversation to delete them.

## Rules that must survive
- Never use an Artifact tool or memory tool from the scheduled task; never ask for approval; never mention individual people or visa status in any file.
- Claremont McKenna is checked every run and stays last in the "clear" tier with a "checked every run" note; the words "highest priority" are banned.
- Verification standard: a school's own page or its student newspaper; aggregators are pointers only.
- All times shown to the owner are Hong Kong time; UTC stays internal (JSON, log headings, commit messages).
