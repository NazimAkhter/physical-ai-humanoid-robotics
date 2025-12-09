# Tasks: Docusaurus UI/UX Improvements

## Feature: Enhanced Branding, Hero Section, and Navigation

**Goal**: Improve visual design and navigation completeness for the Physical AI & Humanoid Robotics educational platform

**Tech Stack**:
- Docusaurus v3 (React-based)
- Custom CSS modules
- SVG/WebP images
- Responsive design (mobile-first)

## User Stories

### US1: Brand Identity (P1)
**As a** visitor
**I want to** see professional branding with a custom logo
**So that** the platform appears credible and memorable

**Acceptance Criteria**:
- Logo appears in navbar (40x40px)
- Favicon displays in browser tab
- Logo works in light and dark modes
- All assets properly licensed

### US2: Engaging Hero Section (P1)
**As a** visitor
**I want to** see an engaging hero section with robot imagery
**So that** I understand the platform's focus immediately

**Acceptance Criteria**:
- Hero section displays robot image
- Layout is responsive (stacked on mobile, side-by-side on desktop)
- Images optimized (<200KB total)
- Call-to-action buttons are visible

### US3: Complete Navigation (P2)
**As a** user
**I want to** find all important links in navbar and footer
**So that** I can easily navigate to documentation, community, and resources

**Acceptance Criteria**:
- Navbar includes Resources and Community dropdowns
- Footer has 4 columns: Learn, Resources, Community, More
- All links are functional
- Mobile hamburger menu works

## Implementation Strategy

**MVP Scope**: US1 + US2 (Logo and Hero section)
**Phase 2**: US3 (Navigation completeness)
**Incremental Delivery**: Each user story is independently deployable

## Dependencies

```
Phase 1 (Setup)
    ↓
Phase 2 (US1: Brand Identity)
    ↓
Phase 3 (US2: Hero Section) [Can run parallel with US1 after setup]
    ↓
Phase 4 (US3: Navigation)
    ↓
Phase 5 (Polish)
```

**Parallel Opportunities**:
- After Phase 1: US1 and US2 tasks can run in parallel (different files)
- US3 can start once US1 navbar config is understood

---

## Phase 1: Setup & Asset Preparation

**Goal**: Prepare development environment and source all required assets

### Tasks

- [ ] T001 Create tasks directory structure in `tasks/002-ui-ux-improvements/`
- [ ] T002 [P] Source robot icon from Heroicons for temporary logo at https://heroicons.com/
- [ ] T003 [P] Download high-quality robot image from Unsplash at https://unsplash.com/s/photos/humanoid-robot
- [ ] T004 [P] Optimize hero image with Squoosh (WebP 80% quality) at https://squoosh.app/
- [ ] T005 [P] Create PNG fallback for hero image (for older browsers)
- [ ] T006 [P] Generate favicon variants using RealFaviconGenerator at https://realfavicongenerator.net/
- [ ] T007 [P] Create `frontend/static/img/` subdirectories: logos/, heroes/, icons/
- [ ] T008 Verify all downloaded assets have proper licenses (CC0 or MIT)
- [ ] T009 Document asset sources in `tasks/002-ui-ux-improvements/ASSETS.md`

**Acceptance**: All assets downloaded, optimized, and placed in correct directories

---

## Phase 2: US1 - Brand Identity

**Goal**: Implement professional branding with custom logo

**Story**: As a visitor, I want to see professional branding with a custom logo

### Tasks

- [ ] T010 [US1] Copy logo SVG to `frontend/static/img/logos/logo.svg`
- [ ] T011 [US1] Copy dark mode logo variant to `frontend/static/img/logos/logo-dark.svg` (if different)
- [ ] T012 [US1] Copy all favicon files to `frontend/static/img/icons/`
- [ ] T013 [US1] Update navbar logo configuration in `frontend/docusaurus.config.js`:
  ```javascript
  navbar: {
    logo: {
      alt: 'Physical AI & Humanoid Robotics Logo',
      src: 'img/logos/logo.svg',
      srcDark: 'img/logos/logo-dark.svg',
    }
  }
  ```
- [ ] T014 [US1] Update HTML head section in `frontend/docusaurus.config.js` to include favicon:
  ```javascript
  headTags: [
    {
      tagName: 'link',
      attributes: {
        rel: 'icon',
        href: '/img/icons/favicon.ico',
      },
    },
  ]
  ```
