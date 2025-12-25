import React from 'react';
import styles from './styles.module.css';

/**
 * Loading indicator shown while waiting for bot response
 */
export default function LoadingIndicator() {
  return (
    <div className={`${styles.message} ${styles.messageBot}`}>
      <div className={styles.loadingDots}>
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>
  );
}
