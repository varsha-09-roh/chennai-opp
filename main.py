from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import json

app = FastAPI(title="ChennaiOpp API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Data Models ───────────────────────────────────────────────
class Opportunity(BaseModel):
    id: int
    title: str
    category: str          # scholarship | internship | workshop | govt_exam | hackathon
    organizer: str
    description: str
    deadline: str
    location: str          # Chennai area or "Online"
    link: str
    is_free: bool
    posted_date: str
    tags: list[str]

# ─── Sample Data (replace with Supabase/DB later) ──────────────
OPPORTUNITIES: list[dict] = [
    {
        "id": 1,
        "title": "Tamil Nadu Merit Scholarship 2025",
        "category": "scholarship",
        "organizer": "TN Government",
        "description": "Merit-based scholarship for students scoring above 80% in 12th standard. Covers tuition fees up to ₹50,000 per year.",
        "deadline": "2025-04-30",
        "location": "Chennai",
        "link": "https://www.tnscholarships.gov.in",
        "is_free": True,
        "posted_date": "2025-03-01",
        "tags": ["scholarship", "government", "merit", "12th"]
    },
    {
        "id": 2,
        "title": "IIT Madras Free Python Bootcamp",
        "category": "workshop",
        "organizer": "IIT Madras",
        "description": "4-week intensive Python bootcamp for college students. Certificate provided. Fully online and free.",
        "deadline": "2025-04-15",
        "location": "Online",
        "link": "https://www.iitm.ac.in/bootcamp",
        "is_free": True,
        "posted_date": "2025-03-05",
        "tags": ["python", "free", "certificate", "iit"]
    },
    {
        "id": 3,
        "title": "Zoho Chennai Internship Drive",
        "category": "internship",
        "organizer": "Zoho Corporation",
        "description": "6-month paid internship for final year engineering students. Stipend ₹15,000/month. Chennai office.",
        "deadline": "2025-04-20",
        "location": "Chennai - Estancia IT Park",
        "link": "https://careers.zoho.com",
        "is_free": True,
        "posted_date": "2025-03-06",
        "tags": ["internship", "paid", "engineering", "zoho"]
    },
    {
        "id": 4,
        "title": "TNPSC Group 2 Exam 2025",
        "category": "govt_exam",
        "organizer": "TNPSC",
        "description": "Tamil Nadu Public Service Commission Group 2 exam notification. 700+ vacancies across departments.",
        "deadline": "2025-05-01",
        "location": "Chennai",
        "link": "https://www.tnpsc.gov.in",
        "is_free": True,
        "posted_date": "2025-03-07",
        "tags": ["tnpsc", "government job", "group2", "exam"]
    },
    {
        "id": 5,
        "title": "Anna University Hackathon 2025",
        "category": "hackathon",
        "organizer": "Anna University",
        "description": "48-hour hackathon. Theme: AI for Social Good. Prize pool ₹1,00,000. Open to all college students.",
        "deadline": "2025-04-10",
        "location": "Anna University, Chennai",
        "link": "https://www.annauniv.edu/hackathon",
        "is_free": True,
        "posted_date": "2025-03-08",
        "tags": ["hackathon", "ai", "prize", "college"]
    },
    {
        "id": 6,
        "title": "Google DSC Chennai Workshop",
        "category": "workshop",
        "organizer": "Google Developer Student Clubs",
        "description": "Free Flutter & Firebase hands-on workshop for students. Build a real app in one day.",
        "deadline": "2025-04-05",
        "location": "SRM Institute, Chennai",
        "link": "https://gdsc.community.dev/chennai",
        "is_free": True,
        "posted_date": "2025-03-08",
        "tags": ["flutter", "firebase", "google", "free", "workshop"]
    },
]

# ─── API Routes ─────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "ChennaiOpp API is running 🚀", "version": "1.0.0"}


@app.get("/opportunities", response_model=list[Opportunity])
def get_opportunities(
    category: Optional[str] = Query(None, description="Filter by category"),
    is_free: Optional[bool] = Query(None, description="Filter free only"),
    search: Optional[str] = Query(None, description="Search by keyword"),
):
    """Get all opportunities with optional filters."""
    results = OPPORTUNITIES.copy()

    if category:
        results = [o for o in results if o["category"] == category]

    if is_free is not None:
        results = [o for o in results if o["is_free"] == is_free]

    if search:
        search = search.lower()
        results = [
            o for o in results
            if search in o["title"].lower()
            or search in o["description"].lower()
            or any(search in tag for tag in o["tags"])
        ]

    # Sort by deadline (soonest first)
    results.sort(key=lambda x: x["deadline"])
    return results


@app.get("/opportunities/{opp_id}", response_model=Opportunity)
def get_opportunity(opp_id: int):
    """Get a single opportunity by ID."""
    for opp in OPPORTUNITIES:
        if opp["id"] == opp_id:
            return opp
    return {"error": "Not found"}


@app.get("/categories")
def get_categories():
    """Get all available categories with counts."""
    cats = {}
    for opp in OPPORTUNITIES:
        c = opp["category"]
        cats[c] = cats.get(c, 0) + 1
    return cats


@app.get("/stats")
def get_stats():
    """App stats for dashboard."""
    return {
        "total_opportunities": len(OPPORTUNITIES),
        "free_count": sum(1 for o in OPPORTUNITIES if o["is_free"]),
        "categories": len(set(o["category"] for o in OPPORTUNITIES)),
        "last_updated": datetime.now().isoformat()
    }