- [ ] T015 [P] [US1] Add apple-touch-icon link in `frontend/static/img/icons/apple-touch-icon.png`
- [ ] T016 [US1] Test logo displays correctly in navbar (light mode)
- [ ] T017 [US1] Test logo displays correctly in navbar (dark mode)
- [ ] T018 [US1] Test favicon appears in browser tab
- [ ] T019 [US1] Verify logo is responsive on mobile devices
- [ ] T020 [US1] Run Lighthouse accessibility audit for logo alt text

**US1 Acceptance Test**:
```bash
cd frontend
npm start
# Manual verification:
# 1. Logo appears in navbar at correct size
# 2. Favicon shows in browser tab
# 3. Logo adapts to dark mode if enabled
# 4. Alt text is present for screen readers
```

---

## Phase 3: US2 - Engaging Hero Section

**Goal**: Create compelling hero section with robot imagery

**Story**: As a visitor, I want to see an engaging hero section with robot imagery

### Tasks

- [ ] T021 [P] [US2] Copy optimized hero image to `frontend/static/img/heroes/hero-robot.webp`
- [ ] T022 [P] [US2] Copy PNG fallback to `frontend/static/img/heroes/hero-robot.png`
- [ ] T023 [P] [US2] Create responsive variants (1920px, 1280px, 640px) using Squoosh
- [ ] T024 [US2] Read current homepage structure from `frontend/src/pages/index.js`
- [ ] T025 [US2] Modify hero banner section in `frontend/src/pages/index.js`:
  ```jsx
  <header className={styles.heroBanner}>
    <div className="container">
      <div className={styles.heroContent}>
        <div className={styles.heroText}>
          <h1 className="hero__title">{siteConfig.title}</h1>
          <p className="hero__subtitle">{siteConfig.tagline}</p>
          <div className={styles.buttons}>
            <Link
              className="button button--primary button--lg"
              to="/docs/intro">
              Get Started →
            </Link>
            <Link
              className="button button--secondary button--lg margin-left--md"
              to="/docs/modules">
              Explore Modules
            </Link>
          </div>
        </div>
        <div className={styles.heroImage}>
          <picture>
            <source
              srcSet="/img/heroes/hero-robot.webp"
              type="image/webp"
            />
            <img
              src="/img/heroes/hero-robot.png"
              alt="Modern humanoid robot representing Physical AI education"
              loading="lazy"
            />
          </picture>
        </div>
      </div>
    </div>
  </header>
  ```
- [ ] T026 [US2] Add hero section styles to `frontend/src/pages/index.module.css`:
  ```css
  .heroContent {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    align-items: center;
  }

  .heroText {
    text-align: left;
  }

  .heroImage img {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
  }

  @media (max-width: 768px) {
    .heroContent {
      grid-template-columns: 1fr;
      text-align: center;
    }

    .heroText {
      text-align: center;
    }

    .heroImage {
      order: -1;
    }
  }
  ```
- [ ] T027 [P] [US2] Add buttons styling to `frontend/src/css/custom.css` if needed
- [ ] T028 [US2] Test hero section layout on desktop (1920px)
- [ ] T029 [US2] Test hero section layout on tablet (768px)
- [ ] T030 [US2] Test hero section layout on mobile (375px)
- [ ] T031 [US2] Verify WebP fallback works in older browsers
- [ ] T032 [US2] Test lazy loading behavior (image loads after fold)
- [ ] T033 [US2] Run Lighthouse performance audit (target: <200KB images)
- [ ] T034 [US2] Verify CTA buttons navigate correctly

**US2 Acceptance Test**:
```bash
cd frontend
npm start
# Manual verification:
# 1. Hero section displays with robot image
# 2. Layout is responsive (side-by-side on desktop, stacked on mobile)
# 3. CTA buttons work and navigate to correct pages
# 4. Image loads efficiently with lazy loading
# Lighthouse: Performance >90, image size <200KB
```

---

## Phase 4: US3 - Complete Navigation

**Goal**: Ensure all essential links are present in navbar and footer

**Story**: As a user, I want to find all important links in navbar and footer

### Tasks

#### Navbar Enhancement

