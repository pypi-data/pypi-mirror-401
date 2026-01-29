"""Sample data fixtures for FastMCP Feedback tests."""

from datetime import datetime, timedelta
from typing import List, Dict, Any


def get_sample_feedback_data() -> Dict[str, Any]:
    """Get a single sample feedback item."""
    return {
        "type": "bug",
        "title": "Application crashes on startup",
        "description": "The app crashes immediately after launching on iOS 17",
        "submitter": "test_user",
        "contact_info": "test@example.com"
    }


def get_multiple_feedback_data() -> List[Dict[str, Any]]:
    """Get multiple sample feedback items with different types."""
    return [
        {
            "type": "bug",
            "title": "Login button broken",
            "description": "Cannot click login button",
            "submitter": "user1",
            "contact_info": "user1@test.com"
        },
        {
            "type": "feature", 
            "title": "Add dark mode",
            "description": "Please add dark mode support",
            "submitter": "user2",
            "contact_info": "user2@test.com"
        },
        {
            "type": "improvement",
            "title": "Faster loading",
            "description": "App loads slowly on older devices",
            "submitter": "user3"
        }
    ]


def get_large_feedback_dataset(count: int = 100) -> List[Dict[str, Any]]:
    """Generate a large dataset of feedback items for performance testing."""
    feedback_types = ["bug", "feature", "improvement", "question"]
    feedback_data = []
    
    for i in range(count):
        feedback_type = feedback_types[i % len(feedback_types)]
        
        feedback_item = {
            "type": feedback_type,
            "title": f"{feedback_type.title()} #{i+1}: Sample {feedback_type} report",
            "description": f"This is a sample {feedback_type} report generated for testing purposes. "
                          f"Item number {i+1} in the test dataset. "
                          f"Contains enough text to test various scenarios and edge cases.",
            "submitter": f"test_user_{i+1}",
        }
        
        # Add contact info for some items
        if i % 3 == 0:
            feedback_item["contact_info"] = f"user{i+1}@testdomain.com"
            
        feedback_data.append(feedback_item)
    
    return feedback_data


def get_unicode_feedback_data() -> List[Dict[str, Any]]:
    """Get feedback data with unicode characters for internationalization testing."""
    return [
        {
            "type": "bug", 
            "title": "支持中文输入法",
            "description": "希望应用能够支持中文输入法，包括拼音、五笔等输入方式。目前在输入中文时会出现乱码。",
            "submitter": "中文用户",
            "contact_info": "chinese.user@example.com"
        },
        {
            "type": "feature",
            "title": "Añadir soporte para español",
            "description": "Por favor añadir soporte completo para el idioma español, incluyendo la interfaz de usuario y mensajes de error.",
            "submitter": "usuario_español",
            "contact_info": "spanish.user@ejemplo.com"
        },
        {
            "type": "improvement", 
            "title": "Amélioration des performances",
            "description": "L'application pourrait être plus rapide lors du démarrage. Actuellement, il faut attendre environ 10 secondes.",
            "submitter": "utilisateur_français"
        },
        {
            "type": "bug",
            "title": "Проблема с кодировкой",
            "description": "При вводе русского текста отображаются неправильные символы. Необходимо исправить кодировку UTF-8.",
            "submitter": "русский_пользователь",
            "contact_info": "russian.user@пример.рф"
        },
        {
            "type": "feature",
            "title": "🚀 Add emoji support 😊",
            "description": "It would be great to support emojis in feedback! 🎉 Users love expressing themselves with emojis 💯",
            "submitter": "emoji_lover_🎭",
            "contact_info": "emoji@example.com"
        }
    ]


