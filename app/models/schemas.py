from typing import Tuple, Dict, Any, List

class PredictRequestSchema:
    REQUIRED = [
        "years_experience",
        "education_level",
        "job_title",
        "city",
        "company_size",
        "skills_python",
        "skills_java",
        "skills_aws",
        "skills_sql",
    ]

    CATEGORIES = {
        "education_level": ["High School", "Bachelor", "Master", "PhD"],
        "company_size": ["Small", "Medium", "Large"],
        "city": ["Bengaluru", "Hyderabad", "Pune", "Mumbai", "Chennai", "Delhi NCR"],
        "job_title": [
            "Backend Engineer",
            "Data Analyst",
            "Data Scientist",
            "ML Engineer",
            "Full Stack Engineer",
            "Software Developer",  # ✅ Added
            "Other"                # ✅ Optional
        ]
    }

    @classmethod
    def validate(cls, data: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
        errors = []

        # Presence and type checks
        for key in cls.REQUIRED:
            if key not in data:
                errors.append(f"Missing field: {key}")

        # Early return if missing
        if errors:
            return {}, errors

        # Numeric
        try:
            years = float(data["years_experience"])
            if years < 0 or years > 50:
                errors.append("years_experience must be between 0 and 50")
        except Exception:
            errors.append("years_experience must be numeric")

        # Categorical checks
        for cat in ["education_level", "company_size", "city", "job_title"]:
            if data.get(cat) not in cls.CATEGORIES[cat]:
                errors.append(f"{cat} must be one of {cls.CATEGORIES[cat]}")

        # Binary skills
        for sk in ["skills_python", "skills_java", "skills_aws", "skills_sql"]:
            try:
                v = int(data[sk])
                if v not in (0, 1):
                    errors.append(f"{sk} must be 0 or 1")
            except Exception:
                errors.append(f"{sk} must be integer 0/1")

        if errors:
            return {}, errors

        # Clean payload
        cleaned = {
            "years_experience": years,
            "education_level": data["education_level"],
            "job_title": data["job_title"],
            "city": data["city"],
            "company_size": data["company_size"],
            "skills_python": int(data["skills_python"]),
            "skills_java": int(data["skills_java"]),
            "skills_aws": int(data["skills_aws"]),
            "skills_sql": int(data["skills_sql"]),
        }
        return cleaned, []
