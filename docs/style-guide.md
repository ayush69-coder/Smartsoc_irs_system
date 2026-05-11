# PhishGuard Pro - Style Guide

## Overview
This style guide defines the design system, components, and visual standards for PhishGuard Pro, a modern AI-powered phishing detection platform.

## Design Principles

### 1. Security-First Design
- **Trust**: Clean, professional interface that conveys reliability
- **Clarity**: Clear visual hierarchy and information architecture
- **Transparency**: Open communication about AI decisions and explanations

### 2. Modern & Minimal
- **Clean Lines**: Simple, uncluttered layouts
- **White Space**: Generous spacing for readability
- **Focus**: Highlight important information without distraction

### 3. Accessibility
- **Contrast**: High contrast ratios for readability
- **Navigation**: Clear, consistent navigation patterns
- **Responsive**: Works across all device sizes

## Color Palette

### Primary Colors
- **Blue**: `#3B82F6` - Primary actions, links, highlights
- **Green**: `#10B981` - Success states, legitimate content
- **Red**: `#EF4444` - Alerts, phishing content, danger
- **Yellow**: `#F59E0B` - Warnings, caution states
- **Gray**: `#6B7280` - Secondary text, borders

### Background Colors
- **Dark**: `#111827` - Main background
- **Card**: `#1F2937` - Card backgrounds
- **Border**: `#374151` - Borders and dividers
- **Hover**: `#374151` - Hover states

### Text Colors
- **Primary**: `#FFFFFF` - Main text
- **Secondary**: `#D1D5DB` - Secondary text
- **Muted**: `#9CA3AF` - Muted text
- **Disabled**: `#6B7280` - Disabled text

## Typography

### Font Stack
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
```

### Font Sizes
- **Display**: `3rem` (48px) - Page titles
- **Heading 1**: `2.25rem` (36px) - Section headers
- **Heading 2**: `1.875rem` (30px) - Subsection headers
- **Heading 3**: `1.5rem` (24px) - Card titles
- **Body Large**: `1.125rem` (18px) - Important text
- **Body**: `1rem` (16px) - Regular text
- **Body Small**: `0.875rem` (14px) - Secondary text
- **Caption**: `0.75rem` (12px) - Labels, captions

### Font Weights
- **Light**: 300
- **Regular**: 400
- **Medium**: 500
- **Semibold**: 600
- **Bold**: 700

## Components

### Buttons

#### Primary Button
```css
background: #3B82F6;
color: #FFFFFF;
padding: 0.5rem 1rem;
border-radius: 0.375rem;
font-weight: 500;
```

#### Secondary Button
```css
background: #374151;
color: #FFFFFF;
padding: 0.5rem 1rem;
border-radius: 0.375rem;
font-weight: 500;
```

#### Danger Button
```css
background: #EF4444;
color: #FFFFFF;
padding: 0.5rem 1rem;
border-radius: 0.375rem;
font-weight: 500;
```

### Cards

#### Standard Card
```css
background: #1F2937;
border: 1px solid #374151;
border-radius: 0.5rem;
padding: 1.5rem;
box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
```

#### Interactive Card
```css
background: #1F2937;
border: 1px solid #374151;
border-radius: 0.5rem;
padding: 1.5rem;
transition: all 0.2s ease-in-out;
```

#### Interactive Card Hover
```css
transform: translateY(-2px);
box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
```

### Status Badges

#### Success Badge
```css
background: #D1FAE5;
color: #065F46;
padding: 0.25rem 0.5rem;
border-radius: 9999px;
font-size: 0.75rem;
font-weight: 500;
```

#### Warning Badge
```css
background: #FEF3C7;
color: #92400E;
padding: 0.25rem 0.5rem;
border-radius: 9999px;
font-size: 0.75rem;
font-weight: 500;
```

#### Danger Badge
```css
background: #FEE2E2;
color: #991B1B;
padding: 0.25rem 0.5rem;
border-radius: 9999px;
font-size: 0.75rem;
font-weight: 500;
```

### Forms

#### Input Field
```css
background: #374151;
border: 1px solid #4B5563;
color: #FFFFFF;
padding: 0.5rem 0.75rem;
border-radius: 0.375rem;
font-size: 0.875rem;
```

#### Input Field Focus
```css
border-color: #3B82F6;
box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
outline: none;
```

#### Label
```css
color: #D1D5DB;
font-size: 0.875rem;
font-weight: 500;
margin-bottom: 0.5rem;
```

## Animations

### Fade In
```css
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### Slide In
```css
@keyframes slideIn {
  from {
    transform: translateX(100%);
  }
  to {
    transform: translateX(0);
  }
}
```

