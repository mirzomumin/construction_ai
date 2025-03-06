import pytest

@pytest.mark.asyncio(loop_scope="session")
async def test_retrieve_project_success(client, project_obj):

    response = await client.get(f"/projects/{project_obj.id}")
    response_data = response.json()

    ######### assert response ##########
    assert response.status_code == 200
    assert response_data['project_name'] == project_obj.name
    assert response_data['location'] == project_obj.location
    assert response_data['status'] == project_obj.status
    assert isinstance(response_data['tasks'], list)
    assert 'id' in response_data

    if response_data['tasks']:
        task0 = response_data['tasks'][0]
        assert 'name' in task0
        assert 'status' in task0
    ####################################


@pytest.mark.asyncio(loop_scope="session")
async def test_retrieve_project_fail(client):
    response = await client.get("/projects/2")

    response_data = response.json()

    ######### assert response ##########
    assert response.status_code == 404
    assert response_data['detail'] == 'Project not found'
    ####################################
