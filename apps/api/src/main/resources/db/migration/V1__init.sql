create table core_region (
    id char(36) primary key,
    street varchar(255),
    city varchar(255) not null,
    state varchar(255),
    country varchar(255)
);

create table core_activity (
    id char(36) primary key,
    region_id char(36) not null,
    name varchar(255) not null,
    description text,
    image_url varchar(2048),
    categories_csv varchar(1024) not null,
    schedule_type varchar(50),
    created_at timestamp,
    updated_at timestamp,
    constraint fk_core_activity_region foreign key (region_id) references core_region(id)
);

create table core_platform (
    id char(36) primary key,
    code varchar(32) not null unique,
    name varchar(255) not null,
    homepage_url varchar(2048) not null,
    enabled boolean not null default true
);

create table core_venue (
    id char(36) primary key,
    name varchar(255) not null,
    address_json text,
    timezone varchar(100),
    description text
);

create table core_ticket_type (
    id char(36) primary key,
    activity_id char(36) not null,
    title varchar(255) not null,
    name varchar(255) not null,
    description text,
    base_price decimal(10,2),
    constraint fk_core_tt_activity foreign key (activity_id) references core_activity(id)
);

create table core_schedule (
    id char(36) primary key,
    activity_id char(36) not null,
    venue_id char(36),
    ticket_type_id char(36),
    start_date date not null,
    selling_start timestamp,
    selling_end timestamp,
    max_pax integer,
    constraint fk_core_schedule_activity foreign key (activity_id) references core_activity(id),
    constraint fk_core_schedule_venue foreign key (venue_id) references core_venue(id),
    constraint fk_core_schedule_ticket_type foreign key (ticket_type_id) references core_ticket_type(id)
);

create table core_offer (
    id char(36) primary key,
    activity_id char(36) not null,
    platform_id char(36) not null,
    schedule_id char(36),
    ticket_type_id char(36),
    currency_code varchar(3) not null,
    base_price decimal(10,2) not null,
    fee_amount decimal(10,2) not null,
    discount_amount decimal(10,2) not null,
    affiliate_url varchar(2048) not null,
    availability integer not null,
    last_seen_at timestamp not null,
    constraint fk_core_offer_activity foreign key (activity_id) references core_activity(id),
    constraint fk_core_offer_platform foreign key (platform_id) references core_platform(id),
    constraint fk_core_offer_schedule foreign key (schedule_id) references core_schedule(id),
    constraint fk_core_offer_ticket_type foreign key (ticket_type_id) references core_ticket_type(id)
);

create table mualba_canonical_activity (
    id char(36) primary key,
    slug varchar(128) not null unique,
    name varchar(255) not null,
    canonical_category varchar(128) not null,
    status varchar(32) not null,
    created_at timestamp
);

create table source_raw_offer (
    id char(36) primary key,
    source varchar(64) not null,
    source_offer_id varchar(255) not null,
    source_activity_id varchar(255) not null,
    idempotency_key varchar(255) not null unique,
    payload_json text not null,
    observed_at timestamp not null
);

create table source_activity_map (
    id char(36) primary key,
    source varchar(64) not null,
    source_activity_id varchar(255) not null,
    core_activity_id char(36),
    mualba_activity_id char(36),
    constraint fk_source_map_core_activity foreign key (core_activity_id) references core_activity(id),
    constraint fk_source_map_mualba_activity foreign key (mualba_activity_id) references mualba_canonical_activity(id)
);

insert into core_region (id, street, city, state, country) values
('550e8400-e29b-41d4-a716-446655440001', '11 W 53rd St', 'New York', 'NY', 'USA'),
('550e8400-e29b-41d4-a716-446655440002', '200 Central Park W', 'New York', 'NY', 'USA'),
('550e8400-e29b-41d4-a716-446655440003', '111 S Michigan Ave', 'Chicago', 'IL', 'USA');

insert into core_activity (id, region_id, name, description, image_url, categories_csv, schedule_type, created_at, updated_at) values
('660e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440001', 'Museum of Modern Art (MoMA)', 'Modern and contemporary art museum in NYC.', 'https://images.musepicker.com/moma.jpg', 'Museums & Galleries,Art', 'Day-based', current_timestamp, current_timestamp),
('660e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440002', 'American Museum of Natural History', 'Iconic natural history museum in NYC.', 'https://images.musepicker.com/amnh.jpg', 'Museums & Galleries,Kids Activities', 'Day-based', current_timestamp, current_timestamp),
('660e8400-e29b-41d4-a716-446655440003', '550e8400-e29b-41d4-a716-446655440003', 'The Art Institute of Chicago', 'World-class museum in Chicago.', 'https://images.musepicker.com/aic.jpg', 'Museums & Galleries,Art', 'Day-based', current_timestamp, current_timestamp);

