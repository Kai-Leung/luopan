import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.compass.mobile',
  appName: '罗盘',
  webDir: '../h5/dist',
  server: {
    androidScheme: 'https',
  },
  plugins: {
    SplashScreen: {
      launchShowDuration: 1000,
      backgroundColor: '#F9FAFFFF',
      showSpinner: false,
    },
    StatusBar: {
      style: 'LIGHT',
      backgroundColor: '#F9FAFFFF',
      overlaysWebView: false,
    },
  },
};

export default config;
