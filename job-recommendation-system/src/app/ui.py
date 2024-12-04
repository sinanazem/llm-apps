import streamlit as st
from PyPDF2 import PdfReader
import psycopg2
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

from src.utils import get_embeddings
from src.retrive import get_top3_similar_docs

                
import streamlit as st
import os

import base64
from PIL import Image

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    resume_text = ""
    for page in reader.pages:
        resume_text += page.extract_text()
    return resume_text


connection = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="mypass",
    host="localhost",
    port="5432"
)



def image_to_base64(image_path):
        """
        Convert an image file to base64.
        """
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string
    
    
def display_profile_card(job):
    # HTML and CSS for profile card
    card_html = f"""
    <style>
    .profile-card {{
        width: 100%;
        max-width: 230px;
        margin: 0 auto;
        text-align: center;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        transition: 0.3s;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
        height: 350px;  /* Force same height for all cards */
    }}
    .profile-card:hover {{
        box-shadow: 0 0 20px rgba(0,0,0,0.2);
    }}
    .profile-card img {{
        border-radius: 50%;
        width: 100px;
        height: 100px;
        object-fit: cover;
    }}
    .social-icons a {{
        margin: 5px;
        text-decoration: none;
        color: gray;
        font-size: 20px;
    }}
    .social-icons a:hover {{
        color: #007bff;
    }}
    </style>
    <div class="profile-card">
        <img src="{job['company_logo']}" alt="Profile Image">
        <h6>{job['company_name']}</h6>
        <a href="{job["url"]}"><h7>{job['job_position']}</h7></a>
        <p>{job['location']}</p>
        <div class="social-icons">
    """
    social_media_links = {
        "twitter": '<i class="fab fa-twitter"></i>',
        "github": '<i class="fab fa-github"></i>',
        "linkedin": '<i class="fab fa-linkedin"></i>',
        "personal_website": '<i class="fas fa-globe"></i>',
        "instagram": '<i class="fab fa-instagram"></i>'
    }
    for key, icon in social_media_links.items():
        if job.get(key):
            card_html += f'<a href="{job[key]}" target="_blank">{icon}</a>'
    
    # card_html += """
    #     </div>
    # </div>
    # """

    # Include the Font Awesome link
    st.markdown(
        """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
        """,
        unsafe_allow_html=True
    )

    # Display the HTML card
    st.markdown(card_html, unsafe_allow_html=True)




st.header("Job Recommendation")

with st.expander("Upload your resume"):
        uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
        job_description = st.text_area("Enter job description (optional)").strip()
        
if st.button("Jobs Recommendation", use_container_width=True):
            if uploaded_file is not None:
                resume_text = extract_text_from_pdf(uploaded_file)
                top3_similar_docs = get_top3_similar_docs(resume_text, connection)
                num_cols = 3
                cols = st.columns(num_cols)
                for idx, job_data in enumerate(top3_similar_docs):
                    with cols[idx % num_cols]:
                        job = {
                            "company_name": job_data[4],
                            "job_position": job_data[3],
                            "location": job_data[5],
                            "url": job_data[2],
                            "company_logo": "https://cdn-icons-png.flaticon.com/512/9371/9371369.png" if not job_data[14] else  job_data[14],
                        }
                        display_profile_card(job)
            else:
                st.error("Please upload a resume")