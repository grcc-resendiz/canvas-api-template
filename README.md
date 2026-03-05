# Canvas API Template

## 🚀 Quick Start (Recommended)

1. Click **Use this template** on GitHub
2. Create your new repository
3. Open it in **Codespaces**
4. Add your Canvas credentials

   Go to:
   Settings → Secrets and variables → Codespaces

   Create these secrets:

   CANVAS_URL  
   CANVAS_TOKEN  
   COURSE_ID

5. Run the template:

python canvas_template.py

## Prerequisites

- Canvas instance with API access enabled
- API token from your Canvas account

## Full Setup with Detailed Instructions

### 1. Clone or Fork
```bash
git clone <your-repo-url>
cd canvas-api-template
```

### 2. Open in Dev Container

#### Option A: GitHub Codespaces (Easiest - No Local Setup Required)
1. In your repository on GitHub, click the green **Code** button
2. Select **Codespaces** tab
3. Click **Create codespace on main**
4. Wait for the container to build automatically (2-3 minutes)
5. The environment is ready - all dependencies are pre-installed!

#### Option B: VS Code Desktop
1. Open this folder in VS Code on your local machine
2. When prompted, click **"Reopen in Container"** (or press `Ctrl+Shift+P` and search "Dev Containers: Reopen in Container")
3. Wait for the container to build (dependencies will install automatically)

**Codespaces is recommended** - you don't need anything installed locally, just a web browser!

### 3. Configure Environment

#### Option A: Codespaces Secrets (Recommended for Codespaces)
If using GitHub Codespaces, use encrypted secrets for secure credential storage:

1. Go back to your GitHub repo, not in Codespaces. Then do this: → Settings → Secrets and variables → Codespaces
2. Create new secrets:
   - `CANVAS_URL`
   - `CANVAS_TOKEN`
   - `COURSE_ID`
3. The `.env` will read from these automatically (no file needed)

This keeps your credentials secure and encrypted by GitHub.

#### Option B: Local .env file (Quick Start)
```bash
cp .env.example .env
```

Edit `.env` with your Canvas credentials:
```
CANVAS_URL=https://your-institution.instructure.com
CANVAS_TOKEN=your_api_token_here
COURSE_ID=123456
```

### 4. Run the Template
```bash
python canvas_template.py
```

### Expected Output

When you run the script successfully, you should see:
```
🔗 Connecting to Canvas: https://your-institution.instructure.com
📚 Fetching course 123456...

✅ Successfully connected!
   Course Name: Introduction to Python
   Course ID: 123456

📋 Course Content:
   Number of modules: 4
   Module Names:
     - Week 1: Getting Started
     - Week 2: Variables and Types
     - Week 3: Functions
     - Week 4: Projects

🎉 Success! Your Canvas API connection is working.
   Next steps: Uncomment examples above or explore the Canvas API docs
```

**If you see an error instead**, check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for solutions.

## Finding Your Course ID

You need your Canvas course ID to get started. Here's how to find it:

### Method 1: From the URL (Easiest)
1. Go to your Canvas course
2. Look at the URL in your browser
3. Find the number after `/courses/`:
   ```
   https://your-institution.instructure.com/courses/123456/modules
                                                      ^^^^^^
                                                  Course ID
   ```

### Method 2: From Course Settings
1. In Canvas, click **Settings** (bottom left of course menu)
2. Look for **Course ID** displayed on the page
3. Copy the number (just digits, no letters)

### Method 3: From Canvas Admin
If you don't have direct access to the course:
- Ask your Canvas instructor or administrator
- Provide them the course name and they can give you the ID

## Getting Your Canvas API Token

