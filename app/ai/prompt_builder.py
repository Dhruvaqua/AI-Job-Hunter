class PromptBuilder:

    @staticmethod
    def resume_tailor(candidate, job):

        return f"""
You are an expert ATS Resume Reviewer.

Candidate

Name:
{candidate["name"]}

Experience:
{candidate["experience"]} years

Skills:
{", ".join(candidate["skills"])}

Target Job

Title:
{job["title"]}

Company:
{job["company"]}

Description:
{job["description"]}

Required Skills:
{job["required_skills"]}

Return ONLY markdown.

Include:

# ATS Score

# Missing Keywords

# Resume Improvements

# Better Professional Summary

# Final Advice
"""

    @staticmethod
    def interview_questions(candidate, job):

        return f"""
You are a Senior Software Engineering Interviewer.

Candidate Skills

{", ".join(candidate["skills"])}

Target Role

{job["title"]}

Generate

# Technical Questions

# Coding Questions

# Behavioral Questions

# System Design Questions

# Sample Answers
"""

    @staticmethod
    def learning_roadmap(candidate, job):

        return f"""
You are a Senior Engineering Mentor.

Candidate Skills

{", ".join(candidate["skills"])}

Required Skills

{job["required_skills"]}

Return markdown.

Include

# Current Skill Match

# Missing Skills

# Week 1

# Week 2

# Week 3

# Week 4

# Learning Resources

# Estimated Match Improvement
"""