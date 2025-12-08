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
  favicon: 'img/favicon.ico',

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
          alt: 'Physical AI Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'curriculumSidebar',
            position: 'left',
            label: 'Curriculum',
          },
          {
            to: 'docs/modules/ros2-nervous-system',
            label: 'Module 1: ROS 2',
            position: 'left'
          },
          {
            to: 'docs/modules/gazebo-unity-digital-twin',
            label: 'Module 2: Digital Twin',
            position: 'left'
          },
          {
            to: 'docs/modules/isaac-ai-brain',
            label: 'Module 3: Isaac AI',
            position: 'left'
          },
          {
            to: 'docs/modules/vla-integration',
            label: 'Module 4: VLA Integration',
            position: 'left'
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
            title: 'Curriculum',
            items: [
              {
                label: 'Module 1: ROS 2 Nervous System',
                to: 'docs/modules/ros2-nervous-system',
              },
              {
                label: 'Module 2: Digital Twin (Gazebo & Unity)',
                to: 'docs/modules/gazebo-unity-digital-twin',
              },
              {
                label: 'Module 3: Isaac AI Brain',
                to: 'docs/modules/isaac-ai-brain',
              },
              {
                label: 'Module 4: VLA Integration',
                to: 'docs/modules/vla-integration',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/NazimAkhter/hackathon_01_humanoid_book',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'Educational Platform',
                href: 'https://github.com/NazimAkhter/hackathon_01_humanoid_book',
              },
            ],
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