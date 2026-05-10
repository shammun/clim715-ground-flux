# Claude Code setup guide for the CLIM-715 project

## What you have already

Looking at your folder, you have a `.claude/` directory, which means Claude Code has been initialized here at least once. You're partway there. The two missing pieces are: (a) Claude Code installed and authenticated on your desktop if it isn't already, and (b) a `CLAUDE.md` file at the project root that tells Claude Code what your project is and how to work on it.

The `CLAUDE.md` and `.gitignore` are now created in this folder. The rest of this guide walks you through everything else.

---

## 1. Install Claude Code (if you haven't already)

You're on Windows. The simplest path is the **native installer** — no Node.js, no WSL, no terminal complications. Open PowerShell (search "PowerShell" in the Start menu, right-click, "Run as Administrator" is *not* needed) and run:

```powershell
irm https://claude.ai/install.ps1 | iex
```

That single line downloads and installs the Claude Code binary. Verify it worked:

```powershell
claude --version
```

You should see a version number. If you get "command not found", close PowerShell completely and open a new window — the installer adds Claude Code to your PATH but the new PATH only takes effect in new terminal sessions.

If you prefer a graphical interface and don't want to use the terminal at all, there's a separate option: install the **Claude Desktop app** (from claude.ai) and use its **Cowork** feature, which gives you Claude Code's capabilities through a chat-style UI. For your workflow — iterating on HTML visualizations and editing reports — either works. The terminal version is more responsive once you're used to it; Cowork is easier on day one.

## 2. Authentication

Claude Code requires a **Pro, Max, Team, Enterprise, or Console account**. The free Claude.ai plan does not include Claude Code access. Since you have access via the Claude web interface where you've been talking to me, you likely already have a Pro or Max plan — that same login works.

To authenticate, just run:

```powershell
claude
```

…in your project folder. The first time, it opens a browser window for you to log in. After that, you're done — no API key juggling.

## 3. Open Claude Code in your project folder

Open PowerShell, then `cd` to the folder containing your CLIM-715 files:

```powershell
cd "$env:USERPROFILE\Documents\CLIM715"
```

(Adjust the path to wherever your folder actually is. From your screenshot, the folder contains the `.claude` directory, the report Word docs, the notebook, `run_experiments.py`, and the HTML files.)

Then start a Claude Code session:

```powershell
claude
```

Claude Code automatically reads `CLAUDE.md` from the current directory at the start of every session. That file (which I just created) gives Claude Code the full project context — what the project is, what each file does, your style preferences, and the rules to follow when modifying things.

## 4. The most useful things to do in your first session

Once Claude Code is running, try these in order. They take 2 minutes each and give you a feel for what works.

**(a) Verify Claude Code can see the project.** Type:
```
What's in CLAUDE.md? Briefly summarize the project rules.
```
This confirms it found and read the context file. If it says "I don't see a CLAUDE.md", you opened Claude Code in the wrong folder.

**(b) Open one of the existing HTML visualizations.** Type:
```
Read window_delta_t.html and tell me what it does and how the slider works.
```
Claude Code will read the file and explain it back to you. This verifies file access works and gives you confidence that Claude Code understands what's there.

**(c) Make a small edit.** Type something like:
```
In window_delta_t.html, change the header subtitle text to say "..." instead of "...".
```
Claude Code shows you the diff before applying it, you approve, and the file is changed. Reload the file in Chrome to see the result.

## 5. The workflow that actually works for presentation iteration

Here is the loop I'd recommend, based on how the visualizations were built so far:

1. **Open Chrome** with the HTML file you're iterating on. Press F12 to open DevTools (helpful for inspecting layout issues).
2. **In one PowerShell window, have Claude Code running.**
3. **Make a request** in plain English: "make the slider thumb bigger" or "the lower-left panel is too tall, compress it." Claude Code shows the diff, applies it.
4. **Hard-refresh Chrome** with `Ctrl+Shift+R`. The browser caches HTML aggressively, and a normal F5 sometimes doesn't pick up edits. `Ctrl+Shift+R` always works.
5. **Iterate.**

This cycle takes 10–30 seconds per change. The key is the hard-refresh — without it, you'll think Claude Code's edit didn't work when actually it did, and you'll waste time.

## 6. Practices that will save you time

