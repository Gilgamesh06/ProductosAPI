
def test_add_categoria(client, categoria_data_list):
    for categoria_data in categoria_data_list:
        response = client.post("/categoria/register", json=categoria_data)
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == categoria_data["nombre"]

def test_get_all_categorias(client, categoria_data_list):
    response = client.get("/categoria/get", params={"skip": 0, "limit": 10})
    assert response.status_code == 200
    data = response.json().get("content", [])
    assert len(data) == len(categoria_data_list)
    for i, categoria_data in enumerate(categoria_data_list):
        assert data[i]["nombre"] == categoria_data["nombre"]

def test_update_categoria(client):

    # First, create a categoria to update
    create_response = client.post("/categoria/register", json={"nombre": "Ropa"})
    assert create_response.status_code == 200
    created_categoria = create_response.json()
    categoria_id = created_categoria["id"]

    # Now, update the categoria
    update_data = {"nombre": "Ropa Actualizada"}
    update_response = client.put(f"/categoria/update/{categoria_id}", json=update_data)
    assert update_response.status_code == 200
    updated_categoria = update_response.json()
    assert updated_categoria["nombre"] == update_data["nombre"] 

def test_delete_categoria(client):

    # First, create a categoria to delete
    create_response = client.post("/categoria/register", json={"nombre": "Camisetas"})
    assert create_response.status_code == 200
    created_categoria = create_response.json()
    categoria_id = created_categoria["id"]

    # Now, delete the categoria
    delete_response = client.delete(f"/categoria/delete/{categoria_id}")
    assert delete_response.status_code == 200
    deleted_categoria = delete_response.json()
    assert deleted_categoria["estado"] == "INACTIVO"