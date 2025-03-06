import pytest
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio(loop_scope="session")
async def test_create_project_success(client):
    mock_tasks = [
        {"name": "Task 1", "status": "pending"},
        {"name": "Task 2", "status": "pending"},
    ]
    data = {
        "project_name": "Restaurant",
        "location": "San Francisco"
    }

    with patch(
        "app.services.GeminiService.generate_content",
        new_callable=AsyncMock,
        return_value=mock_tasks,
    ):
        response = await client.post(
            "/projects/",
            json=data,
        )

        response_data = response.json()

        ######### assert response ##########
        assert response.status_code == 200
        assert response_data['project_name'] == data['project_name']
        assert response_data['location'] == data['location']
        assert response_data['status'] == 'processing'
        assert isinstance(response_data['tasks'], list)
        assert 'id' in response_data

        if response_data['tasks']:
            task0 = response_data['tasks'][0]
            assert 'name' in task0
            assert 'status' in task0
        ####################################


@pytest.mark.asyncio(loop_scope="session")
async def test_create_project_fail(client):

    response = await client.post(
        "/projects/",
        json={},
    )

    response_data = response.json()
    error_details = response_data['detail']
    ######### assert response ##########
    assert response.status_code == 422
    error_detail0 = error_details[0]
    error_detail1 = error_details[1]

    assert error_detail0['type'] == 'missing'
    assert error_detail0['loc'] == ['body', 'project_name']
    assert error_detail0['msg'] == 'Field required'

    assert error_detail1['type'] == 'missing'
    assert error_detail1['loc'] == ['body', 'location']
    assert error_detail1['msg'] == 'Field required'
    ####################################