def get_edge_case_feedback_data() -> List[Dict[str, Any]]:
    """Get feedback data for testing edge cases."""
    return [
        {
            "type": "bug",
            "title": "A" * 255,  # Maximum title length
            "description": "Short description",
            "submitter": "edge_case_user"
        },
        {
            "type": "feature", 
            "title": "Short title",
            "description": "X" * 10000,  # Maximum description length
            "submitter": "long_description_user"
        },
        {
            "type": "improvement",
            "title": "Special characters: @#$%^&*()[]{}|\\:;\"'<>?/~`",
            "description": "Testing with special characters in title and description: !@#$%^&*()_+-={}[]|\\:;\"'<>?,./ and more symbols",
            "submitter": "special_chars_user@domain-with-dashes.co.uk"
        },
        {
            "type": "question",
            "title": "Minimum viable feedback",
            "description": "X",  # Minimum description length
            "submitter": "minimal_user"
        },
        {
            "type": "bug",
            "title": "Feedback with very long email",
            "description": "Testing feedback with extremely long contact email address",
            "submitter": "user_with_long_name_for_testing",
            "contact_info": "very.long.email.address.for.testing.purposes@extremely.long.domain.name.example.com"
        }
    ]


def get_status_transition_data() -> List[Dict[str, Any]]:
    """Get data for testing status transitions."""
    base_time = datetime.utcnow()
    
    return [
        {
            "feedback_data": {
                "type": "bug",
                "title": "Critical login issue",
                "description": "Users cannot log into the application",
                "submitter": "critical_reporter"
            },
            "status_transitions": [
                {"status": "open", "timestamp": base_time, "note": "Issue reported"},
                {"status": "in_progress", "timestamp": base_time + timedelta(hours=1), "note": "Started investigation"},
                {"status": "resolved", "timestamp": base_time + timedelta(hours=6), "note": "Fixed authentication service"},
                {"status": "closed", "timestamp": base_time + timedelta(days=1), "note": "Verified fix in production"}
            ]
        },
        {
            "feedback_data": {
                "type": "feature",
                "title": "Add export functionality",
                "description": "Users want to export their data",
                "submitter": "feature_requester"
            },
            "status_transitions": [
                {"status": "open", "timestamp": base_time, "note": "Feature request submitted"},
                {"status": "in_progress", "timestamp": base_time + timedelta(days=3), "note": "Added to sprint backlog"},
                {"status": "resolved", "timestamp": base_time + timedelta(weeks=2), "note": "Export feature implemented"}
            ]
        }
    ]


def get_analytics_test_data() -> List[Dict[str, Any]]:
    """Get data for testing analytics and insights functionality."""
    base_time = datetime.utcnow()
    
    analytics_events = []
    
    # Simulate a week of feedback activity
    for day in range(7):
        day_time = base_time - timedelta(days=day)
        
        # Different activity patterns for each day
        if day < 2:  # Recent days - higher activity
            submissions_per_day = 15
        elif day < 5:  # Mid-week - moderate activity
            submissions_per_day = 8
        else:  # Older days - lower activity
            submissions_per_day = 3
            
        for i in range(submissions_per_day):
            event_time = day_time + timedelta(hours=i % 24)
            
            feedback_types = ["bug", "feature", "improvement", "question"]
            feedback_type = feedback_types[i % len(feedback_types)]
            
            analytics_events.append({
                "timestamp": event_time,
                "event_type": "feedback_submitted",
                "data": {
                    "type": feedback_type,
                    "has_contact": i % 3 == 0,  # 1/3 have contact info
                    "title_length": 20 + (i % 50),  # Varying title lengths
                    "description_length": 100 + (i % 400),  # Varying description lengths
                    "source": "api" if i % 2 == 0 else "web"
                }
            })
            
            # Some feedback gets status updates
            if i % 4 == 0:  # 1/4 get updated
                analytics_events.append({
                    "timestamp": event_time + timedelta(hours=2),
                    "event_type": "feedback_status_updated",
                    "data": {
                        "from_status": "open",
                        "to_status": "in_progress",
                        "type": feedback_type
                    }
                })
                
                # Some get resolved
                if i % 8 == 0:  # 1/8 get resolved
                    analytics_events.append({
                        "timestamp": event_time + timedelta(hours=24),
                        "event_type": "feedback_status_updated", 
                        "data": {
                            "from_status": "in_progress",
                            "to_status": "resolved",
                            "type": feedback_type,
                            "resolution_time_hours": 24
                        }
                    })
    
    return analytics_events


