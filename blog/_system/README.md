# Blog system

The blog runs **separately from the portfolio**. The portfolio never loads blog code. If the blog breaks, or is
removed, the portfolio keeps working exactly as before.

## Where things are
| Path | What it is |
|---|---|
| `blog/_src/posts/*.md` | The articles (Markdown). The only files you ever edit by hand |
| `blog/_system/config.yml` | **Settings**: how often, AI models, topics, length |
| `blog/_system/style-guide.md` | The voice and rules the AI follows |
| `blog/_system/build.py` | Turns the Markdown into pages, the listing and `blog/sitemap.xml` |
| `blog/_system/write.py` | The AI writer (Gemini first, Groq as backup) |
| `blog/_system/templates/` | Page templates for posts and the listing |
| `blog/assets/` | Blog-only CSS and JS |
| `blog/<slug>/`, `blog/index.html`, `blog/sitemap.xml` | **Generated.** Don't edit; they're rebuilt automatically |
| `.github/workflows/blog.yml` | Runs daily, and after every change to posts or settings |
| `.github/workflows/blog-remove.yml` | One-click removal |

Folders starting with `_` are not published by GitHub Pages, so the sources and system files are never public pages.
The only blog code in the portfolio is the Blog link in `index.html`, between `BLOG-LINK` markers.

## One-time setup
1. **Gemini key:** go to https://aistudio.google.com/, then **Get API key**, then create a key (free, no card).
2. **Groq key:** go to https://console.groq.com/, then **API Keys**, then create a key (free).
3. In GitHub, open the repo and go to **Settings → Secrets and variables → Actions → New repository secret**. Add:
   - `GEMINI_API_KEY`
   - `GROQ_API_KEY`
4. Required (new posts arrive as pull requests): go to **Settings → Actions → General → Workflow permissions**. Tick
   **Allow GitHub Actions to create and approve pull requests**, then save.
5. Optional: in Google Search Console, submit `https://salmanalirafeeq.github.io/portfolio/blog/sitemap.xml`.

Until the keys exist, the daily run only rebuilds pages and skips writing. Nothing fails.

## How it runs
Every day at 04:37 Pakistan time:
1. **Publish due posts:** a post goes live when `draft: false` and its `date` has arrived. Future dates wait.
2. **Write a new post if due:** a new post is due when the newest post is at least `every_days` old.
   - The AI picks a new topic, never repeating one, and balances categories.
   - It writes the article and runs strict checks:
     - no invented statistics or studies
     - no client names
     - only safe links
     - correct length, FAQ section and SEO fields
   - A failed check gets one rewrite. If a model still fails, the next model or provider is tried.
3. **You approve every new post:** a pull request is opened, assigned to you, and GitHub emails it to you with the full article. Nothing the AI writes goes live without this step.
   - **Merge** to publish (live about 2 minutes later).
   - **Close** to discard.
   - No new draft is written while one is waiting.

If every provider fails, the run is marked failed and GitHub emails you. The site is not touched.

## Everyday controls
| I want to… | Do this |
|---|---|
| Pause the AI | `config.yml` → `enabled: false` |
| Change how often | `config.yml` → `every_days` |
| Get a post right now | Actions → **Blog** → Run workflow → "write a post now" |
| Write a post myself | Add `blog/_src/posts/<slug>.md` (copy an existing one's header), push |
| Schedule a post | Give it a future `date`; it publishes on that day |
| Fix a typo | Edit the `.md` file and push. Pages, listing and sitemap update |
| Unpublish a post | Set `draft: true`, or delete the `.md` file |
| Preview locally | `pip install -r blog/_system/requirements.txt`, then `python blog/_system/build.py` |

## Remove the blog completely
GitHub, then **Actions → "Blog: remove completely" → Run workflow**, tick the box, then **Run**.

It deletes the `blog/` folder and the Blog link from the home page nav, and switches off both blog workflows.
The portfolio is otherwise untouched.

To undo, revert the "Remove blog" commit and re-enable the workflows in the Actions tab.

Notes:
- GitHub pauses scheduled workflows in repos with no activity for 60 days. If that happens, Actions shows a button to turn it back on.
- The free AI tiers can change their limits. Models and their order live in `config.yml`.
