# Building APIs

- API-1: Validate every request and response at the boundary with the shared schema. Never redefine a contract inside the API package; reuse the domain types.
- API-2: Keep the access matrix true for every route: who may call it, and what it returns to each role.
- API-3: Put each failure in the API error map. A client never sees a raw exception.
- API-4: Every procedure has a contract test with fake dependencies. A coverage test fails when a procedure has none.
- API-5: Add or update the request collection (Bruno or the project's tool) for each route.
- API-6: Parameterized queries only. Secrets and auth checks stay server-side.
- API-7: Name routes, types and fields from the project vocabulary (SESSION SE-6).
