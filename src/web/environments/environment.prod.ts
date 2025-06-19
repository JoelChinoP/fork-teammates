import { config } from './config';

/**
 * Environment variables for production mode.
 */
export const environment: any = {
  ...config,
  production: true,
  backendUrl: 'https://cigarra-teammates.appspot.com',
  frontendUrl: 'https://cigarra-teammates.appspot.com',
  withCredentials: false,
};