- [ ] T035 [US3] Read current navbar configuration from `frontend/docusaurus.config.js`
- [ ] T036 [US3] Add Resources dropdown to navbar in `frontend/docusaurus.config.js`:
  ```javascript
  {
    type: 'dropdown',
    label: 'Resources',
    position: 'left',
    items: [
      { label: 'Documentation', to: '/docs/intro' },
      { label: 'Project Setup', to: '/docs/project/setup' },
      { label: 'Development Guide', to: '/docs/project/development' },
      { label: 'Examples', to: '/docs/examples' },
    ]
  }
  ```
- [ ] T037 [P] [US3] Add Community dropdown to navbar in `frontend/docusaurus.config.js`:
  ```javascript
  {
    type: 'dropdown',
    label: 'Community',
    position: 'right',
    items: [
      {
        label: 'Discussions',
        href: 'https://github.com/NazimAkhter/hackathon_01_humanoid_book/discussions'
      },
      {
        label: 'Report Issues',
        href: 'https://github.com/NazimAkhter/hackathon_01_humanoid_book/issues'
      },
    ]
  }
  ```
- [ ] T038 [P] [US3] Reorganize module links for better UX in navbar (keep as quick access)
- [ ] T039 [US3] Test navbar dropdowns work on desktop
- [ ] T040 [US3] Test navbar collapses to hamburger menu on mobile
- [ ] T041 [US3] Verify all navbar links navigate correctly

#### Footer Enhancement

- [ ] T042 [US3] Read current footer configuration from `frontend/docusaurus.config.js`
- [ ] T043 [US3] Update footer with Learn column in `frontend/docusaurus.config.js`:
  ```javascript
  {
    title: 'Learn',
    items: [
      { label: 'Getting Started', to: '/docs/intro' },
      { label: 'Module 1: ROS 2', to: 'docs/modules/ros2-nervous-system' },
      { label: 'Module 2: Digital Twin', to: 'docs/modules/gazebo-unity-digital-twin' },
      { label: 'Module 3: Isaac AI', to: 'docs/modules/isaac-ai-brain' },
      { label: 'Module 4: VLA', to: 'docs/modules/vla-integration' },
    ]
  }
  ```
- [ ] T044 [P] [US3] Add Resources column to footer in `frontend/docusaurus.config.js`:
  ```javascript
  {
    title: 'Resources',
    items: [
      { label: 'Documentation', to: '/docs/intro' },
      { label: 'Project Setup', to: '/docs/project/setup' },
      { label: 'Development Guide', to: '/docs/project/development' },
      { label: 'Deployment', to: '/docs/project/deployment' },
    ]
  }
  ```
- [ ] T045 [P] [US3] Add Community column to footer in `frontend/docusaurus.config.js`:
  ```javascript
  {
    title: 'Community',
    items: [
      {
        label: 'GitHub Repository',
        href: 'https://github.com/NazimAkhter/hackathon_01_humanoid_book'
      },
      {
        label: 'Discussions',
        href: 'https://github.com/NazimAkhter/hackathon_01_humanoid_book/discussions'
      },
      {
        label: 'Report Issues',
        href: 'https://github.com/NazimAkhter/hackathon_01_humanoid_book/issues'
      },
    ]
  }
  ```
- [ ] T046 [P] [US3] Add More column to footer in `frontend/docusaurus.config.js`:
  ```javascript
  {
    title: 'More',
    items: [
      { label: 'About This Project', to: '/about' },
      {
        label: 'License',
        href: 'https://github.com/NazimAkhter/hackathon_01_humanoid_book/blob/master/LICENSE'
      },
    ]
  }
  ```
- [ ] T047 [US3] Test all footer links navigate correctly
- [ ] T048 [US3] Verify footer layout is responsive on mobile
- [ ] T049 [US3] Run accessibility audit on navigation elements

**US3 Acceptance Test**:
```bash
cd frontend
npm start
# Manual verification:
# 1. Navbar has Resources and Community dropdowns
# 2. Footer has 4 columns with correct links
# 3. All links navigate to correct destinations
# 4. Mobile navigation works (hamburger menu)
# 5. No broken links (404 errors)
```

---

## Phase 5: Polish & Cross-Cutting Concerns

**Goal**: Finalize implementation with optimization and quality checks

### Tasks

#### Accessibility

