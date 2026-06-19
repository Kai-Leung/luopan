export const COMPASS_NATIVE_BACK_EVENT = 'compass:native-back' as const;

export interface CompassNativeBackEventDetail {
  handled: boolean;
}

export type CompassNativeCapability =
  | 'camera'
  | 'file_picker'
  | 'microphone'
  | 'back_button'
  | 'safe_area';

export interface CompassNativeRuntimeInfo {
  platform: 'web' | 'android' | 'ios';
  capabilities: CompassNativeCapability[];
}
