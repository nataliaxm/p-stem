from flask import Flask, render_template, jsonify

app = Flask(__name__)

QUESTIONS = [
    {
        "id": "academic",
        "text": "Are you interested in academic RSOs?",
        "type": "yesno",
        "followup": "academic_detail",
    },
    {
        "id": "academic_detail",
        "text": "Which academic areas interest you?",
        "type": "multichoice",
        "choices": [
            {"id": "premed",     "label": "Pre-Med"},
            {"id": "prelaw",     "label": "Pre-Law"},
            {"id": "tech",       "label": "Tech / CS"},
            {"id": "econ",       "label": "Economics"},
            {"id": "science",    "label": "Natural Sciences"},
            {"id": "humanities", "label": "Humanities"},
        ],
    },
    {
        "id": "cultural",
        "text": "Are you interested in Cultural or Identity-Based RSOs?",
        "type": "yesno",
        "followup": "cultural_detail",
    },
    {
        "id": "cultural_detail",
        "text": "Which cultural communities resonate with you?",
        "type": "multichoice",
        "choices": [
            {"id": "east_asian",     "label": "East Asian"},
            {"id": "south_asian",    "label": "South Asian"},
            {"id": "african",        "label": "African / Caribbean"},
            {"id": "latin",          "label": "Latin American"},
            {"id": "middle_eastern", "label": "Middle Eastern"},
            {"id": "european",       "label": "European"},
        ],
    },
    {
        "id": "sports",
        "text": "Are you interested in Sports & Recreation?",
        "type": "yesno",
        "followup": "sports_detail",
    },
    {
        "id": "sports_detail",
        "text": "Which sports or activities interest you?",
        "type": "multichoice",
        "choices": [
            {"id": "team_sports", "label": "Team Sports"},
            {"id": "individual",  "label": "Individual Sports"},
            {"id": "extreme",     "label": "Outdoor / Adventure"},
            {"id": "dance",       "label": "Dance"},
        ],
    },
    {
        "id": "arts",
        "text": "Are you interested in Art, Media, or Entertainment?",
        "type": "yesno",
        "followup": "arts_detail",
    },
    {
        "id": "arts_detail",
        "text": "What creative areas interest you?",
        "type": "multichoice",
        "choices": [
            {"id": "journalism",  "label": "Journalism / Writing"},
            {"id": "film",        "label": "Film / Photography"},
            {"id": "theater",     "label": "Theater / Performance"},
            {"id": "music",       "label": "Music / A Cappella"},
            {"id": "visual_arts", "label": "Visual Arts"},
        ],
    },
    {
        "id": "service",
        "text": "Are you interested in Community Service or Activism?",
        "type": "yesno",
        "followup": None,
    },
    {
        "id": "gov",
        "text": "Are you interested in Student Government?",
        "type": "yesno",
        "followup": None,
    },
    {
        "id": "spiritual",
        "text": "Are you interested in Spiritual or Religious groups?",
        "type": "yesno",
        "followup": "spiritual_detail",
    },
    {
        "id": "spiritual_detail",
        "text": "Which spiritual communities resonate with you?",
        "type": "multichoice",
        "choices": [
            {"id": "christian",  "label": "Christian"},
            {"id": "jewish",     "label": "Jewish"},
            {"id": "muslim",     "label": "Muslim"},
            {"id": "hindu",      "label": "Hindu"},
            {"id": "buddhist",   "label": "Buddhist"},
            {"id": "interfaith", "label": "Interfaith"},
        ],
    },
]

