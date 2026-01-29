<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/images/logo-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="docs/images/logo-light.png">
    <img src="docs/images/logo-light.png" alt="Cosmux" height="80">
  </picture>
</p>

<p align="center">
  <strong>AI coding assistant that lives in your dev environment</strong><br>
  Powered by Claude. Reads, writes, and edits your code while you work.
</p>

<p align="center">
  <img src="docs/images/cosmux-workflow.gif" alt="Cosmux Workflow" width="100%">
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> •
  <a href="#features">Features</a> •
  <a href="#configuration">Configuration</a> •
  <a href="#how-it-works">How It Works</a>
</p>

---

## Quick Start

```bash
npm install -D cosmux
```

```typescript
// vite.config.ts
import { cosmux } from 'cosmux/vite'

export default defineConfig({
  plugins: [cosmux()]
})
```

```bash
# .env
ANTHROPIC_API_KEY=sk-ant-api03-...
```

Run `npm run dev` — the widget appears in the bottom-right corner.

---

## Features

| | Feature | Description |
|---|---------|-------------|
| 💬 | **Chat Interface** | Natural conversation with streaming responses |
| 🧠 | **Extended Thinking** | Watch the AI reason through complex problems |
| 📁 | **File Operations** | Read, Write, Edit files in your project |
| 💻 | **Terminal Access** | Run shell commands via Bash tool |
| 🔍 | **Code Search** | Glob and Grep tools for finding code |
| 💾 | **Session Persistence** | Chat history saved locally |
| 📖 | **Context-Aware** | Reads `CLAUDE.md` for project understanding |

---

## Vite Setup

Works with React, Vue, Svelte, and other Vite-based projects.

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { cosmux } from 'cosmux/vite'

export default defineConfig({
  plugins: [
    react(),
    cosmux()
  ]
})
```

The plugin automatically starts the Cosmux server and injects the widget.

---

## Next.js Setup

```javascript
// next.config.mjs
import { withCosmux } from 'cosmux/next'

export default withCosmux({
  // your existing Next.js config
})
```

For App Router, create a widget component:

```tsx
// components/CosmuxWidget.tsx
'use client'

import { useEffect } from 'react'

export function CosmuxWidget({ port = 3333 }: { port?: number }) {
  useEffect(() => {
    if (process.env.NODE_ENV !== 'development') return

    ;(window as any).__COSMUX_CONFIG__ = { serverUrl: `http://localhost:${port}` }

    const script = document.createElement('script')
    script.src = `http://localhost:${port}/static/inject.js`
    script.async = true
    document.body.appendChild(script)

    return () => { script.remove() }
  }, [port])

  return null
}
```

```tsx
// app/layout.tsx
import { CosmuxWidget } from '@/components/CosmuxWidget'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <CosmuxWidget />
      </body>
    </html>
  )
}
```

---

## Configuration

### Plugin Options

```typescript
cosmux({
  port: 3333,           // Server port (default: 3333)
  autoStart: true,      // Auto-start server (default: true)
  injectWidget: true,   // Inject widget script (default: true)
  workspace: './',      // Workspace path (default: cwd)
})
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key | Required |
| `COSMUX_PORT` | Server port | `3333` |
| `COSMUX_MODEL` | Claude model | `claude-opus-4-5-20251101` |

### Project Context

Create a `CLAUDE.md` file in your project root to give the AI context:

```markdown
# My Project

## Tech Stack
- React 18 + TypeScript
- Tailwind CSS

## Code Style
- Use functional components
- Prefer named exports
```

---

## CLI

Run Cosmux standalone:

```bash
npx cosmux serve                        # Start server
npx cosmux serve --port 4000            # Custom port
npx cosmux serve --workspace ./project  # Specific workspace
```

---

## Manual Integration

For projects without Vite or Next.js:

```html
<script>
  window.__COSMUX_CONFIG__ = { serverUrl: 'http://localhost:3333' };
</script>
<script src="http://localhost:3333/static/inject.js"></script>
```

```bash
npx cosmux serve
```

---

## How It Works

1. **Install** — Downloads a platform-specific binary
2. **Configure** — Plugin starts the server automatically
3. **Develop** — Widget injects into your dev HTML
4. **Code** — AI reads and modifies files in your workspace

All file operations happen locally. Your code is only sent to Claude's API for processing.

---

## Troubleshooting

<details>
<summary><strong>Widget doesn't appear?</strong></summary>

- Check that the server is running (look for "Cosmux server ready" in terminal)
- Verify your API key is set in `.env`
- Try opening `http://localhost:3333/widget` directly
</details>

<details>
<summary><strong>Server won't start?</strong></summary>

- Check if port 3333 is in use: `lsof -i :3333`
- Try a different port: `cosmux({ port: 4000 })`
</details>

<details>
<summary><strong>Binary download failed?</strong></summary>

- Install via pip as fallback: `pip install cosmux`
</details>

---

## Requirements

- Node.js 18+
- Anthropic API key — [console.anthropic.com](https://console.anthropic.com)

---

## License

MIT — see [LICENSE](LICENSE)

---

<p align="center">
  <a href="./CONTRIBUTING.md">Contributing</a> •
  <a href="https://github.com/cosmux-dev/cosmux/issues">Issues</a>
</p>
