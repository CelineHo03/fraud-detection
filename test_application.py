from app.redis_client import redis_client
import json

def test_create_application():
    """Test creating application documents"""
    
    print("=" * 60)
    print("TASK 6: TESTING APPLICATION CREATION")
    print("=" * 60)
    
    # Test 1: Create text application
    print("\n1. Creating text application...")
    app_id = redis_client.create_application(
        submission_type="text",
        content="Tài khoản của bạn sẽ bị khóa. Nhấn link: http://fake.com",
        metadata={"source": "sms", "phone": "+84901234567"}
    )
    print(f"   ✅ Created application: {app_id}")
    
    # Test 2: Retrieve and verify application
    print("\n2. Retrieving application from Redis...")
    app_data = redis_client.json_get(f"application:{app_id}")
    
    if app_data:
        print("   ✅ Application retrieved successfully!")
        print(f"\n   Application structure:")
        print(json.dumps(app_data, indent=6, ensure_ascii=False))
    else:
        print("   ❌ Application not found!")
        return False
    
    # Test 3: Verify all required fields
    print("\n3. Verifying application structure...")
    required_fields = [
        "id", "type", "content", "metadata", "status",
        "created_at", "updated_at", "agents", "final_score"
    ]
    
    missing_fields = []
    for field in required_fields:
        if field not in app_data:
            missing_fields.append(field)
    
    if missing_fields:
        print(f"   ❌ Missing fields: {missing_fields}")
        return False
    else:
        print("   ✅ All required fields present!")
    
    # Test 4: Verify agents structure
    print("\n4. Verifying agents structure...")
    if "doc_auth" in app_data["agents"] and "text_similarity" in app_data["agents"]:
        print("   ✅ Both agents initialized!")
        print(f"      - doc_auth status: {app_data['agents']['doc_auth']['status']}")
        print(f"      - text_similarity status: {app_data['agents']['text_similarity']['status']}")
    else:
        print("   ❌ Agents not properly initialized!")
        return False
    
    # Test 5: Verify message added to stream
    print("\n5. Verifying message added to stream...")
    stream_length = redis_client.client.xlen(settings.ingest_stream)
    print(f"   Stream now has {stream_length} message(s)")
    
    # Read last message from stream
    messages = redis_client.client.xrevrange(settings.ingest_stream, count=1)
    if messages:
        last_message = messages[0][1]
        if last_message.get('application_id') == app_id:
            print(f"   ✅ Message added to stream with correct app_id!")
        else:
            print(f"   ❌ Stream message has wrong app_id")
            return False
    else:
        print("   ❌ No messages in stream!")
        return False
    
    # Test 6: Create screenshot application
    print("\n6. Creating screenshot application...")
    app_id2 = redis_client.create_application(
        submission_type="screenshot",
        content="/path/to/screenshot.png",
        metadata={"source": "zalo"}
    )
    print(f"   ✅ Created screenshot application: {app_id2}")
    
    app_data2 = redis_client.json_get(f"application:{app_id2}")
    if app_data2 and app_data2["type"] == "screenshot":
        print("   ✅ Screenshot application structure correct!")
    else:
        print("   ❌ Screenshot application incorrect!")
        return False
    
    print("\n" + "=" * 60)
    print("✅ ALL APPLICATION CREATION TESTS PASSED!")
    print("=" * 60)
    
    print("\nWhat happens when you create an application:")
    print("  1. Generate unique ID")
    print("  2. Create JSON document with full structure")
    print("  3. Store in Redis as 'application:{id}'")
    print("  4. Add to 'fraud:ingest' stream for processing")
    print("  5. Return ID to user immediately")
    
    return True

if __name__ == "__main__":
    from app.config import settings
    
    try:
        success = test_create_application()
        if not success:
            print("\n❌ TESTS FAILED")
            exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)