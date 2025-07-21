import json

# Paste in all of your scenarios and their 50 titles each:
scenario_titles = {
    "best movie": [
        "The Shawshank Redemption", "The Godfather", "Parasite",
        "The Dark Knight", "The Lord of the Rings: The Return of the King",
        "Fight Club", "Pulp Fiction", "Interstellar", "Forrest Gump",
        "Inception", "The Matrix", "Se7en", "Coco", "Spirited Away",
        "Whiplash", "The Intouchables", "The Green Mile",
        "Léon: The Professional", "The Lord of the Rings: The Fellowship of the Ring",
        "The Lord of the Rings: The Two Towers", "Saving Private Ryan",
        "Gladiator", "The Lion King", "Back to the Future", "Memento",
        "Shutter Island", "The Prestige", "The Departed", "Star Wars",
        "Titanic", "Joker", "Django Unchained", "The Wolf of Wall Street",
        "Avengers: Infinity War", "Avengers: Endgame", "Mad Max: Fury Road",
        "Guardians of the Galaxy", "Avatar", "Deadpool",
        "Harry Potter and the Deathly Hallows: Part 2",
        "Spider-Man: Into the Spider-Verse", "The Shining", "Schindler's List",
        "WALL·E", "Up", "Inside Out", "La La Land", "Arrival"
    ],
    "underrated movie": [
        "Suicide Squad", "Batman v Superman: Dawn of Justice", "Lucy",
        "Thor: The Dark World", "Star Wars: Episode I – The Phantom Menace",
        "Man of Steel", "Jurassic World", "Captain Marvel", "Thor",
        "The Hunger Games: Mockingjay - Part 1", "Venom", "Ready Player One",
        "The Maze Runner", "World War Z", "Pacific Rim", "Justice League",
        "Transformers: Age of Extinction", "The Amazing Spider-Man",
        "Independence Day: Resurgence", "The Dark Tower", "The Meg",
        "Rampage", "Gods of Egypt", "Battleship", "The Great Wall",
        "The Mummy (2017)", "Terminator Genisys", "Resident Evil: The Final Chapter",
        "Assassin's Creed", "G.I. Joe: Retaliation", "X-Men: Apocalypse",
        "Divergent", "The Last Airbender", "Ghostbusters (2016)",
        "Goosebumps", "Warcraft", "Cars 2", "The Da Vinci Code",
        "Now You See Me 2", "Maleficent", "The Incredible Hulk",
        "Pirates of the Caribbean: On Stranger Tides",
        "Star Wars: The Last Jedi", "Ant-Man and the Wasp",
        "X-Men: Dark Phoenix", "Thor: Love and Thunder",
        "Fantastic Beasts: The Crimes of Grindelwald",
        "The Hunger Games: Mockingjay - Part 2", "Star Wars: The Rise of Skywalker"
    ],
    "best movie in the 90s": [
        "The Shawshank Redemption", "Pulp Fiction", "Fight Club",
        "Forrest Gump", "Se7en", "The Lion King", "The Green Mile",
        "The Matrix", "GoodFellas", "Schindler's List",
        "Saving Private Ryan", "The Silence of the Lambs",
        "Terminator 2: Judgment Day", "Groundhog Day", "Jurassic Park",
        "Braveheart", "Heat", "Toy Story", "American Beauty",
        "The Truman Show", "The Big Lebowski", "Fargo", "Léon: The Professional",
        "Casino", "Scream", "Point Break", "The Fugitive", "Before Sunrise",
        "True Lies", "The Usual Suspects", "The Sixth Sense", "Donnie Brasco",
        "Jerry Maguire", "Sleepless in Seattle", "Independence Day",
        "Edward Scissorhands", "Babe", "Men in Black", "Beauty and the Beast",
        "Mrs. Doubtfire", "Aladdin", "Apollo 13", "Speed", "A Few Good Men",
        "Clueless", "Rush Hour", "Notting Hill", "The Fifth Element", "Titanic"
    ],
    "best new movie": [
        "Spider-Man: No Way Home", "Dune", "No Time to Die", "A Quiet Place Part II",
        "Soul", "Tenet", "1917", "Parasite", "Joker", "Ford v Ferrari",
        "Avengers: Endgame", "Knives Out", "Jojo Rabbit",
        "Once Upon a Time… in Hollywood", "Toy Story 4",
        "Spider-Man: Far From Home", "Us", "A Star Is Born", "Green Book",
        "Bohemian Rhapsody", "Black Panther", "Coco", "Blade Runner 2049",
        "Logan", "La La Land", "Arrival", "Hacksaw Ridge", "Zootopia",
        "Inside Out", "Mad Max: Fury Road", "Get Out", "Baby Driver",
        "The Shape of Water", "Doctor Strange", "Ready Player One", "Dunkirk",
        "Spider-Man: Homecoming", "Wonder Woman", "Split",
        "Kingsman: The Secret Service", "John Wick", "The Revenant",
        "The Martian", "Guardians of the Galaxy Vol. 2", "Big Hero 6",
        "Interstellar", "The Dark Knight Rises", "Whiplash", "Frozen II"
    ],
    "family-friendly animated classics": [
        "Spirited Away", "Coco", "The Lion King", "WALL·E", "Inside Out",
        "Toy Story", "Up", "Ratatouille", "How to Train Your Dragon",
        "Finding Nemo", "Toy Story 3", "Zootopia", "The Incredibles",
        "Frozen", "Tangled", "Monsters, Inc.", "Shrek", "Shrek 2",
        "The Iron Giant", "Lilo & Stitch", "Big Hero 6", "Moana",
        "The Prince of Egypt", "Brave", "The Little Mermaid",
        "Beauty and the Beast", "Aladdin", "Mulan", "Kubo and the Two Strings",
        "Kung Fu Panda", "Despicable Me", "Raya and the Last Dragon",
        "The Boss Baby", "Rio", "Happy Feet", "The Croods",
        "Cloudy with a Chance of Meatballs", "Madagascar", "Ice Age",
        "Sing", "Bolt", "Puss in Boots", "Peter Pan", "The Jungle Book",
        "Bambi", "Dumbo", "Pocahontas", "Hercules", "The Fox and the Hound"
    ],
    "space-exploration epics": [
        "Interstellar", "The Martian", "Gravity", "Avatar", "Star Wars",
        "The Empire Strikes Back", "Return of the Jedi",
        "Rogue One: A Star Wars Story", "Guardians of the Galaxy",
        "Guardians of the Galaxy Vol. 2", "Avengers: Infinity War",
        "Avengers: Endgame", "Captain Marvel", "Dune", "Ad Astra",
        "Arrival", "Star Wars: The Force Awakens", "Star Wars: The Last Jedi",
        "Thor: Ragnarok", "Thor", "Galaxy Quest", "Serenity", "Passengers",
        "Ender's Game", "Prometheus", "Star Trek", "Star Trek Into Darkness",
        "First Man", "Moon", "Apollo 13", "2001: A Space Odyssey",
        "Europa Report", "Life", "The Wandering Earth", "Hidden Figures",
        "Valerian and the City of a Thousand Planets", "Elysium", "Oblivion",
        "Total Recall", "The Midnight Sky", "Sunshine", "Contact",
        "Event Horizon", "Cosmos", "Mission to Mars", "Battlefield Earth",
        "Edge of Tomorrow", "WALL·E", "Space Cowboys", "Planet 51"
    ],
    "mind-bending thrillers": [
        "Inception", "Shutter Island", "The Matrix", "Memento", "Fight Club",
        "Se7en", "The Prestige", "Black Swan", "Gone Girl", "Split", "Joker",
        "Get Out", "The Shining", "Interstellar", "Donnie Darko",
        "Eternal Sunshine of the Spotless Mind", "Source Code",
        "Predestination", "Primer", "Looper", "Tenet", "The Machinist",
        "Mulholland Drive", "Oldboy", "The Usual Suspects", "American Psycho",
        "The Sixth Sense", "The Butterfly Effect", "Vanilla Sky",
        "The Game", "12 Monkeys", "Edge of Tomorrow", "The Truman Show",
        "Dark City", "Under the Skin", "Annihilation", "A Beautiful Mind",
        "Reservoir Dogs", "Prisoners", "Zodiac", "Insomnia", "Chronicle",
        "Limitless", "Paprika", "Total Recall", "We Need to Talk About Kevin",
        "Enemy", "Requiem for a Dream", "Cloud Atlas", "Triangle"
    ],
    "feel-good comfort watches": [
        "Forrest Gump", "The Intouchables", "Up", "Inside Out", "Coco",
        "Toy Story", "Toy Story 3", "The Lion King", "Spirited Away",
        "Finding Nemo", "Ratatouille", "How to Train Your Dragon", "Moana",
        "Monsters, Inc.", "The Grand Budapest Hotel", "La La Land",
        "Paddington", "Paddington 2", "The Princess Bride",
        "Little Miss Sunshine", "Amélie", "Chef",
        "Soul", "The Secret Life of Walter Mitty", "Sing Street",
        "School of Rock", "Pitch Perfect", "Yes Man", "Legally Blonde",
        "Juno", "Bend It Like Beckham", "The Lego Movie", "Zootopia",
        "Shrek", "Big Hero 6", "About Time", "500 Days of Summer",
        "Julie & Julia", "Hunt for the Wilderpeople", "Mamma Mia!",
        "The Peanut Butter Falcon", "The Mitchells vs. the Machines",
        "Harry Potter and the Philosopher's Stone", "Matilda", "Enchanted",
        "Hairspray", "Freaky Friday", "A Knight’s Tale", "We Bought a Zoo"
    ],
    "based on a true story": [
        "Schindler's List", "12 Years a Slave", "The Imitation Game",
        "Catch Me If You Can", "The Wolf of Wall Street", "Hidden Figures",
        "Hacksaw Ridge", "The Revenant", "Spotlight", "Bohemian Rhapsody",
        "The Social Network", "Moneyball", "The Big Short",
        "Dallas Buyers Club", "BlacKkKlansman", "A Beautiful Mind",
        "The Theory of Everything", "American Sniper", "Ford v Ferrari",
        "Rush", "Remember the Titans", "Hotel Rwanda", "Erin Brockovich",
        "Apollo 13", "Argo", "Into the Wild", "Rocketman", "Lion",
        "The King’s Speech", "Walk the Line", "127 Hours", "Sully",
        "Invictus", "The Pursuit of Happyness", "Unbroken",
        "The Disaster Artist", "The Blind Side", "Cinderella Man",
        "Captain Phillips", "Milk", "Ray", "The Pianist", "Bridge of Spies",
        "Darkest Hour", "The Last King of Scotland", "The Founder",
        "Remember", "Respect", "Coach Carter", "Gorillas in the Mist"
    ],
    "post-apocalyptic & dystopian futures": [
        "Mad Max: Fury Road", "The Matrix", "Blade Runner 2049",
        "Interstellar", "I Am Legend", "Snowpiercer", "WALL·E", "Ready Player One",
        "World War Z", "The Road", "Children of Men", "A Quiet Place",
        "A Quiet Place Part II", "Edge of Tomorrow", "Oblivion", "Elysium",
        "District 9", "The Book of Eli", "The Hunger Games",
        "The Hunger Games: Catching Fire", "The Hunger Games: Mockingjay - Part 1",
        "The Hunger Games: Mockingjay - Part 2", "Dune", "28 Days Later",
        "28 Weeks Later", "Dredd", "V for Vendetta", "Divergent", "Insurgent",
        "Alita: Battle Angel", "The Maze Runner", "Maze Runner: The Scorch Trials",
        "Maze Runner: The Death Cure", "Terminator 2: Judgment Day",
        "Terminator: Dark Fate", "Planet of the Apes", "Rise of the Planet of the Apes",
        "Dawn of the Planet of the Apes", "War for the Planet of the Apes",
        "Waterworld", "Escape from New York", "Resident Evil",
        "Resident Evil: Apocalypse", "I, Robot", "Gattaca", "Logan",
        "A.I. Artificial Intelligence", "The Midnight Sky", "Love and Monsters"
    ],
    "big plot-twist thrillers": [
        "Fight Club", "Se7en", "The Usual Suspects", "Gone Girl",
        "Shutter Island", "Memento", "The Sixth Sense", "The Prestige",
        "Oldboy", "Prisoners", "Zodiac", "Split", "Arrival", "Donnie Darko",
        "The Others", "12 Monkeys", "Predestination", "Coherence", "Triangle",
        "The Game", "Identity", "The Machinist", "The Girl with the Dragon Tattoo",
        "Insomnia", "The Invisible Guest", "The Departed", "Mulholland Drive",
        "Secret Window", "The Butterfly Effect", "The Invitation",
        "Lucky Number Slevin", "Primal Fear", "Source Code", "Perfect Stranger",
        "Nocturnal Animals", "Side Effects", "Basic Instinct", "Atonement",
        "Arlington Road", "Ambush", "Upgrade", "The Handmaiden", "Wind River",
        "Nightcrawler", "Enemy", "Cloud Atlas", "Collateral Beauty",
        "The Village", "Remember Me"
    ],
    "women-led action & adventure": [
        "Wonder Woman", "Captain Marvel", "Rogue One: A Star Wars Story",
        "The Hunger Games", "The Hunger Games: Catching Fire",
        "Kill Bill: Vol. 1", "Kill Bill: Vol. 2", "Lucy", "Mad Max: Fury Road",
        "Atomic Blonde", "Mulan", "Moana", "Star Wars: The Last Jedi",
        "Star Wars: The Rise of Skywalker", "Alita: Battle Angel",
        "Edge of Tomorrow", "Tomb Raider", "Black Widow", "Birds of Prey",
        "Terminator 2: Judgment Day", "Alien", "Aliens", "G.I. Jane", "Salt",
        "Resident Evil", "Underworld", "Lara Croft: Tomb Raider", "Divergent",
        "Wonder Woman 1984", "The Old Guard", "Red Sparrow", "Colombiana",
        "Peppermint", "Annihilation", "Zootopia", "Frozen", "Brave",
        "Guardians of the Galaxy Vol. 2", "Knives Out", "Ocean’s 8",
        "Sucker Punch", "Hanna", "Haywire", "Nikita", "Upgrade", "Kick-Ass",
        "Snow White and the Huntsman", "The 355", "A Wrinkle in Time",
        "Captain Marvel 2"
    ]
}

# Load movies.json once and build a title→UUID lookup
with open("movies.json", encoding="utf-8") as f:
    movies = json.load(f)
title_to_uuid = {m["title"]: m["id"] for m in movies}

# Translate each scenario’s titles into UUIDs
ground_truth_ids = {
    scenario: [
        title_to_uuid[title]
        for title in titles
        if title in title_to_uuid
    ]
    for scenario, titles in scenario_titles.items()
}

# Dump to JSON for direct consumption
with open("ground_truth_ids.json", "w", encoding="utf-8") as f:
    json.dump(ground_truth_ids, f, indent=2)

# Now ground_truth_ids.json contains, for every scenario, an array of the 50 UUIDs.
# You can load it in your evaluator and cast each list to set(...) for O(1) membership tests.