insert into core_platform (id, code, name, homepage_url, enabled) values
('880e8400-e29b-41d4-a716-446655440001', 'KLOOK', 'Klook', 'https://www.klook.com', true),
('880e8400-e29b-41d4-a716-446655440002', 'VIATOR', 'Viator', 'https://www.viator.com', true),
('880e8400-e29b-41d4-a716-446655440003', 'TRIPCOM', 'Trip.com', 'https://www.trip.com', true),
('880e8400-e29b-41d4-a716-446655440004', 'TICKETSTODO', 'TicketsToDo', 'https://www.ticketstodo.com', true);

insert into core_ticket_type (id, activity_id, title, name, description, base_price) values
('770e8400-e29b-41d4-a716-446655440001', '660e8400-e29b-41d4-a716-446655440001', 'General Admission', 'Adult', 'General admission adult ticket.', 30.00),
('770e8400-e29b-41d4-a716-446655440002', '660e8400-e29b-41d4-a716-446655440002', 'General Admission', 'Adult', 'General admission adult ticket.', 28.00),
('770e8400-e29b-41d4-a716-446655440003', '660e8400-e29b-41d4-a716-446655440003', 'Fast Pass', 'Adult', 'Fast pass adult ticket.', 32.00);

insert into core_schedule (id, activity_id, venue_id, ticket_type_id, start_date, selling_start, selling_end, max_pax) values
('990e8400-e29b-41d4-a716-446655440001', '660e8400-e29b-41d4-a716-446655440001', null, '770e8400-e29b-41d4-a716-446655440001', '2026-04-10', current_timestamp, current_timestamp, 9),
('990e8400-e29b-41d4-a716-446655440002', '660e8400-e29b-41d4-a716-446655440002', null, '770e8400-e29b-41d4-a716-446655440002', '2026-04-10', current_timestamp, current_timestamp, 9),
('990e8400-e29b-41d4-a716-446655440003', '660e8400-e29b-41d4-a716-446655440003', null, '770e8400-e29b-41d4-a716-446655440003', '2026-04-11', current_timestamp, current_timestamp, 6);

insert into core_offer (id, activity_id, platform_id, schedule_id, ticket_type_id, currency_code, base_price, fee_amount, discount_amount, affiliate_url, availability, last_seen_at) values
('100e8400-e29b-41d4-a716-446655440001', '660e8400-e29b-41d4-a716-446655440001', '880e8400-e29b-41d4-a716-446655440001', '990e8400-e29b-41d4-a716-446655440001', '770e8400-e29b-41d4-a716-446655440001', 'USD', 31.50, 1.00, 2.00, 'https://www.klook.com/activity/moma?aid=musepicker', 999, current_timestamp),
('100e8400-e29b-41d4-a716-446655440002', '660e8400-e29b-41d4-a716-446655440001', '880e8400-e29b-41d4-a716-446655440002', '990e8400-e29b-41d4-a716-446655440001', '770e8400-e29b-41d4-a716-446655440001', 'USD', 33.00, 0.00, 3.00, 'https://www.viator.com/tours/moma?aid=musepicker', 999, current_timestamp),
('100e8400-e29b-41d4-a716-446655440003', '660e8400-e29b-41d4-a716-446655440002', '880e8400-e29b-41d4-a716-446655440003', '990e8400-e29b-41d4-a716-446655440002', '770e8400-e29b-41d4-a716-446655440002', 'USD', 29.00, 0.50, 1.00, 'https://www.trip.com/attraction/amnh?aid=musepicker', 999, current_timestamp),
('100e8400-e29b-41d4-a716-446655440004', '660e8400-e29b-41d4-a716-446655440002', '880e8400-e29b-41d4-a716-446655440004', '990e8400-e29b-41d4-a716-446655440002', '770e8400-e29b-41d4-a716-446655440002', 'USD', 27.50, 1.50, 0.00, 'https://www.ticketstodo.com/amnh?aid=musepicker', 999, current_timestamp),
('100e8400-e29b-41d4-a716-446655440005', '660e8400-e29b-41d4-a716-446655440003', '880e8400-e29b-41d4-a716-446655440001', '990e8400-e29b-41d4-a716-446655440003', '770e8400-e29b-41d4-a716-446655440003', 'USD', 32.10, 0.00, 0.10, 'https://www.klook.com/activity/aic?aid=musepicker', 999, current_timestamp);

insert into mualba_canonical_activity (id, slug, name, canonical_category, status, created_at) values
('aa0e8400-e29b-41d4-a716-446655440001', 'moma-general-admission', 'Museum of Modern Art General Admission', 'museum', 'draft', current_timestamp);
