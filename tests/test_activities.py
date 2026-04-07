"""Tests for activities API endpoints."""

import pytest


def test_get_activities_returns_all_activities(client):
    """Test GET /activities returns all activities with correct structure."""
    # Arrange: No specific setup needed as data is in-memory

    # Act: Make GET request to /activities
    response = client.get("/activities")

    # Assert: Check status and response content
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 9  # Should have 9 activities
    assert "Chess Club" in data
    assert "Programming Class" in data
    # Verify structure of one activity
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)


def test_signup_for_valid_activity(client):
    """Test POST /activities/{activity_name}/signup with valid data."""
    # Arrange: Choose an activity and new email
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check success response
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}


def test_signup_for_invalid_activity(client):
    """Test POST /activities/{activity_name}/signup with invalid activity."""
    # Arrange: Use non-existent activity
    activity_name = "NonExistent Club"
    email = "student@mergington.edu"

    # Act: Make POST request
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check 404 error
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_duplicate_participant(client):
    """Test POST /activities/{activity_name}/signup with duplicate email."""
    # Arrange: Use an activity and email that's already signed up
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already in participants

    # Act: Make POST request
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check 400 error
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up"}


def test_remove_valid_participant(client):
    """Test DELETE /activities/{activity_name}/participants with valid data."""
    # Arrange: Use an activity and existing participant
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act: Make DELETE request
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert: Check success response
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}


def test_remove_participant_from_invalid_activity(client):
    """Test DELETE /activities/{activity_name}/participants with invalid activity."""
    # Arrange: Use non-existent activity
    activity_name = "NonExistent Club"
    email = "student@mergington.edu"

    # Act: Make DELETE request
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert: Check 404 error
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_remove_nonexistent_participant(client):
    """Test DELETE /activities/{activity_name}/participants with non-existent participant."""
    # Arrange: Use valid activity but email not in participants
    activity_name = "Chess Club"
    email = "nonexistent@mergington.edu"

    # Act: Make DELETE request
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert: Check 404 error
    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found"}


def test_signup_and_remove_integration(client):
    """Integration test: signup then remove a participant."""
    # Arrange: Choose activity and new email
    activity_name = "Programming Class"
    email = "integrationtest@mergington.edu"

    # Act: First signup
    signup_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert signup_response.status_code == 200

    # Act: Then remove
    remove_response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})
    assert remove_response.status_code == 200

    # Assert: Verify messages
    assert signup_response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert remove_response.json() == {"message": f"Removed {email} from {activity_name}"}