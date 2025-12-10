// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics Education',
  tagline: 'Learn Robotics, AI, and Humanoid Systems',
  favicon: 'img/icons/favicon.ico',

  // Set the production url of your site here
  url: 'https://hackathon-01-humanoid-book.vercel.app',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For Vercel deployment, use root path
  baseUrl: '/',

  // Repository config
  organizationName: 'NazimAkhter',
  projectName: 'hackathon_01_humanoid_book',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  headTags: [
    {
      tagName: 'link',
      attributes: {
        rel: 'icon',
        href: '/img/icons/favicon.ico',
      },
    },
  ],

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/NazimAkhter/hackathon_01_humanoid_book/tree/master/',
          // Route base path for docs - default is '/docs'
          routeBasePath: '/docs',
        },
        blog: false, // Disable blog for educational platform
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'Physical AI Education',
        logo: {
          alt: 'Physical AI & Humanoid Robotics Logo',
          src: 'img/logos/robot-logo.png',
          srcDark: 'img/logos/robot-logo.png',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'curriculumSidebar',
            position: 'left',
            label: 'Curriculum',
          },
          {
            type: 'dropdown',
            label: 'Resources',
            position: 'left',
            items: [
              { label: 'Documentation', to: '/docs/project/introduction' },
              { label: 'Project Setup', to: '/docs/project/setup' },
              { label: 'Development Guide', to: '/docs/project/development' },
              { label: 'Examples', to: '/docs/project' },
            ]
          },
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
          },
          {
            href: 'https://github.com/NazimAkhter/hackathon_01_humanoid_book',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Learn',
            items: [
              { label: 'Getting Started', to: '/docs/project/introduction' },
            ]
          },
          {
            title: 'Resources',
            items: [
              { label: 'Documentation', to: '/docs/project/introduction' },
              { label: 'Project Setup', to: '/docs/project/setup' },
              { label: 'Development Guide', to: '/docs/project/development' },
              { label: 'Deployment', to: '/docs/project/deployment' },
            ]
          },
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
          },
          {
            title: 'More',
            items: [
              {
                label: 'License',
                href: 'https://github.com/NazimAkhter/hackathon_01_humanoid_book/blob/master/LICENSE'
              },
            ]
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Education. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;