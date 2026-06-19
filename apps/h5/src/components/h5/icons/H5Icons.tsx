import React from 'react';

export const Hamburger = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
    <path d="M4 6h16M4 12h16M4 18h16" stroke="#10142A" strokeWidth="2" strokeLinecap="round" />
  </svg>
);

export const EditIcon = () => (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
    <path d="M12 20h9" stroke="#9AA1B8" strokeWidth="1.8" strokeLinecap="round" />
    <path d="M16.5 3.5a2.121 2.121 0 013 3L7 19l-4 1 1-4L16.5 3.5z" stroke="#9AA1B8" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

export const PlusIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
    <path d="M12 5v14M5 12h14" stroke="#3D63FF" strokeWidth="2.2" strokeLinecap="round" />
  </svg>
);

export const SearchIcon = () => (
  <svg width="42" height="42" viewBox="0 0 24 24" fill="none">
    <circle cx="11" cy="11" r="7" stroke="#3D63FF" strokeWidth="2" />
    <path d="M21 21l-4.35-4.35" stroke="#3D63FF" strokeWidth="2" strokeLinecap="round" />
  </svg>
);

export const VoiceBarsIcon = () => (
  <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
    <rect x="12" y="16" width="7" height="20" rx="3.5" fill="white" opacity="0.92" />
    <rect x="21" y="9" width="7" height="27" rx="3.5" fill="white" />
    <rect x="30" y="16" width="7" height="20" rx="3.5" fill="white" opacity="0.92" />
  </svg>
);

export const SparkleIcon = () => (
  <svg width="44" height="44" viewBox="0 0 44 44" fill="none">
    <path d="M22 4c1.8 8.2 4.8 12.2 13 14-8.2 1.8-11.2 5.8-13 14-1.8-8.2-4.8-12.2-13-14 8.2-1.8 11.2-5.8 13-14z" fill="url(#sparkleMain)" />
    <path d="M34 27c.8 3.3 2.1 4.8 5 5.5-2.9.7-4.2 2.2-5 5.5-.8-3.3-2.1-4.8-5-5.5 2.9-.7 4.2-2.2 5-5.5z" fill="#9A7BFF" opacity="0.9" />
    <path d="M10 29c.5 2.1 1.4 3.1 3.5 3.6-2.1.5-3 1.5-3.5 3.6-.5-2.1-1.4-3.1-3.5-3.6 2.1-.5 3-1.5 3.5-3.6z" fill="#6E8CFF" opacity="0.8" />
    <defs>
      <linearGradient id="sparkleMain" x1="11" y1="8" x2="32" y2="30" gradientUnits="userSpaceOnUse">
        <stop stopColor="#5F7CFF" />
        <stop offset="0.52" stopColor="#8B55FF" />
        <stop offset="1" stopColor="#C86BFF" />
      </linearGradient>
    </defs>
  </svg>
);

export const ChevronRight = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
    <path d="M9 6l6 6-6 6" stroke="#9AA1B8" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

export const CameraIcon = () => (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
    <path d="M8 7l1.4-2h5.2L16 7h3a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2V9a2 2 0 012-2h3z" stroke="#3D63FF" strokeWidth="1.8" strokeLinejoin="round" />
    <circle cx="12" cy="13" r="3.2" stroke="#3D63FF" strokeWidth="1.8" />
  </svg>
);

export const ImageIcon = () => (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
    <rect x="3" y="5" width="18" height="14" rx="3" stroke="#3D63FF" strokeWidth="1.8" />
    <path d="M7 16l3.5-4 2.5 3 2-2.3L19 16" stroke="#3D63FF" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
    <circle cx="8" cy="9" r="1.2" fill="#3D63FF" />
  </svg>
);

export const FileIcon = () => (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
    <path d="M7 3h7l4 4v14H7V3z" stroke="#7B4DFF" strokeWidth="1.8" strokeLinejoin="round" />
    <path d="M14 3v5h5M9 13h6M9 17h4" stroke="#7B4DFF" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

export const SendArrowIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
    <path d="M12 19V5M6 11l6-6 6 6" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

export const ConfirmTypeIcon = ({ index }: { index: number }) => (
  <div className={`h5-confirm-type h5-confirm-type-${index % 5}`}>
    <span>{['进', '险', '会', '合', '费'][index]}</span>
  </div>
);

export const VoiceSupplementIcon = () => (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
    <rect x="6" y="9" width="3" height="8" rx="1.5" fill="white" opacity="0.9" />
    <rect x="11" y="5" width="3" height="12" rx="1.5" fill="white" />
    <rect x="16" y="9" width="3" height="8" rx="1.5" fill="white" opacity="0.9" />
  </svg>
);

type DrawerIconKey = 'company' | 'account' | 'guide' | 'help' | 'quickReply' | 'voice' | 'privacy' | 'logout';

const drawerIconPaths: Record<DrawerIconKey, React.ReactNode> = {
  company: <><path d="M5 20V6.5A1.5 1.5 0 016.5 5h8A1.5 1.5 0 0116 6.5V20" /><path d="M9 9h3M9 13h3M4 20h16M16 11h1.5A1.5 1.5 0 0119 12.5V20" /></>,
  account: <><path d="M9.5 11.5a3.3 3.3 0 100-6.6 3.3 3.3 0 000 6.6z" /><path d="M4.5 19c.7-3.2 2.5-5 5-5s4.3 1.8 5 5" /><path d="M16 11.8a2.6 2.6 0 10-.7-5.1M16.8 14.2c1.4.7 2.4 2.1 2.8 4.1" /></>,
  guide: <><path d="M6 6.8A2.8 2.8 0 018.8 4h6.4A2.8 2.8 0 0118 6.8v10.4a2.8 2.8 0 01-2.8 2.8H8.8A2.8 2.8 0 016 17.2V6.8z" /><path d="M9 9h6M9 13h4M15.5 17.5l1.5 1.5 3-3" /></>,
  help: <><path d="M6 5.5A2.5 2.5 0 018.5 3H18v16h-9.5A2.5 2.5 0 016 16.5v-11z" /><path d="M6 16.5A2.5 2.5 0 018.5 14H18M10 7.5h4M10 10.5h3" /></>,
  quickReply: <><path d="M5 6.8A2.8 2.8 0 017.8 4h8.4A2.8 2.8 0 0119 6.8v5.4a2.8 2.8 0 01-2.8 2.8H10l-4.5 4v-12.2z" /><path d="M9 8.5h6M9 11.5h4" /></>,
  voice: <><rect x="8" y="4" width="8" height="11" rx="4" /><path d="M5 11.5a7 7 0 0014 0M12 18.5V21M9 21h6" /></>,
  privacy: <><path d="M7 10V8a5 5 0 0110 0v2" /><rect x="5" y="10" width="14" height="10" rx="2.2" /><path d="M12 14v2" /></>,
  logout: <><path d="M10 5H6.8A1.8 1.8 0 005 6.8v10.4A1.8 1.8 0 006.8 19H10" /><path d="M14 8l4 4-4 4M8.5 12H18" /></>,
};

export const DrawerLineIcon = ({ id }: { id: string }) => {
  const iconKey = (id in drawerIconPaths ? id : 'help') as DrawerIconKey;
  return (
    <svg className="h5-drawer-line-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <g stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        {drawerIconPaths[iconKey]}
      </g>
    </svg>
  );
};
