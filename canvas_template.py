"""
Canvas API Template - Minimal example to connect and modify a course

This script demonstrates how to:
1. Connect to Canvas using the API
2. Retrieve course information
3. Access course modules
4. Modify course properties (with examples)
"""
import os
from dotenv import load_dotenv
from canvasapi import Canvas

# Load environment variables from .env file
# This keeps credentials out of your code
load_dotenv()

# Retrieve Canvas API credentials from environment variables
CANVAS_URL = os.getenv('CANVAS_URL')
CANVAS_TOKEN = os.getenv('CANVAS_TOKEN')
COURSE_ID_STR = os.getenv('COURSE_ID')

# Validate that all required configuration variables are set
if not all([CANVAS_URL, CANVAS_TOKEN, COURSE_ID_STR]):
    raise ValueError(
        "Missing required environment variables!\n"
        "Please ensure your .env file has:\n"
        "  - CANVAS_URL (e.g., https://your-institution.instructure.com)\n"
        "  - CANVAS_TOKEN (your API token from Canvas Settings)\n"
        "  - COURSE_ID (the course ID number, e.g., 123456)"
    )

# Convert COURSE_ID to integer (after validation)
try:
    COURSE_ID = int(COURSE_ID_STR)
except ValueError:
    raise ValueError(
        f"COURSE_ID must be a number, but got: {COURSE_ID_STR}\n"
        "Please check your .env file and use only digits for COURSE_ID"
    )

# Initialize Canvas API connection
# This creates a connection object that handles all API calls
print(f"\n🔗 Connecting to Canvas: {CANVAS_URL}")
try:
    canvas = Canvas(CANVAS_URL, CANVAS_TOKEN)
except Exception as e:
    print(f"❌ Failed to initialize Canvas connection: {e}")
    print("   Check that CANVAS_URL and CANVAS_TOKEN are correct in your .env file")
    raise

try:
    # Retrieve the course object from Canvas
    print(f"📚 Fetching course {COURSE_ID}...")
    course = canvas.get_course(COURSE_ID)
    
    # Display basic course information
    print(f"\n✅ Successfully connected!")
    print(f"   Course Name: {course.name}")
    print(f"   Course ID: {course.id}")
    
    # ============================================================
    # EXAMPLE: Modify the course name (disabled by default)
    # Uncomment the lines below to try it:
    # ============================================================
    # print("\n📝 Updating course name...")
    # course.update(course={'name': 'New Course Name'})
    # print("✅ Course name updated!")
    
    # ============================================================
    # EXAMPLE: List all course modules
    # This demonstrates how to iterate through Canvas objects
    # ============================================================
    modules = course.get_modules()
    module_list = list(modules)
    print(f"\n📋 Course Content:")
    print(f"   Number of modules: {len(module_list)}")
    
    if module_list:
        print(f"   Module Names:")
        for module in module_list:
            print(f"     - {module.name}")
    else:
        print(f"   (No modules found in this course)")
    
    print(f"\n🎉 Success! Your Canvas API connection is working.")
    print(f"   Next steps: Uncomment examples above or explore the Canvas API docs")
    
except Exception as e:
    print(f"\n❌ Error occurred:")
    print(f"   {e}")
    print(f"\nCommon issues:")
    print(f"   - Invalid COURSE_ID: Check that the course ID exists")
    print(f"   - Invalid token: Your API token may have expired")
    print(f"   - Permission denied: Your account may not have access to this course")
    print(f"\nFor more help, see TROUBLESHOOTING.md")
    raise
