# Setup Wizard Design Options

## Option A: Card-Based Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   ╭──────────────────────────────────────────────────────────────╮  │
│   │  ▄█─●─●─█▄  █ ▄▀ █▀▀█ █   █   █▀▀█ █▀▀▄ █▀▀█ █▀▀█            │  │
│   │  ●──███──●  █▀▄  █  █ █   █   █▄▄█ █▀▀▄ █  █ █▄▄▀            │  │
│   │  ▀█─●─●─█▀  █  █ █▄▄█ █▄▄ █▄▄ █  █ █▄▄▀ █▄▄█ █ █▄            │  │
│   ╰──────────────────────────────────────────────────────────────╯  │
│                                                                     │
│   ┌─ Connection ─────────────────────────────────────────────────┐  │
│   │                                                              │  │
│   │  Endpoint    http://localhost:1234                           │  │
│   │              ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔                  │  │
│   │              KOLLABOR_MY_LLM_ENDPOINT                        │  │
│   │                                                              │  │
│   └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│   ┌─ Model ──────────────────────────────────────────────────────┐  │
│   │                                                              │  │
│   │  Model       qwen3-4b                                        │  │
│   │              ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔                  │  │
│   │                                                              │  │
│   │  Format      ◉ openai    ○ anthropic                         │  │
│   │                                                              │  │
│   └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│                    [ Back ]         [ Continue → ]                  │
│                                                                     │
│   ━━━━━━━━━━━━━━━━━━━━━━━━●━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│   1. Welcome    2. Connect    3. Auth    4. Features    5. Done     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Option B: Minimalist Single-Column

```
                    ╭─────────────────────────────────╮
                    │         K O L L A B O R         │
                    │          Setup Wizard           │
                    ╰─────────────────────────────────╯


                         ┌─────────────────────────┐
                         │                         │
           Endpoint      │  http://localhost:1234  │
                         │                         │
                         └─────────────────────────┘
                         env: KOLLABOR_*_ENDPOINT


                         ┌─────────────────────────┐
                         │                         │
           Model         │  qwen3-4b               │
                         │                         │
                         └─────────────────────────┘


           Format        ▸ openai ◂    anthropic



                              ● ○ ○ ○ ○

                         ↑↓ navigate   → continue
```

---

## Option C: Two-Column Split

```
╔══════════════════════════════════╦══════════════════════════════════╗
║                                  ║                                  ║
║   ┌────────────────────────────┐ ║   CONNECTION                     ║
║   │                            │ ║   ══════════                     ║
║   │   K O L L A B O R          │ ║                                  ║
║   │                            │ ║   Endpoint                       ║
║   │   Setup Wizard             │ ║   ┌──────────────────────────┐   ║
║   │                            │ ║   │ http://localhost:1234_   │   ║
║   └────────────────────────────┘ ║   └──────────────────────────┘   ║
║                                  ║   ↳ KOLLABOR_MY_LLM_ENDPOINT     ║
║                                  ║                                  ║
║   STEPS                          ║   Model                          ║
║   ─────                          ║   ┌──────────────────────────┐   ║
║                                  ║   │ qwen3-4b                 │   ║
║   ● Connect   ← you are here     ║   └──────────────────────────┘   ║
║   ○ Auth                         ║                                  ║
║   ○ Profile                      ║   Format                         ║
║   ○ Done                         ║   [ openai ▾ ]                   ║
║                                  ║                                  ║
║                                  ║                                  ║
║   Press Q to skip                ║   ──────────────────────────────  ║
║                                  ║   Tab: next   Enter: continue    ║
║                                  ║                                  ║
╚══════════════════════════════════╩══════════════════════════════════╝
```

---

## Option D: Wizard Steps with Progress Bar

```
  ══════════════════════════════════════════════════════════════════════

      STEP 2 OF 5                                    ░░░░░████░░░░░░ 40%

  ══════════════════════════════════════════════════════════════════════


                              CONNECTION SETUP

      Connect to your LLM provider. We'll use environment variables
      for sensitive data like API tokens.


      ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
      ┃                                                               ┃
      ┃   ENDPOINT *                                                  ┃
      ┃   ┌─────────────────────────────────────────────────────────┐ ┃
      ┃   │ http://localhost:1234                                   │ ┃
      ┃   └─────────────────────────────────────────────────────────┘ ┃
      ┃   Will also check: $KOLLABOR_MY_LLM_ENDPOINT                  ┃
      ┃                                                               ┃
      ┃   MODEL *                                                     ┃
      ┃   ┌─────────────────────────────────────────────────────────┐ ┃
      ┃   │ qwen3-4b                                                │ ┃
      ┃   └─────────────────────────────────────────────────────────┘ ┃
      ┃                                                               ┃
      ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛


                        ◀ BACK                    NEXT ▶

  ══════════════════════════════════════════════════════════════════════
```

