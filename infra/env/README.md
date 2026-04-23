# Production Env Templates

Use these templates on the OCI host:

```bash
cp infra/env/db.prod.env.example infra/env/db.prod.env
cp infra/env/api.prod.env.example infra/env/api.prod.env
cp infra/env/caddy.prod.env.example infra/env/caddy.prod.env
```

Do not commit real `*.env` files.
