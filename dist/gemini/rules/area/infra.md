# Infrastructure as code

- IN-1: Terraform (or the project's tool) only. No click-ops; a console change is imported or reverted.
- IN-2: Before a handover: `terraform fmt -check -recursive`, then `init -backend=false` and `validate` for each changed stack.
- IN-3: Plan runs in CI. An agent never runs `apply` against a shared environment; the operator applies.
- IN-4: Remote state only. Never commit state, plans with secrets, or `.tfvars` with secrets.
- IN-5: An import block adopts an existing resource. `destroy` of a stateful resource is a decision (GIT GS-8).
- IN-6: Least privilege for every role and key. Name the variable, never the secret.