- [ ] T050 [P] Add descriptive alt text to all images in `frontend/src/pages/index.js`
- [ ] T051 [P] Verify color contrast ratios meet WCAG AA standards (4.5:1 for text)
- [ ] T052 [P] Test keyboard navigation through navbar and footer
- [ ] T053 [P] Ensure focus indicators are visible on all interactive elements
- [ ] T054 Run axe DevTools accessibility scan and fix any issues

#### Performance

- [ ] T055 [P] Verify image sizes meet budget (<500KB total new assets)
- [ ] T056 [P] Test lazy loading works for hero image
- [ ] T057 [P] Verify WebP images load on modern browsers
- [ ] T058 [P] Test PNG fallback loads on older browsers
- [ ] T059 Run Lighthouse performance audit (target: >90 score)
- [ ] T060 Check Cumulative Layout Shift (target: <0.1)

#### Cross-Browser Testing

- [ ] T061 [P] Test on Chrome (latest)
- [ ] T062 [P] Test on Firefox (latest)
- [ ] T063 [P] Test on Safari (latest)
- [ ] T064 [P] Test on Edge (latest)
- [ ] T065 [P] Test on mobile Safari (iOS)
- [ ] T066 [P] Test on mobile Chrome (Android)

#### SEO & Meta

- [ ] T067 [P] Add Open Graph meta tags in `frontend/docusaurus.config.js`
- [ ] T068 [P] Add Twitter Card meta tags in `frontend/docusaurus.config.js`
- [ ] T069 [P] Update site title and description for better SEO
- [ ] T070 Run Lighthouse SEO audit (target: >90 score)

#### Documentation

- [ ] T071 Update `DEPLOYMENT.md` with new assets information
- [ ] T072 Document logo and hero image sources in `tasks/002-ui-ux-improvements/ASSETS.md`
- [ ] T073 Add screenshots of new UI to `tasks/002-ui-ux-improvements/SCREENSHOTS.md`
- [ ] T074 Update `README.md` with new branding information

#### Final Verification

- [ ] T075 Verify all tasks completed and checked off
- [ ] T076 Run full build with `npm run build` to check for errors
- [ ] T077 Test production build locally with `npm run serve`
- [ ] T078 Create git commit with all changes
- [ ] T079 Push to GitHub and verify Vercel preview deployment
- [ ] T080 Review Vercel preview URL and test all features
- [ ] T081 Merge to production branch after approval

**Phase 5 Acceptance**:
```bash
cd frontend
npm run build
npm run serve
# Lighthouse audits:
# - Performance: >90
# - Accessibility: >95
# - Best Practices: >90
# - SEO: >90
# All browsers tested, no console errors
```

---

## Summary

**Total Tasks**: 81
- Phase 1 (Setup): 9 tasks
- Phase 2 (US1 - Brand Identity): 11 tasks
- Phase 3 (US2 - Hero Section): 14 tasks
- Phase 4 (US3 - Navigation): 15 tasks
- Phase 5 (Polish): 32 tasks

**Parallel Opportunities**: 40 tasks marked with [P] can run in parallel

**Independent Test Criteria**:
- US1: Logo visible, favicon working, responsive
- US2: Hero section responsive, images optimized, CTAs functional
- US3: All navigation links present and functional

**MVP Scope**: Phase 1 + Phase 2 + Phase 3 (Logo and Hero section)

**Timeline Estimate**:
- Phase 1: 1-2 hours
- Phase 2: 1-2 hours
- Phase 3: 2-3 hours
- Phase 4: 1-2 hours
- Phase 5: 2-3 hours
- **Total**: 7-12 hours

## Execution Notes

1. **Start with MVP**: Focus on US1 and US2 first for immediate visual impact
2. **Use Parallel Tasks**: Many asset preparation and testing tasks can run concurrently
3. **Test Incrementally**: Verify each user story independently before moving to next
4. **Lighthouse Early**: Run performance audits after US2 to catch issues early
5. **Mobile First**: Always test mobile responsiveness as you implement

## Risk Mitigation

- **Asset Licensing**: Verified all sources use CC0 or MIT licenses
- **Performance**: Budget monitored at <500KB total
- **Accessibility**: WCAG AA compliance checked incrementally
- **Browser Support**: Test matrix covers 95%+ of users
- **Rollback Plan**: Git commits per user story allow easy rollback

---

**Ready for Implementation**: All tasks are specific, testable, and include file paths for execution.
