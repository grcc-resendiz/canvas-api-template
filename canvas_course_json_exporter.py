"""
Canvas Course JSON Exporter

This script demonstrates how to:
1. Connect to Canvas using the API
2. Retrieve course information
3. Retrieve modules and module items
4. Retrieve pages, assignments, discussions, quizzes, and files
5. Retrieve the questions inside every quiz: New Quizzes (items, choices,
   and correct answers) and Classic Quizzes
6. Save the course content to a JSON file

Version log:
  1.0  original exporter
  1.1  (2026-10-03) adds "new_quizzes": every New Quiz with its settings and all
       of its questions (item_body, answer choices, scoring/correct answer),
       read through the New Quizzes API (/api/quiz/v1/...). Also adds the
       questions inside Classic Quizzes under each quiz's "questions" key.
       Question banks referenced from a New Quiz can't be read through this API;
       those entries are kept and flagged rather than skipped silently.

This script is read-only. It does not modify the Canvas course.
"""

import json
import os
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any

import requests
from canvasapi import Canvas
from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

CANVAS_URL = os.getenv("CANVAS_URL")
CANVAS_TOKEN = os.getenv("CANVAS_TOKEN")
COURSE_ID_STR = os.getenv("COURSE_ID")


# ============================================================
# VALIDATE CONFIGURATION
# ============================================================

if not all([CANVAS_URL, CANVAS_TOKEN, COURSE_ID_STR]):
    raise ValueError(
        "Missing required environment variables!\n"
        "Please ensure your .env file has:\n"
        "  - CANVAS_URL (e.g., https://your-institution.instructure.com)\n"
        "  - CANVAS_TOKEN (your Canvas API token)\n"
        "  - COURSE_ID (the Canvas course ID, e.g., 123456)"
    )

try:
    COURSE_ID = int(COURSE_ID_STR)
except ValueError as error:
    raise ValueError(
        f"COURSE_ID must be a number, but got: {COURSE_ID_STR}\n"
        "Please check your .env file and use only digits for COURSE_ID."
    ) from error


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def make_json_safe(value: Any) -> Any:
    """
    Recursively convert values into formats that json.dump() can save.

    CanvasAPI objects may contain dates, nested objects, or internal
    requester properties that should not appear in the JSON file.
    """

    if value is None or isinstance(value, (str, int, float, bool)):
        return value

    if isinstance(value, (datetime, date)):
        return value.isoformat()

    if isinstance(value, dict):
        return {
            str(key): make_json_safe(item)
            for key, item in value.items()
            if not str(key).startswith("_")
        }

    if isinstance(value, (list, tuple, set)):
        return [make_json_safe(item) for item in value]

    if hasattr(value, "__dict__"):
        return {
            key: make_json_safe(item)
            for key, item in vars(value).items()
            if not key.startswith("_")
        }

    return str(value)


def canvas_object_to_dict(canvas_object: Any) -> dict:
    """
    Convert a CanvasAPI object into a regular Python dictionary.
    """

    if canvas_object is None:
        return {}

    return make_json_safe(vars(canvas_object))


def create_safe_filename(name: str) -> str:
    """
    Remove characters that may cause problems in filenames.
    """

    safe_name = re.sub(r'[<>:"/\\|?*]', "", name)
    safe_name = re.sub(r"\s+", "_", safe_name.strip())

    return safe_name or f"canvas_course_{COURSE_ID}"


def retrieve_collection(label: str, retrieval_function, errors: list) -> list:
    """
    Retrieve a Canvas collection without stopping the entire export
    when one content category is unavailable.
    """

    print(f"   Retrieving {label}...")

    try:
        collection = list(retrieval_function())
        print(f"      Found: {len(collection)}")
        return collection

    except Exception as error:
        error_message = f"Could not retrieve {label}: {error}"
        errors.append(error_message)
        print(f"      ⚠️ {error_message}")
        return []


def new_quizzes_get_all(path: str) -> list:
    """
    GET every page of a New Quizzes API endpoint (read-only).
    New Quizzes live outside the classic Canvas API, so canvasapi
    doesn't cover them; this uses plain HTTP with the same token.
    """

    url = f"{CANVAS_URL.rstrip('/')}/api/quiz/v1/courses/{COURSE_ID}{path}"
    headers = {"Authorization": f"Bearer {CANVAS_TOKEN}"}
    results = []

    while url:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list):
            results.extend(data)
        elif isinstance(data, dict):
            results.append(data)

        url = response.links.get("next", {}).get("url")

    return results