RSOS = [
    # Academic
    {"name": "Pre-Medical Society",        "description": "Supports students pursuing medical school with resources, mentorship, and clinical shadowing opportunities.", "tags": ["premed"]},
    {"name": "Pre-Law Society",            "description": "Connects pre-law students with resources, mock trials, and alumni in the legal profession.", "tags": ["prelaw"]},
    {"name": "CS Student Association",     "description": "Community for CS students with hackathons, networking events, and industry connections.", "tags": ["tech"]},
    {"name": "Society of Women Engineers", "description": "Empowers women in STEM through networking, professional development, and mentorship.", "tags": ["tech", "science"]},
    {"name": "Data Science Club",          "description": "Hands-on projects in data analysis, machine learning, and visualization.", "tags": ["tech"]},
    {"name": "Economics Society",          "description": "Connects economics students with speakers, case competitions, and career resources.", "tags": ["econ"]},
    {"name": "Biology Student Association","description": "Community for biology students with research opportunities and grad school prep.", "tags": ["science", "premed"]},
    {"name": "Humanities Council",         "description": "Brings together students in literature, history, philosophy, and the arts for interdisciplinary discourse.", "tags": ["humanities"]},

    # Cultural
    {"name": "Chinese Students Association",              "description": "Celebrates Chinese culture through events, language exchange, and community.", "tags": ["east_asian"]},
    {"name": "Korean Students Association",               "description": "Connects Korean and Korean-American students through cultural events and community.", "tags": ["east_asian"]},
    {"name": "South Asian Student Alliance",              "description": "Celebrates South Asian culture, heritage, and community through events and advocacy.", "tags": ["south_asian"]},
    {"name": "African Caribbean Student Association",     "description": "Celebrates African and Caribbean cultures through events, mentorship, and community.", "tags": ["african"]},
    {"name": "Organization of Latin American Students",   "description": "Promotes Latin American culture and provides community for Latinx students.", "tags": ["latin"]},
    {"name": "Middle Eastern Student Association",        "description": "Celebrates Middle Eastern cultures and creates community for students from the region.", "tags": ["middle_eastern"]},
    {"name": "European Student Association",              "description": "Connects students with European backgrounds through cultural events and discussion.", "tags": ["european"]},

    # Sports
    {"name": "UChicago Frenzy (Ultimate Frisbee)", "description": "Competitive ultimate frisbee team with practices, tournaments, and a great community.", "tags": ["extreme", "team_sports"]},
    {"name": "Club Swimming",                       "description": "Competitive club swim team with regular practices and collegiate meets.", "tags": ["individual"]},
    {"name": "Rock Climbing Club",                  "description": "Explore indoor and outdoor climbing with members of all skill levels.", "tags": ["extreme", "individual"]},
    {"name": "Soccer Club",                         "description": "Competitive and recreational soccer for all skill levels.", "tags": ["team_sports"]},
    {"name": "Basketball Club",                     "description": "Recreational and competitive basketball with regular pickup games and league play.", "tags": ["team_sports"]},
    {"name": "UChicago Dance Sport",                "description": "Competitive ballroom and Latin dance club with training and intercollegiate competitions.", "tags": ["dance"]},
    {"name": "Running Club",                        "description": "Community runs across Chicago for all paces, plus race training support.", "tags": ["individual"]},

    # Arts / Media
    {"name": "The Chicago Maroon",       "description": "UChicago's independent student newspaper covering news, opinions, arts, and sports.", "tags": ["journalism"]},
    {"name": "Fire Escape Films",        "description": "Student film production organization making short films and longer projects.", "tags": ["film"]},
    {"name": "University Theater",       "description": "Student-run theater producing mainstage and workshop productions each quarter.", "tags": ["theater"]},
    {"name": "Off-Off Campus (Improv)",  "description": "UChicago's longest-running improvisational comedy group.", "tags": ["theater"]},
    {"name": "PHiesta (A Cappella)",     "description": "Latin-fusion a cappella group performing contemporary and traditional music.", "tags": ["music"]},
    {"name": "UChicago Photography Club","description": "Community for photographers of all skill levels with workshops and exhibitions.", "tags": ["film", "visual_arts"]},

    # Service
    {"name": "UChicago Votes",        "description": "Nonpartisan voter registration and civic engagement on campus.", "tags": ["service"]},
    {"name": "Food Recovery Network", "description": "Recovers surplus dining hall food to donate to local communities in need.", "tags": ["service"]},
    {"name": "Community Service Fund","description": "Funds and coordinates student community service initiatives across Chicago.", "tags": ["service"]},
    {"name": "Best Buddies",          "description": "Creates friendship and leadership opportunities for people with intellectual disabilities.", "tags": ["service"]},

    # Student Government
    {"name": "Student Government", "description": "The main representative body for UChicago students — voice student concerns and shape campus policy.", "tags": ["gov"]},
    {"name": "College Council",     "description": "Undergraduate student government focused on college-specific programming and advocacy.", "tags": ["gov"]},

    # Spiritual
    {"name": "Catholic Student Association",      "description": "Community for Catholic students with Mass, fellowship, and service opportunities.", "tags": ["christian"]},
    {"name": "InterVarsity Christian Fellowship", "description": "Non-denominational Christian community focused on faith, fellowship, and outreach.", "tags": ["christian", "interfaith"]},
    {"name": "Hillel",                            "description": "Center for Jewish life on campus with Shabbat, holidays, and cultural programming.", "tags": ["jewish"]},
    {"name": "Muslim Students Association",       "description": "Community for Muslim students with prayer, events, and cultural programming.", "tags": ["muslim"]},
    {"name": "Hindu Students Council",            "description": "Celebrates Hindu culture and spirituality through events and community.", "tags": ["hindu"]},
    {"name": "Buddhist Student Association",      "description": "Meditation, dharma talks, and a welcoming community for practitioners of all backgrounds.", "tags": ["buddhist"]},
    {"name": "Interfaith Council",                "description": "Brings together students of all faiths for dialogue, service, and shared programming.", "tags": ["interfaith"]},
]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/data")
def data():
    return jsonify({"questions": QUESTIONS, "rsos": RSOS})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
