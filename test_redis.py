from app.redis_client import redis_client
import json

def test_json_operations():
    """ Test RedisJSON read/write operations"""

    print("\n1. Testing basic JSON write/read")
    test_key = "test:document:1"
    test_data = {
        "id": "test-123",
        "message": "Tài khoản của bạn sẽ bị khoá",
        "timestamp": redis_client.get_timestamp(),
        "status": "pending"
    }

    print(f" Writing to key '{test_key}':")
    print(f" {json.dumps(test_data, indent = 4, ensure_ascii = False)}")
    success = redis_client.json_set(test_key, test_data)
    print(f" Write succesful: {success}")

    print(f"\n Reading from key '{test_key}':")
    retrieved = redis_client.json_get(test_key)
    print(f" {json.dumps(retrieved, indent = 4, ensure_ascii = False)}")

    if retrieved == test_data:
        print(" Data matched!")
    else:
        print(" Data mismatch!")
        return False
    
    print("\n2. Testing read of non-existent key...")
    missing = redis_client.json_get("test:nonexistent")
    if missing is None:
        print(" Correctly returns None for missing key")
    else:
        print(f" Expected None, got: {missing}")
        return False
    
    print("\n3. Testing update of exisiting doc")
    test_data['status'] = 'completed'
    test_data['fraud_score'] = 85
    redis_client.json_set(test_key, test_data)

    updated = redis_client.json_get(test_key)
    if updated['status'] == 'completed' and updated['fraud_score'] == 85:
        print(" Update successful!")
    else:
        print(" Update failed!")
        return False
    
    print("\n4. Testing Vietnamese text")
    vietnamese_data = {
        "id": "vn-test",
        "messages":
        ["Chúc mừng! Bạn đã trúng thưởng 100 triệu",
            "Vui lòng nhấn vào link để nhận quà",
            "Tài khoản sẽ bị khóa trong 24h"]
    }
    redis_client.json_set("test:vietnamese", vietnamese_data)
    vn_retrieved = redis_client.json_get("test:vietnamese")

    if vn_retrieved == vietnamese_data:
        print(" Vietnamese hanled correctly")
        print(f" Messages: {vn_retrieved['messages'][0]}")
    else:
        print(" Vietnamese not handled correctly")
        return False
    
    print("\n5. Testing complex nested structure...")
    complex_data = {
        "id": "app-456",
        "submission": {
            "type": "screenshot",
            "content": "base64encodedimage...",
            "metadata": {
                "source": "sms",
                "phone": "+84901234567"
            }
        },
        "agents": {
            "doc_auth": {
                "status": "completed",
                "score": 90,
                "checks": ["dpi", "metadata", "format"]
            },
            "text_similarity": {
                "status": "pending",
                "score": None
            }
        },
        "timestamps": {
            "created": redis_client.get_timestamp(),
            "updated": redis_client.get_timestamp()
        }
    }

    redis_client.json_set("test:complex", complex_data)
    complex_retrieved = redis_client.json_get("test:complex")

    if complex_retrieved == complex_data:
        print(" Complex structure preserved!")
    else:
        print(" Complex structure corrupted!")
        return False

    print("\n6. Testing multiple documents...")
    for i in range(5):
        doc_id = f"test:batch:{i}"
        doc_data = {
            "id": i,
            "message": f"Test message {i}",
            "timestamp": redis_client.get_timestamp()
        }
        redis_client.json_set(doc_id, doc_data)

    all_exist = True
    for i in range(5):
        doc = redis_client.json_get(f"test:batch:{i}")
        if doc is None or doc['id'] != i:
            all_exist = False
            break
        
    if all_exist:
        print(" All 5 doc stored and retrieved!")
    else:   
        print(" Some docs missing or corrupted")
        return False
        
    print("\n" + "=" * 60)
    print("✅ ALL JSON READ/WRITE TESTS PASSED!")
    print("=" * 60)
    print("\nTest Summary:")
    print("  ✓ Basic read/write")
    print("  ✓ Non-existent key handling")
    print("  ✓ Document updates")
    print("  ✓ Vietnamese text support")
    print("  ✓ Complex nested structures")
    print("  ✓ Multiple document storage")
        
    return True 

if __name__ == "__main__":
    try:
        success = test_json_operations()
        if not success:
            print("\n Tests Failed")
            exit(1)
    
    except Exception as e:
        print(f"\n ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)


    