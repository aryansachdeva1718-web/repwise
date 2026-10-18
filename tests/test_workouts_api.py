
import sqlite3

import pytest
from fastapi.testclient import TestClient

from api.main import app
import api.routers.workouts as workouts_router


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    db_path = tmp_path / "repwise_api_test.db"

    conn = sqlite3.connect(db_path)
    conn.executescript("""
        CREATE TABLE workout_sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            hevy_session_key TEXT UNIQUE NOT NULL,
            title TEXT,
            start_time TEXT NOT NULL,
            end_time TEXT,
            description TEXT
        );

        CREATE TABLE exercises (
            exercise_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        );

        CREATE TABLE workout_sets (
            set_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            exercise_id INTEGER NOT NULL,
            order_in_session INTEGER NOT NULL,
            set_number INTEGER NOT NULL,
            set_type TEXT,
            weight REAL,
            reps INTEGER,
            rpe REAL,
            FOREIGN KEY (session_id)
                REFERENCES workout_sessions(session_id)
                ON DELETE CASCADE,
            FOREIGN KEY (exercise_id)
                REFERENCES exercises(exercise_id)
        );

        INSERT INTO exercises (exercise_id, name)
        VALUES (1, 'Bench Press');
    """)
    conn.close()

    def isolated_connection():
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    monkeypatch.setattr(
        workouts_router,
        "get_connection",
        isolated_connection
    )

    return db_path


def test_workout_crud(test_db):
    client = TestClient(app)

    payload = {
        "title": "API Test - Push Day",
        "start_time": "2026-10-18T10:00:00",
        "end_time": "2026-10-18T11:00:00",
        "description": "Automated test",
        "exercises": [
            {
                "exercise_id": 1,
                "sets": [
                    {
                        "set_type": "normal",
                        "weight": 60,
                        "reps": 10
                    },
                    {
                        "set_type": "normal",
                        "weight": 65,
                        "reps": 8
                    }
                ]
            }
        ]
    }

    # CREATE
    response = client.post("/workouts/", json=payload)
    assert response.status_code == 201, response.text
    session_id = response.json()["session_id"]

    # READ
    response = client.get(f"/workouts/{session_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "API Test - Push Day"
    assert len(response.json()["exercises"][0]["sets"]) == 2

    # UPDATE
    response = client.patch(
        f"/workouts/{session_id}",
        json={"title": "Updated Push Day"}
    )
    assert response.status_code == 200

    response = client.get(f"/workouts/{session_id}")
    assert response.json()["title"] == "Updated Push Day"

    # VALIDATION
    response = client.patch(f"/workouts/{session_id}", json={})
    assert response.status_code == 400

    response = client.patch(
        f"/workouts/{session_id}",
        json={"start_time": None}
    )
    assert response.status_code == 422

    # DELETE
    response = client.delete(f"/workouts/{session_id}")
    assert response.status_code == 204
    assert response.content == b""

    # VERIFY CASCADE
    conn = sqlite3.connect(test_db)
    remaining = conn.execute(
        "SELECT COUNT(*) FROM workout_sets WHERE session_id = ?",
        (session_id,)
    ).fetchone()[0]
    conn.close()

    assert remaining == 0

    # DELETE AGAIN
    response = client.delete(f"/workouts/{session_id}")
    assert response.status_code == 404


def test_nonexistent_workout(test_db):
    client = TestClient(app)

    assert client.get("/workouts/999999").status_code == 404
    assert client.patch(
        "/workouts/999999",
        json={"title": "Test"}
    ).status_code == 404
    assert client.delete("/workouts/999999").status_code == 404


def test_empty_workout_detail(test_db):
    conn = sqlite3.connect(test_db)
    conn.execute(
        """INSERT INTO workout_sessions
           (hevy_session_key, title, start_time)
           VALUES (?, ?, ?)""",
        ("empty_test", "Empty Workout", "2026-10-18T12:00:00")
    )
    session_id = conn.execute(
        "SELECT last_insert_rowid()"
    ).fetchone()[0]
    conn.commit()
    conn.close()

    response = TestClient(app).get(f"/workouts/{session_id}")

    assert response.status_code == 200
    assert response.json()["exercises"] == []


def test_invalid_exercise_rolls_back(test_db):
    payload = {
        "title": "Invalid Exercise",
        "start_time": "2026-10-18T10:00:00",
        "end_time": None,
        "description": None,
        "exercises": [
            {
                "exercise_id": 999999,
                "sets": [
                    {"set_type": "normal", "weight": 50, "reps": 10}
                ]
            }
        ]
    }

    response = TestClient(app).post("/workouts/", json=payload)
    assert response.status_code == 400

    conn = sqlite3.connect(test_db)
    count = conn.execute(
        "SELECT COUNT(*) FROM workout_sessions"
    ).fetchone()[0]
    conn.close()

    assert count == 0
