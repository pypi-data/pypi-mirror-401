"""Test suite for koob_resume."""

import json

from koob_resume.koob_resume import cli_runner, get_output_filename


def test_get_output_filename():
    """Test filename generation logic."""
    data_full = {
        "p_info": {"name": "John Doe"},
        "job_target": {"role": "Developer"},
    }
    assert get_output_filename(data_full) == "John_Doe_Developer.pdf"

    data_missing_name = {
        "p_info": {},
        "job_target": {"role": "Manager"},
    }
    assert get_output_filename(data_missing_name) == "resume.pdf"

    data_spaces = {
        "p_info": {"name": "John Von Doe"},
        "job_target": {"role": "Senior Dev"},
    }
    assert get_output_filename(data_spaces) == "John_Von_Doe_Senior_Dev.pdf"


def test_cli_runner(tmp_path, capsys, monkeypatch):
    """Test that cli_runner processes a JSON file correctly."""
    monkeypatch.chdir(tmp_path)
    data = {
        "p_info": {
            "name": "Test",
            "email": "t@t.com",
            "phone": "1",
            "linkedin": "l",
        },
        "job_target": {"role": "Tester"},
        "summary": "Summary",
        "skills": {"Python": ["Pytest", "Automation"]},
        "experience": [
            {
                "title": "Software Engineer",
                "company": "Tech Corp",
                "website": "example.com",
                "duration": "2020-Present",
                "summary": "Building cool stuff.",
                "responsibilities": ["Coding", "Testing"],
            }
        ],
        "education": [
            {
                "degree": "BSc CS",
                "institution": "University of Tech",
                "duration": "2016-2020",
                "summary": "Graduated with honors",
            }
        ],
        "certifications": [{"cert": "Certified Pro", "year": "2024"}],
    }
    json_file = tmp_path / "test.json"
    json_file.write_text(json.dumps(data))

    cli_runner([str(json_file)])

    captured = capsys.readouterr()
    assert captured.err == ""

    expected_pdf = tmp_path / "Test_Tester.pdf"
    assert expected_pdf.exists()