def summarize_new_quiz_item(item: dict) -> dict:
    """
    Add a readable "summary" next to the raw item: question text, each
    choice's text, and which choice is correct. The raw item is kept in
    full, so nothing is lost.
    """

    entry = item.get("entry") or {}
    summary = {
        "position": item.get("position"),
        "points_possible": item.get("points_possible"),
        "entry_type": item.get("entry_type"),
        "question_type": entry.get("interaction_type_slug"),
        "question_text": re.sub(r"<[^>]+>", " ", entry.get("item_body") or "").split(),
        "choices": [],
        "correct_choice_ids": []
    }
    summary["question_text"] = " ".join(summary["question_text"])

    if item.get("entry_type") == "Bank":
        summary["note"] = (
            "This item points to a question bank. Its questions can't be read "
            "through the New Quizzes API; use a Common Cartridge export instead."
        )
        return summary

    choices = (entry.get("interaction_data") or {}).get("choices") or []
    for choice in choices:
        body = choice.get("itemBody") or choice.get("item_body") or ""
        summary["choices"].append({
            "id": choice.get("id"),
            "position": choice.get("position"),
            "text": " ".join(re.sub(r"<[^>]+>", " ", body).split())
        })

    value = (entry.get("scoring_data") or {}).get("value")
    if isinstance(value, list):
        summary["correct_choice_ids"] = value
    elif value is not None:
        summary["correct_choice_ids"] = [value]

    for choice in summary["choices"]:
        choice["correct"] = choice["id"] in summary["correct_choice_ids"]

    return summary


# ============================================================
# CONNECT TO CANVAS
# ============================================================

print(f"\n🔗 Connecting to Canvas: {CANVAS_URL}")

try:
    canvas = Canvas(CANVAS_URL, CANVAS_TOKEN)
except Exception as error:
    print(f"❌ Failed to initialize Canvas connection: {error}")
    print("   Check CANVAS_URL and CANVAS_TOKEN in your .env file.")
    raise


# ============================================================
# RETRIEVE AND EXPORT COURSE CONTENT
# ============================================================

