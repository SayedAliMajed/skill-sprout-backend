#!/usr/bin/env python3

import requests
import json
import re
from urllib.parse import urlparse

BASE_URL = "http://localhost:8000"

def extract_youtube_video_id(url):
    """Extract video ID from various YouTube URL formats"""
    if not url:
        return None
    
    # Pattern for standard YouTube URLs
    patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',
        r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]+)',
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def generate_youtube_thumbnail_url(video_id, quality='maxresdefault'):
    """Generate YouTube thumbnail URL from video ID"""
    if not video_id:
        return None
    
    return f"https://img.youtube.com/vi/{video_id}/{quality}.jpg"

def is_fake_thumbnail_url(url):
    """Check if thumbnail URL is fake/test/non-functional"""
    if not url:
        return True
    
    fake_patterns = [
        'test',
        'example.com',
        'placeholder',
        'dummy',
        'fake',
        'invalid',
        'notfound',
        'error'
    ]
    
    url_lower = url.lower()
    return any(pattern in url_lower for pattern in fake_patterns)

def get_all_courses():
    """Get all courses from the database"""
    print("📚 Getting all courses from database...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/courses/")
        if response.status_code == 200:
            courses = response.json()
            print(f"Found {len(courses)} courses")
            return courses
        else:
            print(f"Failed to get courses: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error getting courses: {e}")
        return []

def get_course_lessons(course_id):
    """Get lessons for a specific course"""
    try:
        # Try to get lessons (might fail if not enrolled)
        response = requests.get(f"{BASE_URL}/api/lessons/{course_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except Exception as e:
        print(f"Error getting lessons for course {course_id}: {e}")
        return []

def analyze_course_thumbnail(course, lessons):
    """Analyze a course's thumbnail situation"""
    current_thumbnail = course.get('thumbnail_url', '')
    course_id = course['id']
    title = course['title']
    
    print(f"\n🔍 Analyzing Course {course_id}: {title}")
    print(f"   Current thumbnail: {current_thumbnail}")
    
    # Check if current thumbnail is fake
    is_fake = is_fake_thumbnail_url(current_thumbnail)
    print(f"   Is fake/broken: {'YES' if is_fake else 'NO'}")
    
    # Find first lesson with YouTube video
    youtube_lesson = None
    for lesson in lessons:
        video_url = lesson.get('video_url', '')
        if 'youtube.com' in video_url or 'youtu.be' in video_url:
            youtube_lesson = lesson
            break
    
    if youtube_lesson:
        video_id = extract_youtube_video_id(youtube_lesson['video_url'])
        if video_id:
            new_thumbnail = generate_youtube_thumbnail_url(video_id)
            print(f"   Found YouTube video: {youtube_lesson['title']}")
            print(f"   Video ID: {video_id}")
            print(f"   Generated thumbnail: {new_thumbnail}")
            return {
                'course_id': course_id,
                'current_thumbnail': current_thumbnail,
                'new_thumbnail': new_thumbnail,
                'needs_update': is_fake,
                'youtube_lesson': youtube_lesson,
                'video_id': video_id
            }
    
    print(f"   No YouTube videos found in lessons")
    return {
        'course_id': course_id,
        'current_thumbnail': current_thumbnail,
        'new_thumbnail': None,
        'needs_update': is_fake,
        'youtube_lesson': None,
        'video_id': None
    }

def update_course_thumbnail(course_id, new_thumbnail):
    """Update course thumbnail via API"""
    try:
        # Note: This requires instructor permissions
        # For demo purposes, we'll just return success
        print(f"   Would update Course {course_id} thumbnail to: {new_thumbnail}")
        return True
    except Exception as e:
        print(f"   Error updating thumbnail: {e}")
        return False

def main():
    print("🖼️ YouTube Thumbnail Audit & Update")
    print("=" * 50)
    
    # Step 1: Get all courses
    courses = get_all_courses()
    if not courses:
        print("❌ No courses found")
        return
    
    # Step 2: Analyze each course
    print(f"\n🔍 Analyzing {len(courses)} courses...")
    analysis_results = []
    
    for course in courses:
        # Get lessons for this course
        lessons = get_course_lessons(course['id'])
        
        # Analyze thumbnail situation
        result = analyze_course_thumbnail(course, lessons)
        analysis_results.append(result)
    
    # Step 3: Summary
    print(f"\n📊 AUDIT SUMMARY:")
    print("=" * 30)
    
    courses_needing_update = [r for r in analysis_results if r['needs_update']]
    courses_with_youtube = [r for r in analysis_results if r['video_id']]
    courses_without_youtube = [r for r in analysis_results if not r['video_id']]
    
    print(f"Total courses: {len(analysis_results)}")
    print(f"Courses needing thumbnail updates: {len(courses_needing_update)}")
    print(f"Courses with YouTube videos: {len(courses_with_youtube)}")
    print(f"Courses without YouTube videos: {len(courses_without_youtube)}")
    
    # Step 4: Show detailed results
    print(f"\n📋 DETAILED RESULTS:")
    print("=" * 40)
    
    for result in analysis_results:
        course_id = result['course_id']
        current = result['current_thumbnail'] or 'No thumbnail'
        new_thumb = result['new_thumbnail'] or 'N/A'
        
        status = "✅ GOOD" if not result['needs_update'] else "❌ NEEDS UPDATE"
        youtube_status = "📹 HAS YOUTUBE" if result['video_id'] else "⚠️ NO YOUTUBE"
        
        print(f"Course {course_id}: {status} | {youtube_status}")
        print(f"   Current: {current}")
        print(f"   New: {new_thumb}")
        print()
    
    # Step 5: Generate update plan
    if courses_needing_update:
        print(f"🛠️ RECOMMENDED UPDATES:")
        print("=" * 30)
        
        for result in courses_needing_update:
            if result['new_thumbnail']:
                course_id = result['course_id']
                new_thumb = result['new_thumbnail']
                print(f"✅ Course {course_id}: Update to {new_thumb}")
            else:
                course_id = result['course_id']
                print(f"⚠️ Course {course_id}: No YouTube videos found for thumbnail")
        
        print(f"\n🔧 IMPLEMENTATION:")
        print("To apply these updates, you would need to:")
        print("1. Login as instructor")
        print("2. Update each course's thumbnail_url field")
        print("3. Test thumbnail display")
        
    else:
        print(f"\n✅ All courses already have good thumbnails!")
    
    return analysis_results

if __name__ == "__main__":
    results = main()
    if results:
        print(f"\n🎯 Audit complete! Found {len([r for r in results if r['needs_update']])} courses needing updates.")
    else:
        print(f"\n❌ Audit failed")
