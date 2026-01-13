import tmdbsimple as tmdb
from datetime import datetime, timedelta
from plexflow.core.metadata.providers.imdb.imdb import search_movie_by_imdb
import os

def get_complete_release_report(imdb_id):
    tmdb.API_KEY = os.getenv('TMDB_API_KEY')

    imdb_movie = search_movie_by_imdb(imdb_id=imdb_id)

    # 1. Map IMDb ID to TMDB Metadata
    find = tmdb.Find(imdb_id)
    find_res = find.info(external_source='imdb_id')
    
    if not find_res['movie_results']:
        return {"error": "IMDb ID not found in TMDB."}

    m_meta = find_res['movie_results'][0]
    movie_id = m_meta['id']
    
    # movie.info() gets the 'budget' field; movie.release_dates() gets the types
    movie = tmdb.Movies(movie_id)
    details = movie.info() 
    releases_data = movie.release_dates()

    # 2. Extract Key Financial & Social Metrics
    budget = details.get('budget', 0)
    pop = details.get('popularity', 0)
    votes = details.get('vote_count', 0)

    # 3. Map All Release Types (1-6)
    type_map = {
        1: 'premiere',
        2: 'theatrical_limited',
        3: 'theatrical',
        4: 'digital',
        5: 'physical',
        6: 'tv'
    }
    
    # Store the earliest date found globally for each type
    found_dates = {v: None for v in type_map.values()}
    for country in releases_data['results']:
        for r in country['release_dates']:
            rtype = r.get('type')
            if rtype in type_map:
                key = type_map[rtype]
                dt = datetime.strptime(r['release_date'][:10], '%Y-%m-%d')
                if found_dates[key] is None or dt < found_dates[key]:
                    found_dates[key] = dt

    # 4. Calculate Dynamic Safety Buffer
    # Higher Budget/Popularity = Longer theatrical exclusivity
    if budget >= 150_000_000 or pop > 1500 or votes > 5000 or (imdb_movie and imdb_movie.rank < 50):
        buffer_days = 120  # Tentpole / Blockbuster
    elif budget >= 50_000_000 or pop > 500 or (imdb_movie and imdb_movie.rank >= 50 and imdb_movie.rank < 100):
        buffer_days = 90   # Mainstream
    else:
        buffer_days = 45   # Indie / Niche

    # 5. Final Safe Date Priority Logic
    if found_dates['digital']:
        # If Digital exists, use it + 2 days (standard Scene upload delay)
        safe_date = found_dates['digital'] + timedelta(days=2)
    elif found_dates['physical']:
        # If Digital is missing, Physical is the fallback
        safe_date = found_dates['physical'] - timedelta(days=7)
    elif found_dates['theatrical']:
        # Use our calculated buffer if no home-media dates are known
        safe_date = found_dates['theatrical'] + timedelta(days=buffer_days)
    else:
        safe_date = None

    return {
        "title": details.get('title'),
        "metrics": {"budget": budget, "popularity": pop, "votes": votes},
        "all_dates": found_dates,
        "safe_date": safe_date,
        "buffer_used": buffer_days,
        "imdb_rank": imdb_movie.rank if imdb_movie else -1,
        "imdb_votes": imdb_movie.votes if imdb_movie else -1,
    }

if __name__ == '__main__':
    # --- Execution ---
    report = get_complete_release_report('tt33028778') # Avatar: Fire and Ash

    if report:
        print(f"REPORT: {report['title']}")
        print(f"Metrics: Budget: ${report['metrics']['budget']:,} | Pop: {report['metrics']['popularity']:.0f} | Votes: {report['metrics']['votes']} | IMDb rank: {report['imdb_rank']} | IMDb votes: {report['imdb_votes']}")
        print("-" * 50)
        
        # Print every date found
        for r_type, dt in report['all_dates'].items():
            dt_str = dt.strftime('%Y-%m-%d') if dt else "Not Listed"
            print(f"{r_type.replace('_', ' ').title():<20} : {dt_str}")
        
        print("-" * 50)
        if report['safe_date']:
            safe_str = report['safe_date'].strftime('%Y-%m-%d')
            print(f"VERIFIED SAFE DATE   : {safe_str} (Using {report['buffer_used']}-day buffer)")
            
            if datetime.now() < report['safe_date']:
                print("STATUS               : 🚩 FAKE ALERT - Any 'BluRay' torrent is a scam.")
            else:
                print("STATUS               : ✅ SAFE - Legitimate high-quality files may exist.")