"""Tests for the Resume class."""

import os

import pytest
from koob_resume.resume import Resume


@pytest.fixture
def sample_data():
    """Return a sample data dictionary for testing."""
    return {
        "p_info": {
            "name": "Test User",
            "email": "test@example.com",
            "phone": "123-456-7890",
            "linkedin": "linkedin.com/in/test",
        },
        "job_target": {
            "role": "Test Role",
            "company": "Test Company",
            "manager_name": "Test Manager",
            "address": "123 Test Lane",
        },
        "summary": "This is a test summary.",
        "skills": {"Category 1": ["Skill A", "Skill B"], "Category 2": ["Skill C"]},
        "experience": [
            {
                "title": "Job Title 1",
                "company": "Company A",
                "website": "https://example.com",
                "duration": "2020 - Present",
                "summary": "Working here.",
                "responsibilities": ["Doing things", "Making stuff"],
            }
        ],
        "education": [
            {
                "degree": "B.S. Testing",
                "institution": "Test University",
                "duration": "2010 - 2014",
                "summary": "Learned testing.",
            }
        ],
        "certifications": [{"cert": "Certified Tester", "year": "2024"}],
    }


def test_resume_init(sample_data):
    """Test that the Resume class initializes correctly."""
    resume = Resume(sample_data)
    assert resume.data == sample_data


def test_resume_render_creates_file(sample_data, tmp_path):
    """Test that render creates a PDF file with content."""
    resume = Resume(sample_data)
    output_file = tmp_path / "test_resume.pdf"
    resume.render(output_file)
    assert os.path.exists(output_file)
    assert os.path.getsize(output_file) > 1000
