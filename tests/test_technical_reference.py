from scripts.export_technical_reference import markdown, reference


def test_documented_reference_is_derived_from_models_and_routes():
    data = reference()
    assert len(data["tables"]) == 17
    assert "routine_exercises" in {table["name"] for table in data["tables"]}
    assert "/mis-rutinas/<int:routine_id>/registrar" in {route["path"] for route in data["routes"]}
    content = markdown(data)
    assert "measurement_consent_at" in content
    assert "personalization_completed_at" in content
    exercise = next(table for table in data["tables"] if table["name"] == "routine_exercises")
    assert "repetitions IS NOT NULL OR duration_seconds IS NOT NULL" in exercise["constraints"]
