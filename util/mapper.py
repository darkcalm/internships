# util/mapper.py
# This module performs the semantic mapping between the applicant's profile and the job data.

import json
from sentence_transformers import SentenceTransformer, util
import torch
from openai import OpenAI

client = OpenAI()

def get_reasoning_for_match(requirement: str, experience: dict, prompt_file: str) -> str:
    """Uses an LLM to generate a causal reasoning statement for a match."""
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            system_prompt = f.read()
    except FileNotFoundError:
        return "Error: Reasoning prompt file not found."

    experience_text = experience.get('text', 'N/A')
    user_prompt = f"Job Requirement: \"{requirement}\"\nCandidate Experience: \"{experience_text}\""

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5,
            max_tokens=150
        )
        reasoning = completion.choices[0].message.content.strip()
        return reasoning
    except Exception as e:
        return f"Error generating reasoning: {e}"

def generate_mappings(personal_data_path: str, job_data_path: str, mappings_output_path: str, reasoning_prompt_path: str):
    """
    Compares personal and job data to find semantic matches and saves them.
    This version captures all potential matches for later processing.

    Args:
        personal_data_path: Path to the applicant's structured data.
        job_data_path: Path to the job's structured data.
        mappings_output_path: Path to save the resulting mappings.
        reasoning_prompt_path: Path to the reasoning prompt file.
    """
    print("Loading data for mapping...")
    try:
        with open(personal_data_path, 'r', encoding='utf-8') as f:
            personal_data = json.load(f)
        with open(job_data_path, 'r', encoding='utf-8') as f:
            job_data = json.load(f)
    except FileNotFoundError as e:
        print(f"Error: Could not find data file at {e.filename}. Please ensure both personal and job data have been transformed.")
        return

    print("Initializing sentence transformer model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # --- Create a flattened corpus of the user's experiences and skills ---
    experience_corpus = []
    experience_map = {}

    for job in personal_data.get("workExperience", []):
        for resp in job.get("responsibilities", []):
            source = f"Work Experience: {job.get('title')}"
            experience_corpus.append(resp)
            experience_map[resp] = {"source": source, "text": resp}
    
    for project in personal_data.get("projects", []):
        desc = project.get("description", "")
        source = f"Project: {project.get('name')}"
        experience_corpus.append(desc)
        experience_map[desc] = {"source": source, "text": desc}

    skills = personal_data.get("skills", {})
    for category, skill_list in skills.items():
        for skill in skill_list:
            source = f"Skill: {category}"
            experience_corpus.append(skill)
            experience_map[skill] = {"source": source, "text": skill}

    if not experience_corpus:
        print("Warning: No personal experiences or skills found to map from.")
        return
        
    experience_embeddings = model.encode(experience_corpus, convert_to_tensor=True)

    # --- Create a flattened corpus of job requirements ---
    requirements_corpus = []
    job_reqs = job_data.get("requirements", {})
    for exp_req in job_reqs.get("workExperience", []):
        requirements_corpus.append(exp_req)
    for edu_req in job_reqs.get("education", []):
        requirements_corpus.append(edu_req)
    for category, skill_list in job_reqs.get("skills", {}).items():
        for skill in skill_list:
            requirements_corpus.append(skill)

    if not requirements_corpus:
        print("Warning: No job requirements found to map to.")
        return
        
    requirement_embeddings = model.encode(requirements_corpus, convert_to_tensor=True)

    # --- Compute semantic similarity and find matches ---
    print("Computing semantic similarities...")
    cosine_scores = util.cos_sim(requirement_embeddings, experience_embeddings)

    mappings = {}
    for i, req in enumerate(requirements_corpus):
        top_k = min(5, len(experience_corpus))
        scores, indices = torch.topk(cosine_scores[i], k=top_k)
        
        matches = []
        for score, idx in zip(scores, indices):
            matched_experience = experience_corpus[idx]
            
            # Generate reasoning for this specific match
            reasoning = get_reasoning_for_match(req, experience_map[matched_experience], reasoning_prompt_path)

            matches.append({
                "experience": experience_map[matched_experience],
                "similarity": f"{score.item():.2f}",
                "reasoning": reasoning
            })
        
        if matches:
            mappings[req] = matches
            
    # --- Save the mappings ---
    try:
        with open(mappings_output_path, 'w', encoding='utf-8') as f:
            json.dump(mappings, f, indent=4)
        print(f"Successfully generated and saved mappings to '{mappings_output_path}'.")
    except IOError as e:
        print(f"Error saving mappings file: {e}") 