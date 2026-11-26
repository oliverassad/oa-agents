# Databases and storage

- DB-1: Emulators or throwaway databases only. Never the dev or production database from an agent.
- DB-2: A database constraint over application code where the store supports it.
- DB-3: Relational store: a schema change ships a migration and its test. Schemaless store: a shape change ships a backfill, not a migration.
- DB-4: Parameterized queries only. No string-built SQL.
- DB-5: Every seeding path checks that the target is a throwaway store before its first write.
- DB-6: Integration tests prove the database contract; a unit test does not.
