# Deferred Firebase Initialization

## Problem
Firebase initialization during startup is causing the service to hang.

## Solution
Moved Firebase initialization to be deferred until first API call.

## Changes
- Firebase now initializes only when endpoints are called
- Service starts immediately with mock data ready
- Real Firebase data loads on first request
- Prevents startup hanging completely

This should eliminate all timeout issues while maintaining real data access.
