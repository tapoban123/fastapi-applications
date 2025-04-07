# Contacts Manager Application with Authentication

- `Deployed URL`: https://contacts-vercel-app.vercel.app/

- `Test the URL via Swagger UI`: https://contacts-vercel-app.vercel.app/docs/

## Endpoints:

### Home

- **Home**: `/`

### Auth:

- **Create User:** `/auth/create-user`
- **Login User:** `/auth/login`
- **Authenticate User:** `/auth/login`
- **Delete User:** `/auth/delete-user`

### Contacts Services:

- **Create contact:** `/contacts/create`
- **Update contact:** `/contacts/update`
- **Fetch contacts:** `/contacts/fetch-contacts`
- **Delete contact:** `/contacts/delete`

## Resources:

- [Learn about `check_same_thread:false`](https://docs.python.org/3/library/sqlite3.html#sqlite3.threadsafety)
- [FastAPI Docs for Authentication using JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#hash-and-verify-the-passwords)
- [JWT Encode and Decode](https://pyjwt.readthedocs.io/en/stable/usage.html#encoding-decoding-tokens-with-hs256)
- [Handling Multiple Features](https://fastapi.tiangolo.com/tutorial/bigger-applications/#how-relative-imports-work)