1. Log in to Canvas
2. Click your profile picture (top right) → Settings
3. Scroll to "Approved Integrations"
4. Click "New Access Token"
5. Copy the generated token (you'll only see it once)

## Usage Examples

The template script `canvas_template.py` demonstrates:
- Connecting to Canvas API
- Retrieving course information
- Listing course modules

Extend it by uncommenting examples or adding new functionality.

## Canvas API Documentation

- [Canvas API Docs](https://canvas.instructure.com/doc/api/)
- [canvasapi Python Library](https://canvasapi.readthedocs.io/)

## Troubleshooting

Having issues? Check **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** for solutions to common problems:
- Configuration errors (missing credentials, invalid Course ID)
- Connection issues (can't reach Canvas, invalid token)
- Codespaces-specific problems
- Debugging steps when nothing else works

## Common Operations

### Update Course Name
```python
course.update(course={'name': 'New Name'})
```

### Get Assignments
```python
assignments = course.get_assignments()
```

### Create an Assignment
```python
course.create_assignment({'name': 'New Assignment'})
```

### Get Students
```python
students = course.get_users(enrollment_type=['student'])
```

## Security

Your Canvas API token is a **secret key** that grants full access to your Canvas account. Treat it like a password!

### ✅ Best Practices

#### 1. Secure Storage

**For Codespaces Users (Recommended)**
Use [Codespaces encrypted secrets](https://docs.github.com/en/codespaces/managing-your-codespaces/managing-encrypted-secrets-for-your-codespaces) to store credentials:
- GitHub encrypts secrets server-side with AES-256
- Secrets are only decrypted when your codespace runs
- They never appear in logs, code, or git history
- **This is the most secure option**

**For Local Development**
1. **Keep `.env` out of git** - The `.gitignore` file ensures `.env` is never accidentally committed
2. **Check before each commit** - Run `git status` and verify `.env` doesn't appear
3. **Use `.env` locally only** - Never copy credentials into code files

#### 2. Never Share Your Token

🚫 **Never paste your token in:**
- GitHub issues or pull requests
- Chat applications (Slack, Discord, Teams, etc.)
- Email or forums
- Code comments or documentation
- Stack Overflow or public debugging

If you accidentally expose a token:
1. **Delete it immediately** in Canvas Settings → Approved Integrations
2. Create a new token
3. Update your configuration with the new token
4. If exposed publicly, Canvas admins may want to audit API activity

#### 3. Set Token Expiration

When creating your Canvas API token, set an expiration date:
- Go to Canvas Settings → Approved Integrations
- Longer tokens (1 year) are convenient but riskier
- Shorter tokens (1 month - 3 months) are more secure
- **Recommendation:** Use 3-month tokens and rotate them regularly
- You'll need to create a new token when it expires

#### 4. What to Do If Compromised

If you suspect your token was exposed:
1. **Delete the token immediately** in Canvas → Settings → Approved Integrations → Delete
2. Check Canvas Activity log for suspicious API access
3. Create a new token
4. Update all codespaces, machines, and `.env` files with the new token
5. Inform your Canvas admin if it was used maliciously

#### 5. Environment Variable Safety

This template correctly uses environment variables instead of hardcoded credentials. However:

⚠️ **Don't debug with credentials:**
```python
# ❌ BAD - Never do this:
print(f"Token: {CANVAS_TOKEN}")
print(os.getenv('CANVAS_TOKEN'))

# ✅ GOOD - Debug safely:
print(f"Canvas URL: {CANVAS_URL}")  # Safe to print
print("Successfully connected to Canvas")  # No credentials
```

**Why it matters:** Debug output could end up in logs, screenshots, or shared terminal history.

#### 6. Monitor Canvas Audit Logs

Canvas keeps an audit log of all API access:
- Go to Canvas Admin → Logs → API Access Logs
- You can see when your token was used and what actions were taken
- If you see suspicious activity, delete the token immediately
- Document any unauthorized access for your IT department

#### 7. Forking This Repository

If you fork this template:
- **Verify this original repo never had real credentials committed** (it shouldn't)
- Create your own tokens fresh - don't copy tokens from other projects
- Start with a `.env.example` that has placeholder values
- Each environment (dev, staging, production) should have separate tokens

### ⚠️ Why This Matters

If someone gains your `CANVAS_TOKEN`, they could:
- ✏️ Modify grades and assignments
- 📝 Change course content
- 👥 Add/remove students
- 🗑️ Delete course materials
- 📊 Access sensitive student data
- 💬 Post messages as you

### 🔍 Verification Checklist

Before pushing to GitHub:
```bash
# ✅ Verify .env is NOT in git
git status  # Should NOT show .env

# ✅ Verify .gitignore includes .env
cat .gitignore | grep env

# ✅ Search for hardcoded tokens (should find nothing)
git log --all -p | grep -i "token\|canvas"

# ✅ Check recent commits don't include .env
git log --name-only -n 5 | grep env
```