try:
    print(f"📚 Fetching course {COURSE_ID}...")

    course = canvas.get_course(
        COURSE_ID,
        include=["syllabus_body", "term", "teachers"]
    )

    print("\n✅ Successfully connected!")
    print(f"   Course Name: {course.name}")
    print(f"   Course ID: {course.id}")

    export_errors = []

    course_export = {
        "export_information": {
            "exported_at": datetime.now().astimezone().isoformat(),
            "canvas_url": CANVAS_URL,
            "course_id": COURSE_ID,
            "export_format_version": "1.1",
            "notes": [
                "This export contains course content available through the Canvas API.",
                "Course file entries contain file metadata and download URLs, not binary file contents.",
                "Student submissions, grades, and enrollment records are not included.",
                "New Quizzes and their questions are under 'new_quizzes'. Each question keeps the raw API item plus a readable 'summary' with the correct answer marked.",
                "Classic Quiz questions are under each quiz's 'questions' key."
            ]
        },
        "course": canvas_object_to_dict(course),
        "modules": [],
        "pages": [],
        "assignments": [],
        "assignment_groups": [],
        "discussions": [],
        "quizzes": [],
        "new_quizzes": [],
        "files": [],
        "errors": export_errors
    }

    print("\n📦 Retrieving modules and module items...")

    modules = retrieve_collection(
        "modules",
        course.get_modules,
        export_errors
    )

    for module_number, module in enumerate(modules, start=1):
        print(
            f"   Module {module_number}/{len(modules)}: "
            f"{getattr(module, 'name', 'Untitled Module')}"
        )

        module_data = canvas_object_to_dict(module)
        module_data["items"] = []

        try:
            module_items = list(module.get_module_items())

            for item in module_items:
                module_data["items"].append(
                    canvas_object_to_dict(item)
                )

        except Exception as error:
            error_message = (
                f"Could not retrieve items for module "
                f"'{getattr(module, 'name', module.id)}': {error}"
            )
            export_errors.append(error_message)
            print(f"      ⚠️ {error_message}")

        course_export["modules"].append(module_data)

    print("\n📄 Retrieving course pages...")

    page_summaries = retrieve_collection(
        "pages",
        course.get_pages,
        export_errors
    )

    for page_number, page_summary in enumerate(page_summaries, start=1):
        page_title = getattr(page_summary, "title", "Untitled Page")

        print(
            f"   Page {page_number}/{len(page_summaries)}: "
            f"{page_title}"
        )

        try:
            page_url = getattr(page_summary, "url")
            full_page = course.get_page(page_url)

            course_export["pages"].append(
                canvas_object_to_dict(full_page)
            )

        except Exception as error:
            error_message = (
                f"Could not retrieve full page '{page_title}': {error}"
            )
            export_errors.append(error_message)
            print(f"      ⚠️ {error_message}")

            course_export["pages"].append(
                canvas_object_to_dict(page_summary)
            )

    print("\n📝 Retrieving assignments...")

    assignments = retrieve_collection(
        "assignments",
        course.get_assignments,
        export_errors
    )

    course_export["assignments"] = [
        canvas_object_to_dict(assignment)
        for assignment in assignments
    ]

    print("\n📊 Retrieving assignment groups...")

    assignment_groups = retrieve_collection(
        "assignment groups",
        lambda: course.get_assignment_groups(
            include=["assignments"]
        ),
        export_errors
    )

    course_export["assignment_groups"] = [
        canvas_object_to_dict(group)
        for group in assignment_groups
    ]

    print("\n💬 Retrieving discussion topics...")

    discussions = retrieve_collection(
        "discussion topics",
        course.get_discussion_topics,
        export_errors
    )

    course_export["discussions"] = [
        canvas_object_to_dict(discussion)
        for discussion in discussions
    ]

    print("\n❓ Retrieving Classic Quizzes...")

    quizzes = retrieve_collection(
        "Classic Quizzes",
        course.get_quizzes,
        export_errors
    )

    for quiz in quizzes:
        quiz_data = canvas_object_to_dict(quiz)

        try:
            quiz_data["questions"] = [
                canvas_object_to_dict(question)
                for question in quiz.get_questions()
            ]
        except Exception as error:
            error_message = (
                f"Could not retrieve questions for Classic Quiz "
                f"'{getattr(quiz, 'title', quiz.id)}': {error}"
            )
            export_errors.append(error_message)
            print(f"      ⚠️ {error_message}")
            quiz_data["questions"] = []

        course_export["quizzes"].append(quiz_data)

    print("\n🧩 Retrieving New Quizzes and their questions...")

    try:
        new_quizzes = new_quizzes_get_all("/quizzes")
        print(f"      Found: {len(new_quizzes)}")
    except Exception as error:
        error_message = f"Could not retrieve New Quizzes: {error}"
        export_errors.append(error_message)
        print(f"      ⚠️ {error_message}")
        new_quizzes = []

    for quiz_number, new_quiz in enumerate(new_quizzes, start=1):
        quiz_title = new_quiz.get("title", "Untitled Quiz")
        quiz_id = new_quiz.get("id")
        print(f"   New Quiz {quiz_number}/{len(new_quizzes)}: {quiz_title}")

        try:
            items = new_quizzes_get_all(f"/quizzes/{quiz_id}/items")
            items.sort(key=lambda item: item.get("position") or 0)
            new_quiz["items"] = [
                dict(item, summary=summarize_new_quiz_item(item))
                for item in items
            ]
            print(f"      Questions: {len(items)}")
        except Exception as error:
            error_message = (
                f"Could not retrieve questions for New Quiz '{quiz_title}': {error}"
            )
            export_errors.append(error_message)
            print(f"      ⚠️ {error_message}")
            new_quiz["items"] = []

        course_export["new_quizzes"].append(new_quiz)

    print("\n📁 Retrieving course file metadata...")

    files = retrieve_collection(
        "course files",
        course.get_files,
        export_errors
    )

    course_export["files"] = [
        canvas_object_to_dict(file)
        for file in files
    ]

    export_directory = Path("canvas_exports")
    export_directory.mkdir(parents=True, exist_ok=True)

    safe_course_name = create_safe_filename(course.name)
    export_filename = (
        f"{safe_course_name}_"
        f"{COURSE_ID}_"
        f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    )

    export_path = export_directory / export_filename

    with export_path.open(
        mode="w",
        encoding="utf-8"
    ) as json_file:
        json.dump(
            course_export,
            json_file,
            indent=2,
            ensure_ascii=False
        )

    print("\n" + "=" * 60)
    print("🎉 COURSE EXPORT COMPLETE")
    print("=" * 60)

    print(f"\n📚 Course: {course.name}")
    print(f"🆔 Course ID: {course.id}")
    print(f"📦 Modules: {len(course_export['modules'])}")
    print(f"📄 Pages: {len(course_export['pages'])}")
    print(f"📝 Assignments: {len(course_export['assignments'])}")
    print(f"📊 Assignment Groups: {len(course_export['assignment_groups'])}")
    print(f"💬 Discussions: {len(course_export['discussions'])}")
    print(f"❓ Classic Quizzes: {len(course_export['quizzes'])}")
    print(
        f"🧩 New Quizzes: {len(course_export['new_quizzes'])} "
        f"({sum(len(q.get('items', [])) for q in course_export['new_quizzes'])} questions)"
    )
    print(f"📁 Files: {len(course_export['files'])}")

    print(f"\n💾 JSON file created:")
    print(f"   {export_path.resolve()}")

    if export_errors:
        print(
            f"\n⚠️ Export completed with "
            f"{len(export_errors)} warning(s)."
        )
        print(
            "   Review the 'errors' section near the beginning "
            "of the JSON file."
        )
    else:
        print("\n✅ All requested content was retrieved successfully.")

    print(
        "\n🔒 This was a read-only operation. "
        "No Canvas content was modified."
    )

except Exception as error:
    print("\n❌ The course export could not be completed.")
    print(f"   Error: {error}")

    print("\nCommon issues:")
    print("   - The COURSE_ID does not exist.")
    print("   - The API token has expired.")
    print("   - Your account does not have access to the course.")
    print("   - Your Canvas permissions restrict certain content.")
    print("   - The canvasapi package needs to be installed or updated.")

    print("\nFor more help, see TROUBLESHOOTING.md.")
    raise