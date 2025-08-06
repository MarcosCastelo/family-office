"""All model family tests"""
from app.models.family import Family

def test_join_family(client, db, access_token):
    family = Family(name="Familia Teste")
    db.session.add(family)
    db.session.commit()
    response = client.post(
        f"/families/join/{family.id}",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        },
        json={}  # força o header correto
    )

    assert response.status_code == 200
    assert b"associado" in response.data 