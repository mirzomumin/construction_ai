import pytest

@pytest.mark.asyncio(loop_scope="session")
async def test_create_project_success(client):
    response = await client.post(
        "/projects/",
        json={
            "project_name": "Restaurant",
            "location": "San Francisco"
        },
    )

    response_data = response.json()

    ######### assert response ##########
    assert response.status_code == 200
    ####################################


# @pytest.mark.asyncio(loop_scope="session")
# async def test_me_fail_invalid_token(client):
#     # send request to update tokens
#     response = await client.get(
#         "/api/v1/user/me",
#         headers={"Authorization": "Bearer invalid-access-token"},
#     )

#     response_data = response.json()

#     ######### assert response ##########
#     assert response.status_code == 401
#     assert response_data["detail"] == "Token Invalid"
#     ####################################


# @pytest.mark.asyncio(loop_scope="session")
# async def test_me_fail_expired_token(client):
#     user = await create_user()
#     payload = {"sub": user.username, "user_id": str(user.id)}
#     access_token = JWTToken.encode_jwt(payload=payload, ttl=-1)

#     # send request to update tokens
#     response = await client.get(
#         "/api/v1/user/me",
#         headers={"Authorization": f"Bearer {access_token}"},
#     )

#     response_data = response.json()

#     ######### assert response ##########
#     assert response.status_code == 401
#     assert response_data["detail"] == "Token Expired"
#     ####################################