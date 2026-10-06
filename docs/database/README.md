# Database Schema & Storage Documentation

## Overview

Gesture-AI utilizes PostgreSQL for relational persistence and Redis for low-latency in-memory caching and real-time event streaming.

---

## Relational Schema (PostgreSQL)

Database models are defined using SQLAlchemy 2.0 and versioned with Alembic migrations.

### Core Tables

#### 1. `users`
* `id` (UUID, Primary Key)
* `username` (VARCHAR, Unique, Indexed)
* `email` (VARCHAR, Unique, Indexed)
* `hashed_password` (VARCHAR)
* `is_active` (BOOLEAN, Default: True)
* `created_at` (TIMESTAMP WITH TIME ZONE)
* `updated_at` (TIMESTAMP WITH TIME ZONE)

#### 2. `gestures`
* `id` (UUID, Primary Key)
* `name` (VARCHAR, Unique, Indexed, e.g. "PINCH", "SWIPE_RIGHT")
* `category` (VARCHAR, e.g. "static", "dynamic")
* `description` (TEXT)
* `min_confidence` (FLOAT, Default: 0.80)
* `created_at` (TIMESTAMP WITH TIME ZONE)

#### 3. `action_mappings`
* `id` (UUID, Primary Key)
* `user_id` (UUID, Foreign Key -> `users.id`, Optional)
* `gesture_id` (UUID, Foreign Key -> `gestures.id`)
* `action_type` (VARCHAR, e.g. "MOUSE_CLICK", "MEDIA_NEXT_TRACK", "KEYPRESS")
* `action_payload` (JSONB, configuration parameters for target action)
* `is_enabled` (BOOLEAN, Default: True)
* `cooldown_seconds` (FLOAT, Default: 1.0)
* `created_at` (TIMESTAMP WITH TIME ZONE)
* `updated_at` (TIMESTAMP WITH TIME ZONE)

#### 4. `gesture_history`
* `id` (UUID, Primary Key)
* `session_id` (UUID, Indexed)
* `gesture_id` (UUID, Foreign Key -> `gestures.id`)
* `confidence` (FLOAT)
* `action_executed` (VARCHAR)
* `execution_status` (VARCHAR, e.g. "SUCCESS", "REJECTED_LOW_CONFIDENCE", "COOLDOWN_BLOCKED")
* `created_at` (TIMESTAMP WITH TIME ZONE, Indexed)

---

## Migration Management

Alembic handles schema versioning:

```bash
# Generate new migration
alembic revision --autogenerate -m "create gesture and action tables"

# Apply pending migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1
```
