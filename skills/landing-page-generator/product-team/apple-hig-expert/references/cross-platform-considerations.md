# Cross-Platform Considerations (Apple)

Reference for adapting an app across Apple's platforms. Each platform has
distinct conventions; same-everywhere is usually wrong.

## 1. The Apple platform map

| Platform | Primary input | Screen | Conventions |
|----------|---------------|--------|-------------|
| iOS (iPhone) | Touch | 4-7" portrait | Tab bar; modal sheets; nav stack |
| iPadOS | Touch + Pencil + Keyboard | 8-13" | Sidebar; inspector; multitasking |
| macOS | Mouse / trackpad / keyboard | 13-27" landscape | Menu bar; windows; toolbar |
| watchOS | Touch + crown | < 2" | Single-task; quick glance; complications |
| tvOS | Remote (focus engine) | 40-65" | Focus-driven; minimal text input |
| visionOS | Eye + hands | Spatial | Volumes; windows in 3D; gaze + pinch |

## 2. iPadOS — what changes from iPhone

### Layout
- More screen real estate; use it (don't just stretch iPhone)
- `NavigationSplitView` for sidebar + content
- Inspector for secondary content
- Popover for context menus (instead of action sheets)

### Multitasking
- Split View: app shares screen with one other (50/50, 30/70)
- Slide Over: app slides over another
- Stage Manager: floating, resizable windows
- App must handle dynamic size class changes mid-session

### Hardware
- Apple Pencil: support drawing/handwriting where appropriate
- External keyboard: keyboard shortcuts via `.keyboardShortcut`
- Pointer (trackpad / mouse): hover effects, custom pointer shapes

### Specific patterns
- **Sidebar** for top-level navigation (replaces tab bar at large widths)
- **Inspector** for properties / metadata
- **Popover** anchored to specific UI element
- **Multi-column** layouts (e.g., 3-column sidebar + middle + detail)
- **Drag-and-drop** between apps, across split view

## 3. macOS — what changes

### Window-based
- App may have multiple windows (or none)
- Window state persists across launches
- Multiple instances of same view (multiple documents)
- New Window menu item standard

### Menu bar
- Full menu bar with File / Edit / View / Window / Help
- Don't put critical actions only in toolbar — menu bar is primary
- Keyboard shortcuts visible in menu items

### Toolbar
- Persistent at top of window
- Customizable by user
- Symbols + labels (default) or symbols-only

### Sidebar
- Primary nav for browsable content
- Resizable; user collapses to fit
- Multi-level sometimes (e.g., Music, Notes)

### Mouse + trackpad
- Hover effects
- Right-click / two-finger click for context menus
- Drag-and-drop everywhere
- Trackpad gestures (swipe between pages, smart zoom)

### What translates from iOS
- SwiftUI components mostly work
- Asset Catalog, semantic colors, Dynamic Type, SF Symbols

### What doesn't translate
- Push navigation → use windows / split view
- Tab bar → use toolbar or sidebar
- Bottom sheet → use NSPanel / NSPopover
- Heavy gesture-based interaction → users expect mouse/keyboard

### Mac Catalyst vs native Mac
- Catalyst: bring iPad app to Mac with adjustments
- Native (SwiftUI Mac): designed Mac-first; richer experience
- Pure AppKit: legacy; only for specific needs

## 4. watchOS — design for the glance

### Constraints
- Small screen (38-49mm)
- Brief interactions (2-10 seconds typical)
- Limited input (taps, swipes, crown rotation)
- Battery-conscious

### Surface types
- **App** — full-screen experience
- **Complications** — small data points on watch face
- **Notifications** — long look, short look
- **Smart Stack** — context-driven widget feed (watchOS 10+)
- **Workout extensions** — during workouts
- **Always-On display** — simplified state

### Design principles
- One primary task per screen
- Big tap targets (≥44pt)
- High contrast
- Brief text
- Use complications for the at-a-glance value

### What doesn't work
- Long text input (use Dictation, Siri, Scribble)
- Complex multi-step flows
- Browsing
- Persistent media consumption

## 5. tvOS — the focus engine

### Constraints
- Remote-based: focus engine moves focus
- 10-foot viewing: text must be larger
- Living room: shared experience; minimal personal input
- No touch (Siri Remote has touchpad but is not primary)

### Focus engine
- Focused element gets visual emphasis (lift, glow)
- Plan focus order explicitly
- Don't fight the focus engine

### Layout
- Larger spacing
- Use full-screen when possible
- Tab bar at top (not bottom)
- Sidebar for browsing

### What doesn't work
- Long text input (Siri Remote keyboard is painful)
- Detailed lists with small text
- Touch-only gestures

## 6. visionOS — spatial computing

### Core concepts
- **Windows** — 2D, like iPad windows in space
- **Volumes** — 3D bounded objects (e.g., a 3D model)
- **Immersive spaces** — full-environment (e.g., VR experience)

### Input
- **Eye tracking** — what user is looking at
- **Hand pinch** — primary "tap" gesture
- **Voice (Siri)** — for dictation, simple commands
- **Hardware (Mac keyboard / trackpad) when paired**

### Design principles
- Content at conversational depth (~1.5m)
- High contrast; readable from a distance
- Avoid attention-grabbing motion (vestibular)
- Allow user to position window/volume
- Glass material for windows (system default)

### What's new
- Hover state (eye gaze) requires affordances
- Pinch gesture replaces tap
- Depth and parallax for hierarchy
- Don't force users to walk through content

## 7. Cross-platform development strategy

### One codebase, multi-platform (SwiftUI)
- Same view hierarchy adapts to platform
- Platform-specific modifiers handle differences
- Maximum code share; effort to nail each platform's nuances

### Per-platform optimization
- SwiftUI base + platform-specific tuning
- Most popular pattern (2026)
- Best results for production apps

### Catalyst (iPad → Mac)
- Lower lift, less native feel on Mac
- Good for utility apps; less good for productivity

### Per-platform from scratch
- Highest quality
- Highest cost
- Reserve for apps where platform-specific UX is differentiating

## 8. Asset adaptation

### App icons
- 1024×1024 for iOS / iPadOS
- 1024×1024 for macOS (different design — usually richer detail)
- 384×384 for watchOS
- 1280×768 for tvOS (top shelf)
- Apple Vision: custom 3D icon variant

### Screenshots (App Store)
- Per device size
- Show platform-native UX
- Don't reuse iPhone screenshots for iPad

## 9. App Intents and ecosystem features

App Intents make app actions available in:
- **Shortcuts** — user-built automations
- **Siri** — voice-triggered
- **Spotlight** — search-triggered
- **Lock Screen / Home Screen widgets**
- **Apple Watch complications**
- **Apple Intelligence** — system suggests actions

Critical for power users and ecosystem integration.

## 10. Common pitfalls

- **Treating iPad as a big iPhone.** Use sidebar, inspector, popover.
- **Treating Mac as a big iPad.** Embrace mouse, menus, multiple windows.
- **Designing Watch app as a phone app variant.** It's a different product.
- **Designing TV app like a phone app.** Focus engine + 10-foot UI are different.
- **One asset size for all platforms.** Icons, screenshots, layouts differ.
- **Sharing animations that feel wrong on big screen.** Tune motion per platform.
- **iPad app without keyboard shortcuts.** Power users leave.
- **Watch app that requires phone.** Make it standalone where possible.
- **visionOS app that doesn't respect depth.** Feels like a flat iPad app floating.
