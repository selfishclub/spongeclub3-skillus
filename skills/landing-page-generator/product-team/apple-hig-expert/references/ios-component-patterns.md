# iOS Component Patterns Reference

Practical reference for iOS-specific component selection and interaction
patterns.

## 1. Navigation patterns

### Navigation stack (push)
- Hierarchical drill-in
- Back gesture (swipe from left edge) — never break this
- Title in nav bar; large title when scrolled to top
- Use for: master-detail flows, drill-down browsing

### Tab bar
- Top-level navigation between 3-5 sections
- Bottom of screen
- Doesn't disappear during nav stack pushes
- Use for: parallel main sections

### Sheet
- Modal task with clear dismiss (close button or swipe down)
- Detents: small, medium, large
- Use for: secondary task that doesn't fit in current context

### Full-screen cover
- Immersive task (photo editor, video player, sign-up flow)
- No surrounding context; back/done explicit
- Use for: distinct mode where return-to-current is the model

### Popover (iPad-primary)
- Context-anchored options
- On iPhone (compact width): popover becomes a sheet automatically
- Use for: brief contextual choices

### Inspector
- Persistent secondary pane
- iPadOS + macOS
- Use for: properties / metadata that complement primary content

### Sidebar (NavigationSplitView)
- Top-level + secondary level visible simultaneously
- iPad + Mac primarily; collapses to nav stack on iPhone
- Use for: large information architecture

### Menu (button)
- Tap reveals menu of options
- Replaces older action sheet for most cases
- Use for: hidden options on a row or button

### Action sheet
- Bottom sheet with 2-8 options + cancel
- Use for: destructive choice, complex multi-option

## 2. Lists and collections

### List (`List`)
- Standard scrollable rows
- Built-in swipe actions, selection, hierarchy disclosure
- Reorder + delete + multi-select supported
- Use for: any homogeneous scrollable rows

### Grid (`LazyVGrid` / `LazyHGrid`)
- 2D layout of items
- Use for: photos, cards, browsable galleries

### Scroll view
- When you need full layout control
- Use for: non-list content that scrolls

### Disclosure / expandable rows
- Built-in for List
- Use for: hierarchical content (folders, categories)

### Anti-patterns
- Custom list with no swipe actions or accessibility
- Hidden bulk actions (e.g., requiring long-press without affordance)
- Mixed visual styles in the same list

## 3. Controls

### Button styles
- `bordered`, `borderedProminent`, `borderless`, `plain`
- `controlSize`: `mini`, `small`, `regular`, `large`
- Prominent for primary action; bordered for secondary
- Plain for in-line text actions

### Toggle, picker, slider, stepper
- Use native; don't recreate
- Toggle for boolean
- Picker for one-of-many
- Stepper for small increment / decrement
- Slider for continuous value

### Text field, text editor, secure field
- TextField for single-line input
- TextEditor for multi-line (SwiftUI 14+)
- SecureField for passwords
- Keyboard types matter (`.emailAddress`, `.numberPad`)

### Date / color / value pickers
- DatePicker — multiple styles (graphical, wheel, compact)
- ColorPicker — system component
- Don't build custom unless absolutely required

## 4. Search

### Searchable modifier
- Built-in for SwiftUI; works with navigation
- Search field appears in nav bar
- Filter content reactively

### Scopes
- Optional segmented control above results
- Use when search has distinct categories (e.g., "All", "Files", "People")

## 5. Refresh and pull-to-refresh

- `refreshable` modifier — built-in indicator
- Reserve for content that benefits from explicit refresh
- Don't use as the only way to refresh (network changes should auto-update)

## 6. Toolbars

### Top toolbar (navigation bar)
- Title (large or inline)
- Leading + trailing items
- Bottom bar (additional actions)

### Bottom toolbar
- Used on iPhone for primary actions
- Especially for editing modes

### Keyboard toolbar
- Above keyboard
- For done/cancel buttons or formatting controls

## 7. Gestures

### System gestures (don't override)
- Edge swipe (back navigation)
- Pull-to-refresh
- Long press on app icon
- Swipe down from top (notifications)
- Control center

### App gestures (use carefully)
- Tap, double-tap, long press
- Drag, swipe, pinch, rotate
- Provide haptic feedback for confirmations
- Combine with visual cues (arrows, animations)

### Anti-patterns
- Hijacking back gesture
- Multi-finger gestures users wouldn't discover
- Overlapping with system gestures

## 8. Feedback patterns

### Loading states
- Skeleton screens > spinners for content
- Spinner OK for brief operations
- Avoid blocking the UI when possible

### Empty states
- Don't just show an empty list
- Friendly message + primary action
- SF Symbols can help convey the state

### Error states
- Clear message about what went wrong
- Specific suggested action (retry, contact support)
- Avoid technical jargon

### Confirmation
- Sheet/alert for destructive actions
- Snackbar/toast for transient confirmations
- Haptic for tactile confirmation

## 9. Onboarding patterns

### What to do
- Get users to first value FAST
- Sign-in optional unless required
- Explain key permissions in context (right before asking)

### What to avoid
- Multi-page swipe-through tour with no value
- Asking for all permissions on launch
- Long welcome flows that block the value

## 10. Sharing and system integrations

### Share sheet (`ShareLink`)
- System share sheet — all installed targets
- Don't custom-build sharing

### Universal Links
- Open content in your app when web URL is shared
- Improves continuity, deep linking

### App Intents
- Expose app actions to Shortcuts, Siri, Spotlight
- Vital for power users and Apple Intelligence

### Widgets
- Home Screen, Lock Screen, StandBy
- Show timely, glanceable info
- Don't replicate the full app; pick a single useful surface

## 11. Live Activities (iOS 16+)

- Persistent updates in Dynamic Island and Lock Screen
- Use for: orders in transit, sports scores, timers, ride status
- Updates ~once per minute typical
- Strict size + content limits

## 12. Common pitfalls

- **Custom modals replacing sheets.** Users lose dismiss affordances.
- **Hamburger menu on iOS.** Tab bar is more discoverable.
- **Custom search.** Native is faster, accessible, and consistent.
- **Splash screens that linger.** Native launch screens fade fast.
- **Multi-tap to confirm.** Users miss the second tap.
- **All-modal app.** Navigation stack should be primary.
- **No back button affordance.** Even with gestures, label the back action.
- **Keyboard covering input.** Use `keyboardAdaptive` / safe area insets.
- **Ignoring rotation / size classes.** App must handle orientation changes.
- **iPad app that's stretched iPhone.** Use sidebar, inspector, popover patterns.
