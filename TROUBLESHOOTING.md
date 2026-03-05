# Troubleshooting Guide

Having issues? This guide covers common problems beginners encounter.

## Setup Issues

### ❌ "Command not found: python"
**Problem:** Python isn't installed in your environment.

**Solution:**
- If using **Codespaces:** The container automatically includes Python. Wait a few moments and try again, or reload the window (`Ctrl+Shift+P` → "Developer: Reload Window")
- If using **VS Code Desktop:** Ensure your dev container built successfully. Look at the dev container logs for errors

### ❌ "No module named 'canvasapi'"
**Problem:** Dependencies didn't install properly.

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### ❌ "No module named 'dotenv'"
**Problem:** Same as above - missing dependency.

**Solution:**
```bash
pip install python-dotenv
```

---

## Configuration Issues

### ❌ "Missing required environment variables"
**Problem:** The script can't find your Canvas configuration.

**Solution:**
1. Check that `.env` file exists in the project root (not in a subdirectory)
2. Verify the file contains:
   ```
   CANVAS_URL=https://your-institution.instructure.com
   CANVAS_TOKEN=your_token_here
   COURSE_ID=123456
   ```
3. If using **Codespaces secrets**, they might not be loaded. Try:
   - Reloading the window (`Ctrl+Shift+P` → "Developer: Reload Window")
   - Running again after a few seconds

### ❌ "COURSE_ID must be a number"
**Problem:** Your COURSE_ID contains non-numeric characters.

**Solution:**
- Open `.env` and ensure COURSE_ID is just numbers: `COURSE_ID=123456` (not `123456ABC` or `Course123`)
- Don't include quotes or special characters

### ❌ "Error: missing or invalid Canvas URL"
**Problem:** The CANVAS_URL is incorrect or malformed.

**Solution:**
- Your Canvas URL should look like: `https://your-institution.instructure.com`
- Check for typos (common: misspelled institution name)
- Do NOT include trailing slashes: `❌ https://your-institution.instructure.com/` → `✅ https://your-institution.instructure.com`

---

## Connection Issues

### ❌ "Connection refused" or "Failed to connect"
**Problem:** The script can't reach your Canvas server.

**Solution:**
1. Check your internet connection (open a browser, go to your Canvas URL)
2. Verify the URL: `https://your-institution.instructure.com` is accessible
3. Ask your Canvas admin if the Canvas API is enabled for your institution
4. On a corporate network? You might need a VPN - contact your IT department

### ❌ "Invalid API token"
**Problem:** Your Canvas token is invalid, expired, or incorrect.

**Solution:**
1. Log in to Canvas directly to verify your institution URL is correct
2. Create a new API token:
   - Click your profile picture (top right)
   - Go to **Settings**
   - Scroll to **Approved Integrations**
   - Click **New Access Token**
   - Copy the NEW token (you only see it once!)
3. Update your `.env` or Codespaces secret with the new token
4. Try again

### ❌ "Unauthorized" or "Not Found"
**Problem:** Your account doesn't have permission to access this course, or the course ID is wrong.

**Solution:**
1. **Check the Course ID:**
   - Go to your Canvas course
   - Look at the URL: `https://your-institution.instructure.com/courses/123456`
   - The last number is your Course ID (in this example: `123456`)
   - Make sure you're using the correct ID

2. **Check permissions:**
   - Log into Canvas directly
   - Verify you can access the course as a student, instructor, or admin
   - If you can't see it in Canvas, the API token won't help

3. **Verify you're in the course:**
   - Some institutions require enrollment first
   - Ask your Canvas admin if you need special permissions

---

## Script Errors

### ❌ TypeError or AttributeError when running the script
**Problem:** The script encountered an unexpected error structure from Canvas.

**Solution:**
1. Check your Canvas version compatibility:
   ```bash
   pip show canvasapi
   ```
2. Try updating the library:
   ```bash
   pip install --upgrade canvasapi
   ```
3. Check the [canvasapi GitHub issues](https://github.com/ucfopen/canvasapi/issues) for known problems

### ❌ "Timeout" or "Request timed out"
**Problem:** Canvas is taking too long to respond.

**Solution:**
1. Try again in a moment (Canvas might be under maintenance)
2. Check Canvas status page: https://status.instructure.com
3. Check your internet connection
4. Some operations take longer on slow networks - be patient

---

## Codespaces-Specific Issues

### ❌ "Secrets not found" in Codespaces
**Problem:** Your secrets were set up but the script still can't find them.

**Solution:**
1. Verify secrets exist:
   - Go to your GitHub repo → Settings → Secrets and variables → Codespaces
   - Confirm `CANVAS_URL`, `CANVAS_TOKEN`, `CANVAS_ID` are listed
   
2. Reload the Codespace:
   - Close the browser tab with your Codespace
   - Go back to your repo's Code button
   - Create a NEW Codespace (this time it will pick up the secrets)
   - Note: Existing Codespaces won't see NEW secrets automatically

3. Alternative: Use `.env` file
   - Copy `.env.example` to `.env`
   - Add your credentials manually (for testing only - don't commit!)

### ❌ "Dev container failed to build"
**Problem:** The container setup encountered errors.

**Solution:**
1. Check the build log:
   - Look at the "Dev Container" output (might be a tab at the bottom)
   - It will show which step failed
   
2. Rebuild the container:
   - Press `Ctrl+Shift+P`
   - Type "Dev Containers: Rebuild Container"
   - Wait for it to complete
   
3. If that doesn't work:
   - Delete the Codespace: GitHub repo → Codespaces → ⋮ menu → Delete
   - Create a new one

---

## Still Stuck?

### Debugging Steps (in order):

1. **Verify `.env` or secrets are correct:**
   ```bash
   # This ONLY works in Bash, not Python!
   echo $CANVAS_URL
   echo $CANVAS_TOKEN
   echo $COURSE_ID
   ```

2. **Test Canvas connectivity manually:**
   - Open your browser and go to: `https://your-institution.instructure.com`
   - Verify you can log in normally

3. **Enable verbose output** (modify `canvas_template.py`):
   ```python
   # Add after imports
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```
   This will show detailed connection info.

4. **Check Canvas API documentation:**
   - [Canvas API Docs](https://canvas.instructure.com/doc/api/)
   - [canvasapi Library Docs](https://canvasapi.readthedocs.io/)

5. **Ask your Canvas Administrator:**
   - "Is the Canvas API enabled for our institution?"
   - "Do I need special permissions to use the API?"
   - "Is there an IP whitelist I need to be on?"

---

## Common Success Indicators

✅ **When it's working, you'll see:**
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
```

---

## Need More Help?

- **Canvas API Issues:** Check the [Canvas API documentation](https://canvas.instructure.com/doc/api/)
- **canvasapi Library Issues:** Visit [canvasapi GitHub](https://github.com/ucfopen/canvasapi)
- **This template:** Open an issue on the repository
- **Canvas Support:** Contact your Canvas administrator or Instructure support
