def test_health_reports_postgres_and_redis(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "postgres": "ok", "redis": "ok"}