---

## Option E: Floating Modal Style

```


              ╭────────────────────────────────────────────────╮
              │                                                │
              │   ● ● ●   LLM Configuration                    │
              │  ─────────────────────────────────────────────  │
              │                                                │
              │   Provider                                     │
              │   ┌────────────────────────────────────────┐   │
              │   │  Local LLM (localhost:1234)        ▾   │   │
              │   └────────────────────────────────────────┘   │
              │                                                │
              │   Model                                        │
              │   ┌────────────────────────────────────────┐   │
              │   │  qwen3-4b                              │   │
              │   └────────────────────────────────────────┘   │
              │                                                │
              │   Token                                        │
              │   ┌────────────────────────────────────────┐   │
              │   │  ●●●●●●●●●●●●  (from env)              │   │
              │   └────────────────────────────────────────┘   │
              │   ✓ KOLLABOR_MY_LLM_TOKEN is set               │
              │                                                │
              │  ─────────────────────────────────────────────  │
              │                                                │
              │              [ Cancel ]    [ Save & Start ]    │
              │                                                │
              ╰────────────────────────────────────────────────╯


```

---

## Option F: Terminal-Native with ASCII Art

```

╭──────────────────────────────────────────────────╮
│ ▄█─●─●─█▄  █ ▄▀ █▀▀█ █   █   █▀▀█ █▀▀▄ █▀▀█ █▀▀█ │
│ ●──███──●  █▀▄  █  █ █   █   █▄▄█ █▀▀▄ █  █ █▄▄▀ │
│ ▀█─●─●─█▀  █  █ █▄▄█ █▄▄ █▄▄ █  █ █▄▄▀ █▄▄█ █ █▄ │
╰──────────────────────────────────────────────────╯
    >> Welcome to Kollabor!
    // SETUP LLM CONNECTION
    profile:  local
    endpoint: http://localhost:1234_
    model:    qwen3-4b
    token:    sk-...ds
    temp:     0.7
    format:   [x] openai  [ ] anthropic

    STATUS: [!] Token not set - export KOLLABOR_MY_LLM_TOKEN=...
    ─────────────────────────────────────────────────────────────────

    // Keyboard Shortcuts
    Esc        Cancel / close modals
    Enter      Submit / confirm
    Up / Down  Navigate prompt history
    Ctrl+C     Exit application
  
    // Slash commands
    /help - Show all available commands
    /profile - Manage LLM API profiles
    /terminal - Tmux session management
    /save - Save conversation to file
    /resume - Resume conversations
 
```

---

## Option G: Compact Inline

```
╭─ KOLLABOR SETUP ─────────────────────────────────────────────────────╮
│                                                                      │
│  [2/5] CONNECTION                                                    │
│  ════════════════                                                    │
│                                                                      │
│  endpoint   │░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│ http://localhost:1234 │
│  model      │░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│ qwen3-4b              │
│  format     │ openai ◀━━━━━▶ anthropic       │                       │
│  profile    │░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│ my-llm                │
│                                                                      │
│  ┌─ STATUS ───────────────────────────────────────────────────────┐  │
│  │ ✓ endpoint    ✓ model    ✗ token (set KOLLABOR_MY_LLM_TOKEN)   │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                      │
│                           ◀ Back    Next ▶                           │
│                                                                      │
╰──────────────────────────────────────────────────────────────────────╯
```

---

## Option H: Gradient Banner + Clean Form

```

        ░▒▓█ K O L L A B O R █▓▒░

        ─────────────────────────────────────────────────────
                         CONNECTION SETUP
        ─────────────────────────────────────────────────────


        ┌─────────────────────────────────────────────────────┐
        │ ENDPOINT                                            │
        │                                                     │
        │  > http://localhost:1234_                           │
        │                                                     │
        │  env: KOLLABOR_MY_LLM_ENDPOINT                      │
        └─────────────────────────────────────────────────────┘

        ┌─────────────────────────────────────────────────────┐
        │ MODEL                                               │
        │                                                     │
        │  > qwen3-4b                                         │
        │                                                     │
        └─────────────────────────────────────────────────────┘

        FORMAT:  ● openai    ○ anthropic


        ═══════════════════════════════════════════════════════
        ◀ ─ ─ ─ ─ ─ ─ ● ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ▶
                    step 2 of 5
        ═══════════════════════════════════════════════════════

```

---

## Features to Consider

1. **Animated transitions** between steps (slide/fade)
2. **Live validation** with checkmarks/X marks
3. **Auto-detect providers** (show preset buttons for OpenAI, Anthropic, Local)
4. **Keyboard hints** that fade in/out
5. **Color theming** matching main app gradient
6. **Responsive** - adapts to terminal width AND height
7. **Progress indicators** (dots, bar, steps, percentage)

Which style appeals to you? I can implement any of these.