**Keep CLAUDE.md updated.** Every time a rule emerges that you don't want to repeat ("don't use emojis in slides", "always test sliders with jsdom", "the substrate colour is X not Y"), add it to CLAUDE.md. Claude Code re-reads this file each session, so a rule you write down once stays enforced forever.

**Use specific filenames in requests.** "Update the visualization" is ambiguous when you have three. "Update `window_delta_t.html`" is unambiguous and saves a clarification round-trip.

**Ask Claude Code to verify before declaring done.** For interactive HTML, "verify the slider works using jsdom before saying it's complete" forces Claude Code to actually test rather than assume. This caught silent rendering failures in our earlier sessions.

**For numerical changes, ask Claude Code to cross-check against the report.** Example: "Re-generate the Δt sweep data and verify the asphalt BTCS Δt=600s RMSE is within 0.05 K of the report's 2.10 K." This catches data regressions early.

**Use plan mode for big changes.** When you ask Claude Code to do something multi-step, ask it to **plan first, then execute**. Type something like: "Plan the changes you'd make to convert the report from short to long form. Don't make changes yet." Review the plan, then say "go ahead." This prevents Claude Code from doing 10 things when you only wanted 3.

**Commit checkpoints with git.** Before any large refactor, run `git init` once in the folder, then `git add . && git commit -m "checkpoint"` before each big change. If Claude Code does something you don't like, `git reset --hard` rolls everything back. Without git, "undo" is harder.

## 7. Things to avoid

- **Don't try to use Claude Code to generate the Word documents directly.** Word documents work better through the python-docx workflow we've been using — Claude Code can generate Python that builds the docx, but the docx itself isn't text-editable in a useful way from the terminal.
- **Don't paste 500 lines of code into Claude Code's chat input.** It's faster and cleaner to say "look at lines 200–300 of CLIM715_Substrate_3D_Visualization_clean_ed.html and …".
- **Don't use Claude Code to install random packages globally.** Stick to project-local virtual environments (`python -m venv venv` then `pip install -r requirements.txt`). Claude Code respects this if you ask it to.
- **Don't run `claude` in your home directory.** Always `cd` to the project folder first. Claude Code's most useful behaviour comes from having a focused, scoped working directory.

## 8. Specific commands you'll use a lot

Inside a Claude Code session:

| Command | What it does |
|---|---|
| `/help` | Show all available commands |
| `/clear` | Start fresh conversation (Claude Code forgets recent context but keeps CLAUDE.md) |
| `/compact` | Summarize the current conversation to save context space |
| `/quit` | Exit |
| `/doctor` | Diagnose installation issues if something feels broken |

In PowerShell, outside Claude Code:

| Command | Purpose |
|---|---|
| `claude --version` | Verify install |
| `claude doctor` | Health check |
| `claude` | Start a session in the current directory |

## 9. What I'd do first when you sit down

Concretely, in this order:

1. Open PowerShell, `cd` to the CLIM-715 folder.
2. Run `git init && git add . && git commit -m "initial state before Claude Code work"` — gives you an undo button.
3. Run `claude`. Authenticate if it's the first time.
4. Type: `Read CLAUDE.md and the long report. List 3 things you'd improve about the presentation visualizations.` — gives you ideas without committing to anything.
5. Pick one of the suggestions, say "do that one." Hard-refresh Chrome to view.
6. Repeat.

You'll have a meaningful improvement applied within five minutes of the first session.

## 10. When something goes wrong

- **"Command not found: claude"** → close and reopen PowerShell.
- **"Authentication failed"** → run `claude` again, the OAuth popup may have been blocked.
- **Claude Code edits a file but Chrome doesn't show the change** → hard-refresh with Ctrl+Shift+R.
- **Claude Code seems confused or repeats itself** → run `/clear` to reset context, or `/compact` to summarize.
- **A change broke something and you don't know what** → `git diff` to see what changed, `git reset --hard HEAD` to roll back. (Yet another reason to commit checkpoints.)
- **Slider appears not to do anything** → it's almost always browser cache. Hard-refresh. If still broken, ask Claude Code to verify with jsdom.

---

Total time to set up from a fresh Windows machine: about 10 minutes. The biggest payoff after that is the `CLAUDE.md` file — it's the difference between Claude Code as a fast typing assistant and Claude Code as a project collaborator that knows the rules.
