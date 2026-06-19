import React, { useRef } from 'react';
import { ChevronRight, DrawerLineIcon } from '../icons/H5Icons';

type DrawerMenuGroup = {
  title: string;
  items: Array<{ id: string; label: string; disabledWhenSingleCompany?: boolean }>;
};

export function SideDrawer({
  open,
  onClose,
  onNavigate,
  onLogout,
  profile,
  menuGroups,
}: {
  open: boolean;
  onClose: () => void;
  onNavigate: (id: string, label: string, disabled?: boolean) => void;
  onLogout: () => void;
  profile: { name: string; role: string; companyCount: number };
  menuGroups: DrawerMenuGroup[];
}) {
  const startX = useRef(0);
  const visibleGroups = Array.isArray(menuGroups) ? menuGroups : [];
  return (
    <div className={`h5-drawer-layer ${open ? 'h5-drawer-open' : ''}`} aria-hidden={!open}>
      <button className="h5-drawer-mask" onClick={onClose} aria-label="关闭侧边菜单" />
      <aside
        className="h5-side-drawer"
        aria-label="侧边抽屉菜单"
        onTouchStart={(event) => { startX.current = event.touches[0].clientX; }}
        onTouchEnd={(event) => { if (startX.current - event.changedTouches[0].clientX > 56) onClose(); }}
      >
        <button className="h5-profile-card" onClick={() => onNavigate('profile', '个人资料编辑')}>
          <div className="h5-profile-avatar">张</div>
          <div className="h5-profile-copy">
            <strong>{profile.name}</strong>
            <span>{profile.role}</span>
          </div>
          <ChevronRight />
        </button>
        <div className="h5-drawer-scroll">
          {visibleGroups.map((group) => (
            <section className="h5-drawer-group" key={group.title}>
              <h3>{group.title}</h3>
              <div className="h5-drawer-items">
                {(Array.isArray(group.items) ? group.items : []).map((item) => {
                  const disabled = Boolean(item.disabledWhenSingleCompany && profile.companyCount <= 1);
                  return (
                    <button className={`h5-drawer-item ${disabled ? 'h5-drawer-item-disabled' : ''}`} key={item.id} onClick={() => onNavigate(item.id, item.label, disabled)}>
                      <span className="h5-drawer-icon"><DrawerLineIcon id={item.id} /></span>
                      <span>{item.label}</span>
                      <ChevronRight />
                    </button>
                  );
                })}
              </div>
            </section>
          ))}
        </div>
        <button className="h5-drawer-logout" onClick={onLogout}>
          <span className="h5-drawer-icon"><DrawerLineIcon id="logout" /></span>
          <span>退出登录</span>
        </button>
      </aside>
    </div>
  );
}
