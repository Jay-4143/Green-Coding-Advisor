# MongoDB Atlas Setup Guide

This guide will walk you through setting up MongoDB Atlas for the Green Coding Advisor project.

## Step 1: Create MongoDB Atlas Account

1. Go to [https://www.mongodb.com/cloud/atlas/register](https://www.mongodb.com/cloud/atlas/register)
2. Sign up with Google, GitHub, or email
3. Complete the account setup

## Step 2: Create a Free Cluster

1. After logging in, click **"Build a Database"**
2. Choose the **FREE** tier (M0 - Shared)
3. Select your preferred **Cloud Provider** (AWS, Google Cloud, or Azure)
4. Choose a **Region** closest to your location
5. Leave **Cluster Name** as default (e.g., "Cluster0") or customize it
6. Click **"Create"** (takes 1-3 minutes)

## Step 3: Create Database User

1. In the left sidebar, click **"Database Access"**
2. Click **"Add New Database User"**
3. Choose **"Password"** as authentication method
4. Enter a username (e.g., `green_coding_user`)
5. Click **"Autogenerate Secure Password"** or create your own strong password
   - **IMPORTANT**: Copy and save this password! You'll need it for the connection string.
6. Under **"Database User Privileges"**, select **"Atlas admin"** (or "Read and write to any database")
7. Click **"Add User"**

## Step 4: Configure Network Access

1. In the left sidebar, click **"Network Access"**
2. Click **"Add IP Address"**
3. For development/testing:
   - Click **"Allow Access from Anywhere"** (adds `0.0.0.0/0`)
   - **OR** click **"Add Current IP Address"** to only allow your current IP
4. Click **"Confirm"**

> **Security Note**: For production, restrict IP access to only your server's IP address.

## Step 5: Get Connection String

1. In the left sidebar, click **"Database"**
2. Click **"Connect"** button on your cluster
3. Choose **"Connect your application"**
4. Select:
   - **Driver**: Python
   - **Version**: 3.11 or later
5. Copy the connection string. It will look like:
   ```
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

## Step 6: Configure Your Project

1. Copy `.env.example` to `.env` in the `backend` directory:
   ```bash
   cd backend
   cp .env.example .env
   ```

2. Open `.env` and update the MongoDB connection string:
   ```env
   MONGODB_URI=mongodb+srv://green_coding_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/green_coding?retryWrites=true&w=majority
   MONGODB_DB=green_coding
   ```

   **Important**: 
   - Replace `<username>` with your database username
   - Replace `<password>` with your database password (URL encode special characters if needed)
   - Replace `<cluster-url>` with your actual cluster URL
   - Add `/green_coding` before the `?` to specify the database name

3. Update other settings as needed (JWT secret key, email, etc.)

## Step 7: Test Connection

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the backend server:
   ```bash
   python start_server.py
   ```

3. Check the logs - you should see:
   ```
   Connecting to MongoDB...
   Default badges initialized
   ```

4. If you see connection errors, verify:
   - Your IP address is whitelisted in Network Access
   - Username and password are correct
   - Connection string format is correct

## Troubleshooting

### Connection Timeout
- Check that your IP is whitelisted in Network Access
- Verify firewall isn't blocking MongoDB ports

### Authentication Failed
- Double-check username and password
- Ensure password doesn't contain special characters that need URL encoding
- Try regenerating the password in Atlas

### Database Not Found
- The database will be created automatically on first use
- Verify `MONGODB_DB=green_coding` is set correctly

### URL Encoding Special Characters
If your password contains special characters, URL encode them:
- `@` → `%40`
- `#` → `%23`
- `$` → `%24`
- `%` → `%25`
- `&` → `%26`
- `+` → `%2B`
- `=` → `%3D`

Example: If password is `P@ssw0rd#123`, use `P%40ssw0rd%23123` in the connection string.

## Next Steps

Once connected, the application will:
- Automatically create collections (`users`, `submissions`, `teams`, `projects`, `badges`, etc.)
- Initialize default badges on first startup
- Start accepting API requests

Your MongoDB Atlas setup is complete! 🎉