def get_performance_test_data(count: int = 1000) -> List[Dict[str, Any]]:
    """Generate large dataset for performance testing."""
    return [
        {
            "type": ["bug", "feature", "improvement", "question"][i % 4],
            "title": f"Performance test item {i+1}",
            "description": f"This is performance test feedback item number {i+1}. " * 3,  # Make it reasonably long
            "submitter": f"perf_user_{(i % 100) + 1}",  # 100 different users
            "contact_info": f"perf_user_{(i % 100) + 1}@performance.test" if i % 5 == 0 else None
        }
        for i in range(count)
    ]


def get_concurrent_test_data(num_threads: int = 10, items_per_thread: int = 10) -> List[List[Dict[str, Any]]]:
    """Generate data for concurrent operation testing."""
    threads_data = []
    
    for thread_id in range(num_threads):
        thread_data = []
        
        for item_id in range(items_per_thread):
            feedback_item = {
                "type": ["bug", "feature"][item_id % 2],
                "title": f"Thread {thread_id} item {item_id}",
                "description": f"Concurrent test feedback from thread {thread_id}, item {item_id}",
                "submitter": f"thread_{thread_id}_user_{item_id}"
            }
            thread_data.append(feedback_item)
            
        threads_data.append(thread_data)
    
    return threads_data


def get_search_test_data() -> List[Dict[str, Any]]:
    """Get data for testing search and filtering functionality."""
    return [
        {
            "type": "bug",
            "title": "Critical database connection error",
            "description": "Database connection fails randomly causing application crashes",
            "submitter": "db_admin",
            "contact_info": "admin@company.com"
        },
        {
            "type": "bug", 
            "title": "Minor UI alignment issue",
            "description": "Button alignment is slightly off in the header",
            "submitter": "ui_designer",
            "contact_info": "design@company.com"
        },
        {
            "type": "feature",
            "title": "Add database backup functionality", 
            "description": "Need automated database backup feature for data protection",
            "submitter": "system_admin",
            "contact_info": "sysadmin@company.com"
        },
        {
            "type": "feature",
            "title": "Implement real-time notifications",
            "description": "Users want real-time push notifications for important updates",
            "submitter": "product_manager"
        },
        {
            "type": "improvement",
            "title": "Optimize database query performance",
            "description": "Some database queries are running slowly and need optimization",
            "submitter": "performance_engineer",
            "contact_info": "perf@company.com"
        },
        {
            "type": "question",
            "title": "How to configure database settings?",
            "description": "Need guidance on optimal database configuration for production",
            "submitter": "new_developer"
        }
    ]


# Utility functions for test data

def create_feedback_with_timestamps(feedback_data: Dict[str, Any], 
                                   created_at: datetime = None,
                                   updated_at: datetime = None) -> Dict[str, Any]:
    """Add timestamp fields to feedback data."""
    result = feedback_data.copy()
    result["created_at"] = created_at or datetime.utcnow()
    result["updated_at"] = updated_at or result["created_at"]
    return result


def create_feedback_with_status(feedback_data: Dict[str, Any],
                               status: str = "open") -> Dict[str, Any]:
    """Add status field to feedback data."""
    result = feedback_data.copy()
    result["status"] = status
    return result


def create_feedback_with_id(feedback_data: Dict[str, Any],
                           feedback_id: str = None) -> Dict[str, Any]:
    """Add ID field to feedback data."""
    result = feedback_data.copy()
    result["id"] = feedback_id or f"test_id_{hash(str(feedback_data)) % 10000}"
    return result


def mask_sensitive_data(feedback_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create version of feedback data with sensitive information masked for analytics."""
    result = {
        "type": feedback_data["type"],
        "title_length": len(feedback_data["title"]),
        "description_length": len(feedback_data["description"]),
        "has_contact": "contact_info" in feedback_data and feedback_data["contact_info"] is not None,
        "submitter_hash": hash(feedback_data["submitter"]) % 10000
    }
    return result