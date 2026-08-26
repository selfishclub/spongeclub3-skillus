# Apple HIG Fundamentals Reference

Foundational concepts from Apple's Human Interface Guidelines, distilled
to what you actually use day-to-day.

## 1. The HIG principles (across all platforms)

1. **Clarity** — content is legible; UI doesn't compete with content
2. **Deference** — UI defers to content; system chrome stays out of the way
3. **Depth** — visual hierarchy and motion convey structure
4. **Consistency** — interactions follow platform conventions
5. **Direct manipulation** — users act on objects, not buttons that act on objects
6. **Feedback** — immediate response to every interaction
7. **Metaphors** — familiar mental models when appropriate
8. **User control** — users initiate and control; UI doesn't surprise

These read abstract until you violate one and users notice.

## 2. Layout fundamentals

### Spacing
- Use multiples of 4 or 8 points (Apple uses 4-point grid; iOS uses 8)
- Standard layout margins: 16pt iPhone, 20pt iPad, 22pt macOS
- Safe areas: respect them; content gets clipped otherwise
- Reading width: ~50-75 characters per line for body text

### Touch targets
- **Minimum:** 44pt × 44pt for any tappable area
- Larger for primary actions and accessibility
- Spacing between targets: ≥ 8pt typically

### Visual hierarchy
- Size + weight + color carry hierarchy
- Don't rely solely on color (accessibility)
- Most-important action visually prominent
- Secondary actions present but quieter

## 3. Typography — Dynamic Type

Apple's text system scales with user accessibility settings.

### Text styles (use these names)
- `largeTitle` — biggest, used for screen titles in some contexts
- `title1`, `title2`, `title3` — section headers
- `headline` — emphasized body
- `body` — primary text
- `callout`, `subheadline` — secondary text
- `footnote`, `caption1`, `caption2` — minor metadata

### Custom fonts
- Use `UIFontMetrics` (UIKit) or `dynamicTypeSize` (SwiftUI) to scale
- Test at all sizes (`xSmall` → `accessibility5`)
- Reserve custom fonts for brand moments; system font is fast + accessible

### Numerics
- Use the SF Mono variant for tabular data
- Or use `monospacedDigit` modifier for numerals only

## 4. Color system

### Semantic colors (use these)
- `systemBackground`, `secondarySystemBackground`, `tertiarySystemBackground`
- `label`, `secondaryLabel`, `tertiaryLabel`, `quaternaryLabel`
- `separator`, `opaqueSeparator`
- `link`
- `systemFill`, `secondarySystemFill`, `tertiarySystemFill`

These adapt automatically to:
- Light mode / dark mode
- Increased contrast (Accessibility setting)
- Elevation (in macOS-style hierarchies)

### Tint color
- Each platform has a system tint (blue by default)
- Override with brand color in Asset Catalog
- Buttons, links, selection use tint by default

### Avoid
- Hardcoded hex colors for body text or backgrounds
- Color alone to convey state (e.g., red for error without an icon)
- Brand colors that fail contrast in dark mode

## 5. Materials (vibrancy, blur)

Apple's materials provide hierarchy through translucent layers:

- `regularMaterial`, `thickMaterial`, `thinMaterial`, `ultraThinMaterial`
- Used in: navigation bars, tab bars, popovers, sheets, sidebars
- Don't fight the system; use the material your container expects

## 6. Icons

### SF Symbols
- Apple's icon library, ~5000+ symbols, free
- Adapt to text style automatically (scale, weight)
- Multi-color variants available
- Use these instead of custom icons whenever possible

### Custom icons
- 24pt × 24pt at default; provide @2x and @3x
- Match SF Symbols' visual weight
- Use template images for tint-able icons

## 7. Motion and animation

### Standard durations
- Quick transitions: 0.2s
- Standard: 0.3s
- Slower (e.g., sheet present): 0.35–0.5s

### Easing
- Use system defaults (`easeInOut`, `spring`)
- Don't reinvent timing curves; users feel the difference

### Reduce Motion
- Respect the user's "Reduce Motion" accessibility setting
- Replace transition animations with cross-fade or none
- Important for users with vestibular sensitivities

### Haptics (iOS)
- Use system haptics (`UIImpactFeedbackGenerator`, `UINotificationFeedbackGenerator`)
- For: successful actions, errors, selection changes, drag-and-drop
- Don't overuse; subtle is the goal

## 8. Sounds

- iOS apps generally don't play sounds for UI events
- macOS apps have more system sounds available
- Respect the user's mute switch and Do Not Disturb

## 9. Localization and internationalization

### Text expansion
- Other languages can be 30-100% longer than English
- Design with room; text should wrap, not truncate
- Test in German (long words), Japanese (vertical text), Arabic (RTL)

### Right-to-left (RTL)
- Layout flips: leading/trailing edges swap
- Use `.leading` / `.trailing` in SwiftUI; not `.left` / `.right`
- Test RTL renders correctly

### Date / number formatting
- Use system formatters (`DateFormatter`, `NumberFormatter`, `MeasurementFormatter`)
- Never hardcode "/" or "," — formats vary by locale

## 10. App lifecycle

### iOS state
- App can be terminated at any time; save state aggressively
- Background tasks have time limits (~30 seconds)
- Push notifications wake briefly; respect that

### iPadOS multitasking
- App can run in Split View, Slide Over, Stage Manager
- Layout must respond to size class changes mid-session

### macOS lifecycle
- App may have no windows (just menu bar); design for that
- Window restoration: app state persists across launches

## 11. App Store guidelines (the design-impacting bits)

- 1024×1024 app icon, no transparency, no rounded corners (system rounds)
- Screenshots for each device size; show actual app, not marketing
- Privacy nutrition labels: declare data collection truthfully
- In-app purchases: must use StoreKit; can't link to external payment

## 12. Common pitfalls

- **Hardcoded sizes everywhere.** Breaks Dynamic Type, accessibility, device variation.
- **Custom UI for navigation.** Users expect the native nav.
- **Ignoring safe areas.** Content clipped on iPhones with notches / home indicators.
- **Same UI on iPhone and iPad.** They're different devices.
- **Brand colors that fail dark mode.** Test both.
- **No haptic feedback.** Apps that use it feel premium.
- **Forgetting RTL.** A growing market.
- **Hijacking system gestures.** Edge swipes, control center, etc.
- **Modal-heavy navigation.** iOS users prefer push-nav.
- **Ignoring keyboard on iPad.** Major productivity user base.
