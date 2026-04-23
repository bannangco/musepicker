update core_schedule
set start_date = '2030-01-10'
where id in (
    '990e8400-e29b-41d4-a716-446655440001',
    '990e8400-e29b-41d4-a716-446655440002'
);

update core_schedule
set start_date = '2030-01-11'
where id = '990e8400-e29b-41d4-a716-446655440003';

update core_offer
set last_seen_at = current_timestamp
where id in (
    '100e8400-e29b-41d4-a716-446655440001',
    '100e8400-e29b-41d4-a716-446655440002',
    '100e8400-e29b-41d4-a716-446655440003',
    '100e8400-e29b-41d4-a716-446655440004',
    '100e8400-e29b-41d4-a716-446655440005'
);

update core_activity
set image_url = 'https://picsum.photos/id/1015/1200/800'
where id = '660e8400-e29b-41d4-a716-446655440001';

update core_activity
set image_url = 'https://picsum.photos/id/1025/1200/800'
where id = '660e8400-e29b-41d4-a716-446655440002';

update core_activity
set image_url = 'https://picsum.photos/id/1031/1200/800'
where id = '660e8400-e29b-41d4-a716-446655440003';
