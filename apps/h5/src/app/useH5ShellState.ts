import { useCallback, useRef, useState } from 'react';

export function useH5ShellState() {
  const [uploadOpen, setUploadOpen] = useState(false);
  const [pendingOpen, setPendingOpen] = useState(false);
  const [todoOpen, setTodoOpen] = useState(false);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [logoutConfirmOpen, setLogoutConfirmOpen] = useState(false);
  const [factQueryOpen, setFactQueryOpen] = useState(false);
  const touchStartX = useRef(999);

  const openUpload = useCallback(() => setUploadOpen(true), []);
  const closeUpload = useCallback(() => setUploadOpen(false), []);
  const toggleUpload = useCallback(() => setUploadOpen((open) => !open), []);
  const openPending = useCallback(() => setPendingOpen(true), []);
  const closePending = useCallback(() => setPendingOpen(false), []);
  const openTodo = useCallback(() => setTodoOpen(true), []);
  const closeTodo = useCallback(() => setTodoOpen(false), []);
  const openDrawer = useCallback(() => setDrawerOpen(true), []);
  const closeDrawer = useCallback(() => setDrawerOpen(false), []);
  const openLogoutConfirm = useCallback(() => setLogoutConfirmOpen(true), []);
  const closeLogoutConfirm = useCallback(() => setLogoutConfirmOpen(false), []);
  const openFactQuery = useCallback(() => setFactQueryOpen(true), []);
  const closeFactQuery = useCallback(() => setFactQueryOpen(false), []);
  const onShellTouchStart = useCallback((clientX: number) => {
    if (clientX <= 20) touchStartX.current = clientX;
  }, []);
  const onShellTouchEnd = useCallback((clientX: number) => {
    if (touchStartX.current <= 20 && clientX - touchStartX.current > 64) {
      setDrawerOpen(true);
    }
    touchStartX.current = 999;
  }, []);

  return {
    uploadOpen,
    pendingOpen,
    todoOpen,
    drawerOpen,
    logoutConfirmOpen,
    factQueryOpen,
    openUpload,
    closeUpload,
    toggleUpload,
    openPending,
    closePending,
    openTodo,
    closeTodo,
    openDrawer,
    closeDrawer,
    openLogoutConfirm,
    closeLogoutConfirm,
    openFactQuery,
    closeFactQuery,
    onShellTouchStart,
    onShellTouchEnd,
  };
}
