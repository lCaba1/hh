class TestAPI:
    def test_read_root(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Добро пожаловать в систему управления скачками!"}

    def test_get_nonexistent_owner(self, client):
        response = client.get("/owners/999")
        assert response.status_code == 404
        assert "message" in response.json()

    def test_create_owner(self, client, sample_owner_data: dict):
        response = client.post("/owners/", json=sample_owner_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == sample_owner_data["name"]
        assert "id" in data

    def test_create_jockey(self, client, sample_jockey_data: dict):
        response = client.post("/jockeys/", json=sample_jockey_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == sample_jockey_data["name"]
        assert "id" in data

    def test_get_owners_empty(self, client):
        response = client.get("/owners/")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_horses_empty(self, client):
        response = client.get("/horses/")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_jockeys_empty(self, client):
        response = client.get("/jockeys/")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_races_empty(self, client):
        response = client.get("/races/")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_results_empty(self, client):
        response = client.get("/results/")
        assert response.status_code == 200
        assert response.json() == []
