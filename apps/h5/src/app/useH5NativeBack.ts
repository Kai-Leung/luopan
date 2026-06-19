import { useEffect } from 'react';
import type { InteractionPromptState } from '../modules/input_flow/h5Interaction';
import { safeAddEventListener, safeGetHistoryState, safePushState } from '../utils/browserSafe';

type UseH5NativeBackOptions = {
  drawerOpen: boolean;
  factQueryOpen: boolean;
  interactionPrompt: InteractionPromptState;
  logoutConfirmOpen: boolean;
  pendingOpen: boolean;
  todoOpen: boolean;
  uploadOpen: boolean;
  closeDrawer: () => void;
  closeFactQuery: () => void;
  closeInteractionPrompt: () => void;
  closeLogoutConfirm: () => void;
  closePending: () => void;
  closeTodo: () => void;
  closeUpload: () => void;
};

export function useH5NativeBack(options: UseH5NativeBackOptions) {
  useEffect(() => safeAddEventListener('keydown', (event) => {
    if (event.key === 'Escape') options.closeDrawer();
  }), [options.closeDrawer]);

  useEffect(() => safeAddEventListener('compass:native-back', (event) => {
    if (options.logoutConfirmOpen) options.closeLogoutConfirm();
    else if (options.interactionPrompt) options.closeInteractionPrompt();
    else if (options.factQueryOpen) options.closeFactQuery();
    else if (options.pendingOpen) options.closePending();
    else if (options.todoOpen) options.closeTodo();
    else if (options.uploadOpen) options.closeUpload();
    else if (options.drawerOpen) options.closeDrawer();
    else return;
    event.detail.handled = true;
  }), [
    options.drawerOpen,
    options.factQueryOpen,
    options.interactionPrompt,
    options.logoutConfirmOpen,
    options.pendingOpen,
    options.todoOpen,
    options.uploadOpen,
    options.closeDrawer,
    options.closeFactQuery,
    options.closeInteractionPrompt,
    options.closeLogoutConfirm,
    options.closePending,
    options.closeTodo,
    options.closeUpload,
  ]);

  useEffect(() => {
    if (!options.drawerOpen) return;
    const state = { ...(safeGetHistoryState() as Record<string, unknown> || {}), h5Drawer: true };
    safePushState(state, '');
    return safeAddEventListener('popstate', options.closeDrawer, { once: true });
  }, [options.drawerOpen, options.closeDrawer]);
}
