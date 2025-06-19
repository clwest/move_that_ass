# Authentication API

Example usage with `curl`:

```bash
# Register
curl -X POST http://localhost:8000/auth/register/ \
     -H 'Content-Type: application/json' \
     -d '{"email":"user@example.com","password":"Secret123"}'

# Login
curl -X POST http://localhost:8000/auth/login/ \
     -H 'Content-Type: application/json' \
     -d '{"email":"user@example.com","password":"Secret123"}'

# Refresh Token
curl -X POST http://localhost:8000/auth/token/refresh/ \
     -H 'Content-Type: application/json' \
     -d '{"refresh":"<refresh>"}'

# Get Profile
curl -H "Authorization: Bearer <access>" http://localhost:8000/auth/profile/
```
