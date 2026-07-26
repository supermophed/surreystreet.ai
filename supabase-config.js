// SUPABASE_ANON_KEY below is the sb_publishable_ (client-side / anon) key.
// This is DESIGNED to be public — it is the new Supabase naming for what used
// to be the eyJ...-shaped anon JWT. It is safe to expose in client-side code.
//
// Real security is enforced by Row-Level Security policies defined in
// supabase-setup.sql (see the `clients` and `demos` tables and their
// `public_read` policies).
//
// DO NOT replace this with an sb_secret_ (service_role) key. That key bypasses
// RLS and would be catastrophic in a public repo. The service_role key lives
// only in ~/.config/surrey_street/.env on the local machine.

const SUPABASE_URL = 'https://ezlztgnahdysysyxkveq.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_1A_wa2Y-h-HVkznZ_9Y0vw_TWJND0Xg';