### Hover Lift
```css
.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
}
```

## Layout

### Grid System
- **Mobile**: 1 column
- **Tablet**: 2 columns
- **Desktop**: 3-4 columns
- **Gap**: 1.5rem (24px) between grid items

### Spacing Scale
- **xs**: 0.25rem (4px)
- **sm**: 0.5rem (8px)
- **md**: 1rem (16px)
- **lg**: 1.5rem (24px)
- **xl**: 2rem (32px)
- **2xl**: 3rem (48px)

### Border Radius
- **sm**: 0.25rem (4px)
- **md**: 0.375rem (6px)
- **lg**: 0.5rem (8px)
- **xl**: 0.75rem (12px)
- **full**: 9999px (circular)

## Icons

### Icon Library
- **Heroicons**: Primary icon library
- **Size**: 16px, 20px, 24px, 32px
- **Style**: Outline for regular use, solid for emphasis
- **Color**: Inherit from parent or use semantic colors

### Icon Usage
- **Navigation**: 20px outline icons
- **Actions**: 16px outline icons
- **Status**: 16px solid icons with semantic colors
- **Decorative**: 24px outline icons

## Accessibility

### Color Contrast
- **Normal Text**: 4.5:1 minimum contrast ratio
- **Large Text**: 3:1 minimum contrast ratio
- **Interactive Elements**: 3:1 minimum contrast ratio

### Focus States
- **Visible Focus**: All interactive elements have visible focus indicators
- **Keyboard Navigation**: All functionality accessible via keyboard
- **Screen Reader**: Proper ARIA labels and semantic HTML

### Motion
- **Respect Preferences**: Honor `prefers-reduced-motion` setting
- **Subtle Animations**: Use subtle, purposeful animations
- **No Flashing**: Avoid flashing or strobing effects

## Responsive Design

### Breakpoints
- **Mobile**: 0-768px
- **Tablet**: 768px-1024px
- **Desktop**: 1024px+

### Mobile Considerations
- **Touch Targets**: Minimum 44px touch targets
- **Readable Text**: Minimum 16px font size
- **Thumb Navigation**: Important actions within thumb reach

## Dark Theme

### Implementation
- **CSS Variables**: Use CSS custom properties for theming
- **System Preference**: Respect user's system theme preference
- **Toggle**: Provide manual theme toggle

### Dark Theme Colors
- **Background**: `#111827`
- **Surface**: `#1F2937`
- **Border**: `#374151`
- **Text Primary**: `#FFFFFF`
- **Text Secondary**: `#D1D5DB`

## Implementation Notes

### CSS Framework
- **Tailwind CSS**: Primary utility framework
- **Custom CSS**: Additional animations and components
- **PostCSS**: Processing and optimization

### Component Structure
- **Atomic Design**: Build from atoms to organisms
- **Reusable**: Components should be reusable across pages
- **Consistent**: Maintain consistent styling patterns

### Performance
- **Critical CSS**: Inline critical styles
- **Lazy Loading**: Load non-critical styles asynchronously
- **Optimization**: Minify and compress CSS

## Examples

### Page Layout
```html
<div class="min-h-screen bg-gray-900 text-white">
  <div class="flex">
    <Sidebar />
    <div class="flex-1 flex flex-col">
      <Navbar />
      <main class="flex-1 p-6">
        <PageContent />
      </main>
    </div>
  </div>
</div>
```

### Card Component
```html
<div class="bg-gray-800 rounded-lg p-6 border border-gray-700 hover-lift animate-fade-in">
  <h3 class="text-lg font-semibold text-white mb-2">Card Title</h3>
  <p class="text-gray-300">Card content goes here.</p>
</div>
```

### Button Component
```html
<button class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors">
  Click Me
</button>
```

This style guide ensures consistency, accessibility, and a professional appearance across the PhishGuard Pro platform.