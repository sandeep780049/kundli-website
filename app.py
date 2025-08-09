from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

# Zodiac date ranges and info
zodiac_signs = [
    {"sign": "Capricorn", "start": (12, 22), "end": (1, 19),
     "element": "Earth", "lucky_planet": "Saturn",
     "tips": "Focus on discipline and patience. Hard work will pay off soon."},
    {"sign": "Aquarius", "start": (1, 20), "end": (2, 18),
     "element": "Air", "lucky_planet": "Uranus",
     "tips": "Innovate and embrace new ideas. Your creativity will shine."},
    {"sign": "Pisces", "start": (2, 19), "end": (3, 20),
     "element": "Water", "lucky_planet": "Neptune",
     "tips": "Trust your intuition. Compassion will open new doors."},
    {"sign": "Aries", "start": (3, 21), "end": (4, 19),
     "element": "Fire", "lucky_planet": "Mars",
     "tips": "Be courageous and take initiative. New challenges await."},
    {"sign": "Taurus", "start": (4, 20), "end": (5, 20),
     "element": "Earth", "lucky_planet": "Venus",
     "tips": "Focus on stability and comfort. Relationships grow stronger."},
    {"sign": "Gemini", "start": (5, 21), "end": (6, 20),
     "element": "Air", "lucky_planet": "Mercury",
     "tips": "Communicate clearly and keep learning. Social life flourishes."},
    {"sign": "Cancer", "start": (6, 21), "end": (7, 22),
     "element": "Water", "lucky_planet": "Moon",
     "tips": "Trust your emotions and nurture loved ones. Family time is key."},
    {"sign": "Leo", "start": (7, 23), "end": (8, 22),
     "element": "Fire", "lucky_planet": "Sun",
     "tips": "Express yourself boldly. Leadership opportunities are near."},
    {"sign": "Virgo", "start": (8, 23), "end": (9, 22),
     "element": "Earth", "lucky_planet": "Mercury",
     "tips": "Stay organized and practical. Health and work improve."},
    {"sign": "Libra", "start": (9, 23), "end": (10, 22),
     "element": "Air", "lucky_planet": "Venus",
     "tips": "Seek balance and harmony. Partnerships bring joy."},
    {"sign": "Scorpio", "start": (10, 23), "end": (11, 21),
     "element": "Water", "lucky_planet": "Pluto",
     "tips": "Embrace transformation. Passion fuels your progress."},
    {"sign": "Sagittarius", "start": (11, 22), "end": (12, 21),
     "element": "Fire", "lucky_planet": "Jupiter",
     "tips": "Explore new horizons. Optimism brings success."},
]

def get_zodiac_sign(month, day):
    for zodiac in zodiac_signs:
        start_month, start_day = zodiac["start"]
        end_month, end_day = zodiac["end"]

        if start_month == 12 and end_month == 1:
            # Capricorn case spanning year end
            if (month == 12 and day >= start_day) or (month == 1 and day <= end_day):
                return zodiac
        else:
            if (month == start_month and day >= start_day) or (month == end_month and day <= end_day) or (start_month < month < end_month):
                return zodiac
    # fallback (should never happen)
    return None

@app.route('/', methods=['GET', 'POST'])
def home():
    kundli = None
    tips = None
    error = None

    if request.method == 'POST':
        birth_date_str = request.form.get('birth_date')
        if not birth_date_str:
            error = "Please enter a valid birth date."
        else:
            try:
                birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')
                zodiac = get_zodiac_sign(birth_date.month, birth_date.day)
                if zodiac:
                    kundli = {
                        "birth_date": birth_date.strftime("%d %B %Y"),
                        "zodiac_sign": zodiac["sign"],
                        "element": zodiac["element"],
                        "lucky_planet": zodiac["lucky_planet"]
                    }
                    tips = zodiac["tips"]
                else:
                    error = "Could not determine your zodiac sign."
            except Exception as e:
                error = "Invalid date format."
    return render_template('index.html', kundli=kundli, tips=tips, error=error)

if __name__ == '__main__':
    app.run(debug=True)
