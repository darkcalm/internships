Dear Hiring Manager,

I am writing to express my enthusiastic interest in the **{{ job_details.title }}** position at **{{ job_details.company }}**, a role I was excited to discover on the WIPO internship roster. My background in **{{ personal_data.education[0].degree }}** and my hands-on experience as a **{{ personal_data.workExperience[0].title }}** have equipped me with a unique blend of technical knowledge and practical skills that align perfectly with the requirements of this internship.

{% set processed_experiences = [] %}
{% for requirement, matches in mappings.items() if matches %}
    {% for match in matches if match.experience.text not in processed_experiences %}
        {% if loop.first %}
**In relation to the requirement for {{ requirement }}, my experience has provided me with direct, relevant capabilities.** {{ match.reasoning }}
            {% set _ = processed_experiences.append(match.experience.text) %}
        {% endif %}
    {% endfor %}
{% endfor %}

I am particularly drawn to this opportunity at {{ job_details.company }} because of your work in [mention specific area from job_data.jobDetails.summary or your own research]. This resonates with my own interests and my experience in areas like {{ personal_data.skills.softSkills | random }} and {{ personal_data.skills.technologies | random }}. I am confident that my proactive and detail-oriented approach would allow me to quickly integrate and contribute to your team's objectives.

Thank you for your time and consideration. I have attached my full resume for your review and welcome the opportunity to discuss my application further.

Sincerely,

{{ personal_data.contactInfo.name }}
{{ personal_data.contactInfo.email }}
{{ personal_data.contactInfo.phone }} 