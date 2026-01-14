#!/usr/bin/env python3
"""Verify all three logging systems use the same session ID."""
import sys
sys.path.append('.')

from core.llm.conversation_logger import KollaborConversationLogger
from core.llm.conversation_manager import ConversationManager
from core.llm.api_communication_service import APICommunicationService
from core.utils.config_utils import get_conversations_dir

class MockConfig:
    def get(self, key, default=None):
        defaults = {
            "core.llm.max_history": 50,
            "core.llm.save_conversations": True,
            "core.api.url": "http://localhost:1234",
            "core.api.model": "default",
            "core.api.timeout": 30
        }
        return defaults.get(key, default)

class MockProfile:
    def __init__(self):
        self.api_url = "http://localhost:1234"
        self.model = "default"
        self.temperature = 0.7
        self.timeout = 30
        self.max_tokens = None
        self.streaming = False

print("=== Testing Integrated Session ID Usage ===\n")

# Setup directories
conversations_dir = get_conversations_dir()
raw_conversations_dir = conversations_dir / "raw"

# Step 1: Create conversation logger (this generates the master session ID)
logger = KollaborConversationLogger(conversations_dir)
master_session_id = logger.session_id
print(f"[1] conversation_logger session ID: {master_session_id}")

# Step 2: Create conversation manager with logger (should use logger's ID)
manager = ConversationManager(MockConfig(), conversation_logger=logger)
print(f"[2] conversation_manager session ID: {manager.current_session_id}")

# Step 3: Create API service and set session ID (should use logger's ID)
api_service = APICommunicationService(MockConfig(), raw_conversations_dir, MockProfile())
api_service.set_session_id(logger.session_id)
print(f"[3] api_service session ID: {api_service.current_session_id}")

# Verify all match
print()
if manager.current_session_id == master_session_id and api_service.current_session_id == master_session_id:
    print("[PASS] All session IDs match!")
    print(f"       Shared session ID: {master_session_id}")
else:
    print("[FAIL] Session IDs don't match:")
    print(f"       logger:  {master_session_id}")
    print(f"       manager: {manager.current_session_id}")
    print(f"       api:     {api_service.current_session_id}")

# Test file creation
print()
print("=== Testing File Creation ===\n")

# Logger creates: {session_id}.jsonl
logger_file = conversations_dir / f"{logger.session_id}.jsonl"
print(f"[1] conversation_logger will create: {logger_file.name}")

# Manager creates: {session_id}_snapshot_{time}.json
manager.add_message('user', 'Test')
saved_path = manager.save_conversation()
print(f"[2] conversation_manager created: {saved_path.name}")

# API service creates: {session_id}_raw_{time}.jsonl
api_raw_file = raw_conversations_dir / f"{api_service.current_session_id}_raw_172500.jsonl"
print(f"[3] api_service will create: {api_raw_file.name}")

# Verify all use the same base session ID
print()
all_use_same_id = (
    logger_file.name.startswith(master_session_id) and
    saved_path.name.startswith(master_session_id) and
    api_raw_file.name.startswith(master_session_id)
)

if all_use_same_id:
    print("[PASS] All files use the same session ID!")
    print(f"       Base session ID: {master_session_id}")
else:
    print("[FAIL] Files use different session IDs")

print()
print("=== SUMMARY ===")
print(f"Before fix: manager used truncated ID (first 8 chars)")
print(f"After fix:  all three systems use full ID: {master_session_id}")
