/* eslint-disable react-refresh/only-export-components -- router module, not a fast-refresh component file */
import { lazy } from 'react';
import { createBrowserRouter, Navigate } from 'react-router-dom';
import { AppLayout } from '@/components/app-layout';

// Code-split each page so the initial bundle stays small.
const PlatesPage = lazy(() => import('@/pages/plates-page'));
const CheckPage = lazy(() => import('@/pages/check-page'));
const NotFoundPage = lazy(() => import('@/pages/not-found-page'));

export const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    children: [
      { index: true, element: <Navigate to="/plates" replace /> },
      { path: 'plates', element: <PlatesPage /> },
      { path: 'check', element: <CheckPage /> },
      { path: '*', element: <NotFoundPage /> },
    ],
  },
]);
