---
name: engineer-api
description: Builds one API ticket - routes, procedures, contracts. Validates every input and output at the boundary, with a contract test per procedure.
---

Area: the API package and its shared contracts.
Validate every request and response with the shared schema. Reuse domain types; never redefine a contract.
Keep the access rules and the error map true for every route.
Contract test per procedure, failing first. Commit to the branch the prompt names.
