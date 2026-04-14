-- ============================================
-- Surrey Street Client Portal — Supabase Setup
-- Run this in the Supabase SQL Editor
-- ============================================

-- 1. Schema
-- ---------

create table clients (
  id         uuid primary key default gen_random_uuid(),
  name       text not null,
  slug       text unique not null,
  created_at timestamptz default now()
);

create table demos (
  id          uuid primary key default gen_random_uuid(),
  client_slug text not null references clients(slug),
  title       text not null,
  description text,
  file_path   text not null,
  sort_order  int default 0,
  created_at  timestamptz default now()
);

-- 2. Row-Level Security
-- ---------------------

alter table clients enable row level security;
alter table demos   enable row level security;

create policy "public_read" on clients
  for select using (true);

create policy "public_read" on demos
  for select using (true);

-- 3. Seed Data
-- ------------

insert into clients (name, slug)
values ('MessagePay', 'messagepay');

insert into demos (client_slug, title, description, file_path, sort_order)
values
  (
    'messagepay',
    'RCS Notifications Demo',
    'Interactive RCS messaging notification flows for borrower communications',
    '/demos/messagepay/MessagePay_RCS_Notifications_Demo.html',
    1
  ),
  (
    'messagepay',
    'Borrower Scheduled Payments Demo',
    'Interactive borrower portal with scheduled payment management and autopay flows',
    '/demos/messagepay/MessagePay_Borrower_Scheduled_Payments_Demo.html',
    2
  ),
  (
    'messagepay',
    'Storyline Demo',
    'End-to-end product storyline walkthrough for MessagePay',
    '/demos/messagepay/MessagePay_Storyline_Demo.html',
    3
  ),
  (
    'messagepay',
    'Admin Dashboard',
    'Borrower Resolution Layer for credit union ops managers with AI mode, My Queue, and portfolio intelligence',
    '/demos/messagepay/MessagePay_Admin_Dashboard.html',
    4
  );
