INSERT INTO arcana_vault.keys (id, user_id, value, channels, expiration, email, telegram_chat_id, phone, created_at,
                               updated_at)
VALUES ('0709270f-8288-4ed3-89f3-63a92689b65f',
        '7eecd02a-316f-42ac-8dae-48db22d2b6eb',
        '12345678',
        '{0, 1, 2}',
        now() + interval '30 days',
        'user@example.com',
        '123456789',
        '+1234567890',
        now(),
        now());