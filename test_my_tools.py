from app import _ping, _whoami, _time_now, _health_check
import json

def test_tools():
    print("Testing MCP Tools")
    print("=" * 30)

    # Test ping
    print("\n1. Testing ping():")
    result = _ping()
    print(json.dumps(result, indent=2))

    # Test whoami
    print("\n2. Testing whoami():")
    result = _whoami()
    print(json.dumps(result, indent=2))

    # Test time_now with valid timezone
    print("\n3. Testing time_now() with IST:")
    result = _time_now("IST")
    print(json.dumps(result, indent=2))

    # Test time_now with different timezone
    print("\n4. Testing time_now() with UTC:")
    result = _time_now("UTC")
    print(json.dumps(result, indent=2))

    # Test health_check
    print("\n5. Testing health_check():")
    result = _health_check()
    print(json.dumps(result, indent=2))

    print("\n All tools working!")

if __name__ == "__main__":
    test_tools()
