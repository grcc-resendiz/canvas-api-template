# Canvas API Template

A minimal template project for connecting to the Canvas API and modifying courses. Ready to fork and use in a dev container.

---

# 🚀 Quick Start (Recommended)

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

```bash
python canvas_template.py
```

---

# Prerequisites

- Canvas instance with API access enabled  
- API token from your Canvas account  

---

# Full Setup with Detailed Instructions

## 1. Open in Dev Container

### Option A: GitHub Codespaces (Easiest - No Local Setup Required)

In your repository on GitHub:

1. Click the green **Code** button  
2. Select the **Codespaces** tab  
3. Click **Create codespace on main**  

Wait for the container to build automatically (2–3 minutes).

The environment is ready — all dependencies are pre-installed.

---

### Option B: VS Code Desktop

Open this folder in VS Code on your local machine.

When prompted, click **Reopen in Container**

(or press **Ctrl + Shift + P** and search  
`Dev Containers: Reopen in Container`)

Wait for the container to build (dependencies will install automatically).

Codespaces is recommended — you don't need anything installed locally, just a web browser.

---

# 2. Configure Environment

### Option A: Codespaces Secrets (Recommended for Codespaces)

If using GitHub Codespaces, use encrypted secrets for secure credential storage.

Go to your GitHub repo (not inside Codespaces):

Settings → Secrets and variables → Codespaces

Create new secrets:

CANVAS_URL  
CANVAS_TOKEN  
COURSE_ID  

The `.env` will read from these automatically (no file needed).

This keeps your credentials secure and encrypted by GitHub.

---

### Option B: Local `.env` file (Quick Start)

```bash
cp .env.example .env
```

Edit `.env` with your Canvas credentials:

```
CANVAS_URL=https://your-institution.instructure.com
CANVAS_TOKEN=your_api_token_here
COURSE_ID=123456
```

---

# 3. Run the Template

```bash
python canvas_template.py
```

---

# Expected Output

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

If you see an error instead, check **TROUBLESHOOTING.md** for solutions.

---

# Running Locally (Optional)

If you prefer running the project locally instead of Codespaces:

```bash
git clone <your-repo-url>
cd canvas-api-template
```

Then open the folder in **VS Code** and select:

```
Dev Containers: Reopen in Container
```

Follow the environment configuration steps above.

---

# Finding Your Course ID

You need your Canvas course ID to get started.

## Method 1: From the URL (Easiest)

Go to your Canvas course.

Look at the URL in your browser.

Find the number after `/courses/`

```
https://your-institution.instructure.com/courses/123456/modules
                                                   ^^^^^^
                                               Course ID
```

---

## Method 2: From Course Settings

In Canvas:

1. Click **Settings** (bottom left of course menu)  
2. Look for **Course ID** displayed on the page  
3. Copy the number (digits only)

---

## Method 3: From Canvas Admin

If you don't have direct access to the course:

- Ask your Canvas instructor or administrator  
- Provide the course name and they can give you the ID  

---

# Getting Your Canvas API Token

1. Log in to Canvas  
2. Click your profile picture → **Settings**  
3. Scroll to **Approved Integrations**  
4. Click **New Access Token**  
5. Copy the generated token (you will only see it once)

---

# Usage Examples

The template script `canvas_template.py` demonstrates:

- Connecting to Canvas API  
- Retrieving course information  
- Listing course modules  

Extend it by uncommenting examples or adding new functionality.

---

# Canvas API Documentation

- Canvas API Docs  
- canvasapi Python Library  

---

# Troubleshooting

Having issues?

Check **TROUBLESHOOTING.md** for solutions to common problems:

- Configuration errors (missing credentials, invalid Course ID)  
- Connection issues (can't reach Canvas, invalid token)  
- Codespaces-specific problems  
- Debugging steps when nothing else works  

---

# Common Operations

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

---

# Security

Your Canvas API token is a secret key that grants full access to your Canvas account. Treat it like a password.

---

# ✅ Best Practices

## 1. Secure Storage

### For Codespaces Users (Recommended)

Use Codespaces encrypted secrets to store credentials.

GitHub encrypts secrets server-side with AES-256  
Secrets are only decrypted when your codespace runs  
They never appear in logs, code, or git history  

This is the most secure option.

---

### For Local Development

Keep `.env` out of git — the `.gitignore` file ensures `.env` is never accidentally committed.

Before committing:

```
git status
```

Verify `.env` does not appear.

Use `.env` locally only. Never copy credentials into code files.

---

## 2. Never Share Your Token

🚫 Never paste your token in:

- GitHub issues or pull requests  
- Chat applications (Slack, Discord, Teams, etc.)  
- Email or forums  
- Code comments or documentation  
- Stack Overflow or public debugging  

If you accidentally expose a token:

1. Delete it in Canvas **Settings → Approved Integrations**  
2. Create a new token  
3. Update your configuration  

---

## 3. Set Token Expiration

When creating your Canvas API token, set an expiration date.

Go to:

```
Canvas Settings → Approved Integrations
```

Shorter tokens (1–3 months) are more secure.

Recommendation: rotate tokens every 3 months.

---

## 4. What To Do If Compromised

If you suspect your token was exposed:

1. Delete the token immediately  
2. Check Canvas activity logs for suspicious access  
3. Create a new token  
4. Update all machines and environments  

---

## 5. Environment Variable Safety

This template uses environment variables instead of hardcoded credentials.

⚠️ Never debug with credentials.

Bad:

```python
print(f"Token: {CANVAS_TOKEN}")
print(os.getenv('CANVAS_TOKEN'))
```

Good:

```python
print(f"Canvas URL: {CANVAS_URL}")
print("Successfully connected to Canvas")
```

---

## 6. Monitor Canvas Audit Logs

Canvas keeps an audit log of all API access.

```
Canvas Admin → Logs → API Access Logs
```

If suspicious activity appears, delete the token immediately.

---

## 7. Forking This Repository

If you fork this template:

- Verify this repo never had real credentials committed  
- Generate your own API tokens  
- Start with `.env.example`  

Each environment should use separate tokens.

---

# ⚠️ Why This Matters

If someone gains your `CANVAS_TOKEN`, they could:

- Modify grades and assignments  
- Change course content  
- Add or remove students  
- Delete course materials  
- Access sensitive student data  
- Post messages as you  

---

# 🔍 Verification Checklist

Before pushing to GitHub:

```
# Verify .env is NOT in git
git status

# Verify .gitignore includes .env
cat .gitignore | grep env

# Search for hardcoded tokens
git log --all -p | grep -i "token\|canvas"

# Check recent commits
git log --name-only -n 5 | grep env
```
