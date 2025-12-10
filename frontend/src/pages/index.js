import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <div className={styles.heroContent}>
          <div className={styles.heroText}>
            <h1 className="hero__title">{siteConfig.title}</h1>
            <p className="hero__subtitle">{siteConfig.tagline}</p>
            <div className={styles.buttons}>
              <Link
                className="button button--primary button--lg"
                to="/docs/project/introduction">
                Get Started →
              </Link>
              <Link
                className="button button--secondary button--lg margin-left--md"
                to="/docs/modules/ros2-nervous-system/">
                Explore Modules
              </Link>
            </div>
          </div>
          <div className={styles.heroImage}>
            <picture>
              <source
                srcSet="/img/heroes/futuristic-robot-hero.png"
                type="image/png"
              />
              <img
                src="/img/heroes/futuristic-robot-hero.png"
                alt="Modern humanoid robot representing Physical AI education"
                loading="lazy"
              />
            </picture>
          </div>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="Educational platform for Physical AI & Humanoid Robotics">
      <HomepageHeader />
      <main>
        <section className={styles.features}>
          <div className="container">
            <div className="row">
              <div className="col col--4">
                <div className="text--center padding-horiz--md">
                  <h3>Comprehensive Curriculum</h3>
                  <p>Four integrated modules covering ROS 2, Digital Twins, Isaac AI, and Vision-Language-Action systems.</p>
                </div>
              </div>
              <div className="col col--4">
                <div className="text--center padding-horiz--md">
                  <h3>Hands-on Learning</h3>
                  <p>Practical exercises and projects that combine theory with real implementation.</p>
                </div>
              </div>
              <div className="col col--4">
                <div className="text--center padding-horiz--md">
                  <h3>Industry Ready</h3>
                  <p>Learn cutting-edge technologies used in modern robotics and AI applications.</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className={styles.modules}>
          <div className="container padding-vert--lg">
            <div className="row">
              <div className="col col--12">
                <h2 className="text--center">Curriculum Modules</h2>
                <p className="text--center padding-horiz--md">
                  Our comprehensive curriculum is designed to take you from beginner to advanced robotics engineer.
                </p>
              </div>
            </div>

            <div className="row padding-vert--lg">
              <div className="col col--3">
                <div className="card">
                  <div className="card__header">
                    <h3>Module 1: ROS 2 Nervous System</h3>
                  </div>
                  <div className="card__body">
                    <p>Learn ROS 2 as the nervous system for humanoid robotics, including architecture, communication patterns, and integration.</p>
                  </div>
                  <div className="card__footer">
                    <Link className="button button--primary" to="/docs/modules/ros2-nervous-system/">
                      Start Module
                    </Link>
                  </div>
                </div>
              </div>

              <div className="col col--3">
                <div className="card">
                  <div className="card__header">
                    <h3>Module 2: Digital Twin</h3>
                  </div>
                  <div className="card__body">
                    <p>Create and use digital twins with Gazebo and Unity for simulation, testing, and development.</p>
                  </div>
                  <div className="card__footer">
                    <Link className="button button--primary" to="/docs/modules/gazebo-unity-digital-twin/">
                      Start Module
                    </Link>
                  </div>
                </div>
              </div>

              <div className="col col--3">
                <div className="card">
                  <div className="card__header">
                    <h3>Module 3: Isaac AI Brain</h3>
                  </div>
                  <div className="card__body">
                    <p>NVIDIA Isaac for AI-powered robotics, including computer vision, perception, and intelligent decision-making.</p>
                  </div>
                  <div className="card__footer">
                    <Link className="button button--primary" to="/docs/modules/isaac-ai-brain/">
                      Start Module
                    </Link>
                  </div>
                </div>
              </div>

              <div className="col col--3">
                <div className="card">
                  <div className="card__header">
                    <h3>Module 4: VLA Integration</h3>
                  </div>
                  <div className="card__body">
                    <p>Vision-Language-Action integration for natural human-robot interaction using advanced AI systems.</p>
                  </div>
                  <div className="card__footer">
                    <Link className="button button--primary" to="/docs/modules/vla-integration/">
                      Start Module
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}