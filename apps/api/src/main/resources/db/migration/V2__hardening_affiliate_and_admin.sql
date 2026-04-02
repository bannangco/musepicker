create table core_affiliate_click (
    click_id char(36) primary key,
    offer_id char(36) not null,
    platform_code varchar(32) not null,
    target_url varchar(2048) not null,
    request_id varchar(64) not null,
    referrer varchar(2048),
    user_agent varchar(1024),
    created_at timestamp not null,
    constraint fk_aff_click_offer foreign key (offer_id) references core_offer(id)
);

create table source_dead_letter (
    id char(36) primary key,
    source varchar(64) not null,
    payload_json text not null,
    reason varchar(512) not null,
    run_id varchar(64) not null,
    created_at timestamp not null
);

create table source_replay_event (
    id char(36) primary key,
    source varchar(64) not null,
    run_id varchar(64) not null,
    replay_reason varchar(255) not null,
    replayed_at timestamp not null
);

alter table source_activity_map
    add constraint uq_source_activity_map unique (source, source_activity_id);

alter table source_activity_map
    add column confidence_score decimal(5,4) default 0.0000;

alter table source_activity_map
    add column manual_override boolean default false;

create index idx_core_activity_region_name on core_activity(region_id, name);
create index idx_core_schedule_activity_date on core_schedule(activity_id, start_date);
create index idx_core_offer_activity_last_seen on core_offer(activity_id, last_seen_at);
create index idx_core_offer_platform on core_offer(platform_id);
create index idx_source_raw_offer_source_observed on source_raw_offer(source, observed_at);
create index idx_source_dead_letter_source_created on source_dead_letter(source, created_at);
create index idx_affiliate_click_offer_created on core_affiliate_click(offer_id, created_at);
