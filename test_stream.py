from app.redis_client import redis_client

def test_ingest_stream():
    """Test adding messages to ingest stream"""
    
    print("=" * 60)
    print("TASK 5: TESTING INGEST STREAM")
    print("=" * 60)
    
    # Test 1: Add text submission to stream
    print("\n1. Adding text submission to stream...")
    app_id = redis_client.generate_id()
    message_id = redis_client.add_to_ingest_stream(
        application_id=app_id,
        submission_type="text",
        content="Tài khoản của bạn sẽ bị khóa"
    )
    print(f"   Added to stream with message ID: {message_id}")
    
    # Test 2: Add screenshot submission
    print("\n2. Adding screenshot submission to stream...")
    app_id2 = redis_client.generate_id()
    message_id2 = redis_client.add_to_ingest_stream(
        application_id=app_id2,
        submission_type="screenshot",
        content="/path/to/screenshot.png"
    )
    print(f"   Added to stream with message ID: {message_id2}")
    
    # Test 3: Check stream length
    print("\n3. Checking stream length...")
    stream_length = redis_client.client.xlen(settings.ingest_stream)
    print(f"   Stream '{settings.ingest_stream}' has {stream_length} messages")
    
    if stream_length >= 2:
        print("   Stream contains our messages!")
    else:
        print("   Stream doesn't have enough messages")
        return False
    
    # Test 4: Read messages from stream
    print("\n4. Reading messages from stream...")
    messages = redis_client.client.xread(
        {settings.ingest_stream: '0'},
        count=10
    )
    
    if messages:
        print(f"   Successfully read {len(messages[0][1])} messages")
        print(f"\n   Sample message:")
        sample = messages[0][1][0]  # First message
        print(f"   ID: {sample[0]}")
        print(f"   Data: {sample[1]}")
    else:
        print("   No messages found")
        return False
    
    print("\n" + "=" * 60)
    print(" ALL INGEST STREAM TESTS PASSED!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    from app.config import settings
    
    try:
        success = test_ingest_stream()
        if not success:
            print("\TESTS FAILED")
            exit(1)
    except Exception as e:
        print(f"\ ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)