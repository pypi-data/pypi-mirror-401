# Setup Wizard Screens Spec

## Screen 1: Welcome

```
╭──────────────────────────────────────────────────╮
│ ▄█─●─●─█▄  █ ▄▀ █▀▀█ █   █   █▀▀█ █▀▀▄ █▀▀█ █▀▀█ │
│ ●──███──●  █▀▄  █  █ █   █   █▄▄█ █▀▀▄ █  █ █▄▄▀ │
│ ▀█─●─●─█▀  █  █ █▄▄█ █▄▄ █▄▄ █  █ █▄▄▀ █▄▄█ █ █▄ │
╰──────────────────────────────────────────────────╯

                    Setup Wizard

  Welcome! This wizard will configure your LLM connection.

            Press ENTER to begin  |  Press Q to skip

         [ *  .  .  .  .  . ]  Enter: begin  |  Q: skip
```

---

## Screen 2: API Configuration

```
              ╭───────────────────────────╮
              │   LLM API Configuration   │
              ╰───────────────────────────╯

         Configure your LLM provider connection

Connection (required)
  Endpoint *  env: KOLLABOR_MY_LLM_ENDPOINT
  [http://localhost:1234_                ]
  (e.g., http://localhost:1234, https://api.anthropic.com)

Model (required)
  Model *  env: KOLLABOR_MY_LLM_MODEL
  [qwen3-4b                              ]
  (e.g., qwen3-4b, gpt-4-turbo, claude-sonnet)

  Tool Format
  [ openai ]  <-/-> to change
  (openai or anthropic)

Advanced (optional)
  Profile Name
  [my-llm                                ]
  (name for this profile, e.g., my-llm, openai)

        Tab: next field  |  Esc: back  |  Enter: continue

  [ .  *  .  .  .  . ]  <-/->: navigate  |  Enter: next  |  Q: skip
```

---

## Screen 3: Authentication & Settings

```
            ╭───────────────────────────────╮
            │   Authentication & Settings   │
            ╰───────────────────────────────╯

Authentication (required)

  API Token *    env: KOLLABOR_MY_LLM_TOKEN
  [(not set)                             ]
  [warn] Set token in your shell:
    export KOLLABOR_MY_LLM_TOKEN='sk-...'

Advanced (optional)

  Temperature
  [0.7_              ]
  (0.0 = deterministic, 2.0 = creative, default: 0.7)

Status:
  [warn] Missing: token

                 Esc: back  |  Enter: continue

  [ .  .  *  .  .  . ]  <-/->: navigate  |  Enter: next  |  Q: skip
```

---

## Screen 4: Keyboard Shortcuts

```
               ╭────────────────────────╮
               │   Keyboard Shortcuts   │
               ╰────────────────────────╯

  Opt+Left / Opt+Right       Cycle through status views
  Esc                        Cancel / close modals
  Enter                      Submit / confirm
  Up / Down                  Navigate history
  /                          Slash command menu
  Ctrl+C                     Exit application

         Pro tip: Type / to see all available commands!

  [ .  .  .  *  .  . ]  <-/->: navigate  |  Enter: next  |  Q: skip
```

---

## Screen 5: Key Features

```
                  ╭──────────────────╮
                  │   Key Features   │
                  ╰──────────────────╯

  /help            Show all available commands
  /profile         Manage LLM API profiles
  /terminal        Tmux session management
  /save            Save conversation to file
  /resume          Resume conversations
  /matrix          Easter egg

  Kollabor uses a plugin architecture - everything is customizable!
  Plugins can add commands, status views, and hook into events.

  [ .  .  .  .  *  . ]  <-/->: navigate  |  Enter: next  |  Q: skip
```

---

## Screen 6: Ready / Summary

```
╭──────────────────────────────────────────────────╮
│ ▄█─●─●─█▄  █ ▄▀ █▀▀█ █   █   █▀▀█ █▀▀▄ █▀▀█ █▀▀█ │
│ ●──███──●  █▀▄  █  █ █   █   █▄▄█ █▀▀▄ █  █ █▄▄▀ │
│ ▀█─●─●─█▀  █  █ █▄▄█ █▄▄ █▄▄ █  █ █▄▄▀ █▄▄█ █ █▄ │
╰──────────────────────────────────────────────────╯

                     Almost Ready!

Configuration Summary:

  Profile:       my-llm
  Endpoint:      [ok] http://localhost:1234
  Model:         [ok] qwen3-4b
  Token:         [--] (not set)

  Token env var: KOLLABOR_MY_LLM_TOKEN

[warn] Missing: token
Profile will be saved but may not work until configured.

                 Enter: save and start

   Run /setup or /profile anytime to change settings

            [ .  .  .  .  .  * ]  Enter: save & start
```

---

## Navigation Summary

| Screen | Esc | Enter | Arrow Keys | Tab |
|--------|-----|-------|------------|-----|
| 1 Welcome | skip | begin | - | - |
| 2 API Config | back to 1 | next | up/down: fields, left/right: dropdown | next field |
| 3 Token | back to 2 | next | left/right: cursor | next field |
| 4 Shortcuts | back | next | left/right: pages | - |
| 5 Features | back | next | left/right: pages | - |
| 6 Ready | back | save & start | left/right: pages | - |

---

## Notes

- Env var names are dynamic based on profile name: `KOLLABOR_{PROFILE}_TOKEN`
- Status shows [ok]/[warn]/[--] indicators
- Form fields show env var hints
- Required fields marked with *
