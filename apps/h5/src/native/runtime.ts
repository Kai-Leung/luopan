import { App } from '@capacitor/app';
import { Capacitor } from '@capacitor/core';
import { StatusBar, Style } from '@capacitor/status-bar';

export const NATIVE_BACK_EVENT = 'compass:native-back';

export type NativeBackEventDetail = {
  handled: boolean;
};

declare global {
  interface WindowEventMap {
    'compass:native-back': CustomEvent<NativeBackEventDetail>;
  }
}

export async function configureNativeRuntime(): Promise<void> {
  if (!Capacitor.isNativePlatform()) {
    return;
  }

  await Promise.allSettled([
    StatusBar.setStyle({ style: Style.Light }),
    StatusBar.setBackgroundColor({ color: '#F9FAFF' }),
    StatusBar.setOverlaysWebView({ overlay: false }),
  ]);

  await App.addListener('backButton', async ({ canGoBack }) => {
    const detail: NativeBackEventDetail = { handled: false };
    window.dispatchEvent(new CustomEvent(NATIVE_BACK_EVENT, { detail }));
    if (detail.handled) {
      return;
    }
    if (canGoBack) {
      window.history.back();
      return;
    }
    await App.minimizeApp();
  });
}
