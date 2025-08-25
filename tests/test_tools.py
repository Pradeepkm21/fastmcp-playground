from app import _ping, _whoami, _time_now, _health_check


def test_ping_says_pong():
    """Test: Does ping return 'pong'?"""
    result = _ping()
    
    assert result["message"] == "pong"
    print("Ping says pong!")


def test_ping_has_timestamp():
    """Test: Does ping include a timestamp?"""
    result = _ping()
    
    assert "timestamp" in result
    print("Ping has timestamp!")


def test_ping_is_successful():
    """Test: Does ping show success?"""
    result = _ping()
    
    assert result["status"] == "success"
    print("Ping is successful!")


def test_whoami_has_hostname():
    """Test: Does whoami return a hostname?"""
    result = _whoami()
    
    assert "hostname" in result
    assert result["hostname"] != ""
    print("Whoami has hostname!")


def test_whoami_has_platform():
    """Test: Does whoami tell us the platform?"""
    result = _whoami()
    
    assert "platform" in result
    assert result["platform"] != ""
    print("Whoami has platform!")


def test_time_now_utc_works():
    """Test: Does time_now work with UTC?"""
    result = _time_now("UTC")
    
    assert result["status"] == "success"
    assert result["timezone"] == "UTC"
    print("Time_now works with UTC!")


def test_time_now_rejects_bad_timezone():
    """Test: Does time_now reject invalid timezone?"""
    result = _time_now("INVALID")
    
    assert result["status"] == "failed"
    assert "error" in result
    print("Time_now rejects bad timezone!")


def test_health_check_says_healthy():
    """Test: Does health check say we're healthy?"""
    result = _health_check()
    
    assert result["status"] == "healthy"
    print("Health check says healthy!")


def test_health_check_has_version():
    """Test: Does health check include version?"""
    result = _health_check()
    
    assert "version" in result
    assert result["version"] != ""
    print("Health check has version!")


if __name__ == "__main__":
    print("Running All Tests...")
    print("=" * 30)
    
    # Run each test and see results
    test_ping_says_pong()
    test_ping_has_timestamp()
    test_ping_is_successful()
    test_whoami_has_hostname()
    test_whoami_has_platform()
    test_time_now_utc_works()
    test_time_now_rejects_bad_timezone()
    test_health_check_says_healthy()
    test_health_check_has_version()
    
    print("=" * 30)
    print("All simple tests passed!")
