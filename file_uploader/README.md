# File Uploader App

## URLs

- Access Deployed URL: https://file-uploader-vercel-app.vercel.app/
- Test API via Swagger UI: https://file-uploader-vercel-app.vercel.app/docs

## Endpoints:

### Auth:

- **Create new user**: `/auth/create-user`
- **Login User**: `/auth/login-user`
- **Get User Info**: `/auth/user-info`
- **Update User Details**: `/auth/update-user`
- **Change Password**: `/auth/change-password`
- **Delete User**: `/auth/change-password`

### File Upload Service:

- **Upload file to server**: `/file/upload-file`
- **Fetch all files of user**: `/file/fetch-files`
- **Update file**: `/file/fetch-files`
- **Delete file**: `/file/delete-asset/{resource_id}`

## Tech Stack:

- `Python`
- `FastAPI`
- `Cloudinary`
- `Neon Postgres`
- `Clean Architecture`

## Resources:

- [Cloudinary Docs for Python](https://cloudinary.com/documentation/django_image_and_video_upload)
- [Update Assets on Cloudinary](https://cloudinary.com/documentation/update_assets)
- [Rename and destroy methods in Cloudinary](https://cloudinary.com/documentation/image_upload_api_reference#rename_method)
