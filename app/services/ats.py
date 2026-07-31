def calculate_ats_score(analysis):

    total_required = (
        len(analysis.matched_required_skills)
        + len(analysis.missing_required_skills)
    )

    total_preferred = (
        len(analysis.matched_preferred_skills)
        + len(analysis.missing_preferred_skills)
    )

    required_score = (
        len(analysis.matched_required_skills)
        / total_required * 100
        if total_required > 0 else 0
    )

    preferred_score = (
        len(analysis.matched_preferred_skills)
        / total_preferred * 100
        if total_preferred > 0 else 0
    )

    experience_score = calculate_experience_score(
        analysis.candidate_experience_years,
        analysis.required_experience_years
    )

    education_score = calculate_education_score(
        analysis.education_match
    )

    project_score = calculate_project_relevance_score(
        analysis.relevant_projects,
        analysis.total_projects
    )

    relevance_score = calculate_relevance_score(
        required_score,
        project_score
    )

    overall_score = (
        required_score * 0.50
        + preferred_score * 0.10
        + experience_score * 0.20
        + education_score * 0.10
        + relevance_score * 0.10
    )

    return {
        "overall_score": round(overall_score, 2),
        "required_skills_score": round(required_score, 2),
        "preferred_skills_score": round(preferred_score, 2),
        "experience_score": experience_score,
        "education_score": education_score,
        "project_relevance_score": project_score,
        "relevance_score": relevance_score,
    }