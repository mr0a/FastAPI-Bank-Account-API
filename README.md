## RestAPI with FastAPI
### Description
- An RestAPI to create User account and collect personal information to open a bank account.

### Steps to deploy or run locally
- `pip install -r requirements.txt`
- `uvicorn app:app` to run the api locally
- Open [localhost](http://localhost:8000/docs) to view the api docs.

### API Paths
- `/user` - Post data to create a account with first name, last name and mobile number with country code.
- `/user/verify` - Send the user id and otp code to verify the account with post method.
- `/user` - Use PUT method to send basic user details to the backend.
