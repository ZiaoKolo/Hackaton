from src.data_processor import clean_user_record, clean_user_records


def test_clean_user_record_normalizes_values():
    record = {
        "user_id": " U1 ",
        "name": " Ava  Smith ",
        "age": "24",
        "preferences": " Tech, Design ",
    }

    cleaned = clean_user_record(record)

    assert cleaned["user_id"] == "u1"
    assert cleaned["name"] == "ava smith"
    assert cleaned["age"] == 24
    assert cleaned["preferences"] == ["tech", "design"]


def test_clean_user_records_processes_multiple_rows():
    cleaned = clean_user_records([{"user_id": "U2", "name": "Noah"}])

    assert cleaned[0]["user_id"] == "u2"
