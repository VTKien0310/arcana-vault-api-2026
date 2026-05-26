INSERT INTO keys (user_id, value, channels, expiration, email, telegram_chat_id, phone)
VALUES (gen_random_uuid(),
        '12345678',
        '{0, 1, 2}',
        now() + interval '30 days',
        'user@example.com',
        '123456789',
        '+1234567890');