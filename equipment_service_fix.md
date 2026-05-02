# Equipment Service Fix

## Issues Found
1. Service returning 404 - likely deployment issue
2. CORS already configured correctly in settings
3. Missing Procfile for deployment

## Fixes Applied
1. Created Procfile for proper deployment
2. Added sample equipment data management command
3. Verified CORS settings are correct

## Deployment Steps
1. Commit and push the changes
2. Redeploy on Render
3. Run sample data command if needed
4. Test endpoints

## Expected Endpoints
- GET /api/equipements/ - List all equipment
- POST /api/equipements/ - Create new equipment
- PUT /api/equipements/{id}/ - Update equipment
- DELETE /api/equipements/{id}/ - Delete equipment
- POST /api/equipements/{id}/statut/ - Update equipment status
