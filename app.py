from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('library_system.db')
    cursor = conn.cursor()
    
    # PRAGMA modifies the SQLite db engine
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # NOTE
    # SQLite prefers integer, text, or real
    cursor.execute('''CREATE TABLE IF NOT EXISTS watch_history
                        (watch_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        profile_id INTEGER,
                        content_id INTEGER,
                        episode_id INTEGER,
                        watched_at INTEGER,
                        progress_seconds INTEGER,
                        FOREIGN KEY (profile_id) REFERENCES profile (profile_id ),
                        FOREIGN KEY (content_id) REFERENCES content (content_id),
                        FOREIGN KEY (episode_id) REFERENCES episode (episode_id))''')
    
    cursor.execute ('''CREATE TABLE IF NOT EXISTS season
                        (season_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content_id INTEGER,
                        season_number INTEGER,
                        release_year INTEGER,
                        FOREIGN KEY (content_id) REFERENCES content (content_id))''')
    
    cursor.execute ('''CREATE TABLE IF NOT EXISTS episode
                        (episode_id PRIMARY KEY INTEGER AUTOINCREMENT,
                        season_id INTEGER,
                        episode_number INTEGER,
                        title TEXT,
                        duration_mins INTEGER,
                        FOREIGN KEY (season_id) REFERENCES season (season_id))''')
    
    cursor.execute ('''CREATE TABLE IF NOT EXISTS my_list
                        (list_item_id PRIMARY INTEGER KEY AUTOINCREMENT,
                        profile_id INTEGER,
                        content_id INTEGER,
                        added_at INTEGER,
                        FOREIGN KEY (profile_id) REFERENCES profile (profile_id))''')
    
    # here i leave is_original as an integer to abide by SQLite; 1 or 0 is bool
    cursor.execute ('''CREATE TABLE IF NOT EXISTS content
                        (content_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        content_type TEXT,
                        release_year INTEGER,
                        maturity_rating INTEGER,
                        description TEXT,
                        duration_mins INTEGER,
                        studio_id INTEGER,
                        is_original INTEGER,
                        FOREIGN KEY (studio_id) REFERENCES studio (studio_id))''')
    
    # i'm guessing that codec is text
    cursor.execute ('''CREATE TABLE IF NOT EXISTS video_asset
                        (asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content_id INTEGER,
                        episode_id INTEGER,
                        resolution INTEGER,
                        file_url TEXT,
                        codec TEXT,
                        FOREIGN KEY (content_id) REFERENCES content (content_id)
                        FOREIGN KEY (episode_id) REFERENCES episode (episde_id))''')
    
    # NOTE
    # this is a junction table. notice the syntax
    cursor.execute ('''CREATE TABLE IF NOT EXISTS content_genre
                        (content_id INT,
                        genre_id INTEGER,
                        PRIMARY KEY (content_id , genre_id),
                        FOREIGN KEY (content_id) REFERENCES content (content_id),
                        FOREIGN KEY (genre_id) REFERENCES genre(genre_id)''')
    
    cursor.execute ('''CREATE TABLE IF NOT EXISTS genre
                        (genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        genre_name INTEGER)''')
    
    cursor.execute ('''CREATE TABLE IF NOT EXISTS rating
                        (rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        profile_id INTEGER,
                        content_id INTEGER,
                        rating_value INTEGER,
                        rated_at INTEGER,
                        FOREIGN KEY (profile_id) REFERENCES profile(profile_id)
                        FOREIGN KEY (content_id) REFERENCES content(content_id)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS studio
                    (studio_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    studio_name TEXT,
                    country TEXT))''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS content_person,
                    (content_id INTEGER,
                    person_id INTEGER,
                    role_type TEXT,
                    PRIMARY KEY (content_id , person_id)
                    FOREIGN KEY (content_id) REFERENCES content(content_id)
                    FOREIGN KEY (person_id) REFERENCES person (person_id))''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS person
                    (person_id INTEGER PRIMARY KEY AUTOINCREMENT
                    full_name INTEGER,
                    birth_date INTEGER,
                    nationality TEXT))''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS profile
                    (profile_id INTEGER PRIMARY KEY AUTOINCREMENT
                    account_id INTEGER,
                    profile_name TEXT,
                    avatar_url TEXT,
                    is_kids INTEGER,
                    maturity_rating TEXT,
                    FOREIGN KEY (account_id) REFERENCES account (account_id)
                    FOREIGN KEY (language_id) REFERENCES language(language_id))''')
    
    cursor.execute ('''CREATE TABLE IF NOT EXISTS content_track
                    (track_id INTEGER PRIMARY KEY AUTOINCREMENT
                    content_id INTEGER,
                    language_id INTEGER
                    track_type TEXT,
                    FOREIGN KEY (content_id) REFERENCES content(content_id)
                    FOREIGN KEY (languange_id) REFERENCES language(language_id))''')
    
    cursor.execute ('''CREATE TABLE IF NOT EXISTS language
                    (language_id INTEGER PRIMARY KEY AUTOINCREMENT
                    language_name TEXT,
                    iso_code INTEGER))''')
    
    cursor.execute ('''CREATE TABLE IF NOT EXISTS device
                    (device_id INTEGER PRIMARY KEY AUTOINCREMENT
                    account_id INTEGER,
                    device_type TEXT,
                    device_name TEXT,
                    last_active INTEGER,
                    FOREIGN KEY (account_id) REFERENCES account(account_id))''')
    
    cursor.execute ('''CREATE TABLE IF NOT EXISTS account
                    (account_id INTEGER PRIMARY KEY AUTOINCREMENT
                    email TEXT,
                    password_hash TEXT,
                    created_at INTEGER,
                    account_status TEXT,
                    plan_id INTEGER,
                    country_id INTEGER,
                    preferred_language TEXT,
                    FOREIGN KEY (plan_id) REFERENCES subscription_plan(plan_id))''')
    
    cursor.execute ('''CREATE TABLE IF NOT EXISTS subscription_plan
                    (plan_id INTEGER PRIMARY KEY AUTOINCREMENT
                    plan_name TEXT,
                    price_monthly INTEGER,
                    max_profiles INTEGER,
                    max_simultaneous_streams INTEGER))''')
    
    cursor.execute ('''CREATE TABLE IF NOT EXISTS payment
                    (payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_id INTEGER,
                    amount INTEGER,
                    payment_date INTEGER,
                    payment_method TEXT,
                    status TEXT,
                    plan_id INTEGER
                    FOREIGN KEY (account_id) REFERENCES account(account_id)
                    FOREIGN KEY (plan_id) REFERENCES subscription_plan(plan_id)''')