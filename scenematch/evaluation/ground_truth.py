def ground_truth() -> dict:
    """
    Returns a dictionary mapping query string to list of actual relevant movie UUIDs.
    """
    # Map movie titles (or keys you used) to actual UUIDs from your dataset
    id_map = {
        "notebook": "7a8f53d3-6d2e-4bb9-b20e-5e77ea45f945",
        "pride_prejudice": "8b3a6c19-41a9-41f8-9252-8f66b1a1f845",
        "la_la_land": "f00f4234-6a5e-40f0-8d54-0cbf09795125",
        "titanic": "c2d1f29a-1b63-4b67-b1e4-8a9eaa45ec15",
        "call_me_by_your_name": "f65a6d74-2bf0-42e4-8d25-4ec3a3df4f1e",
        "fault_in_our_stars": "e925a96b-d734-49e5-9c4e-64f540bca132",
        "se7en": "b76eaa9e-9a77-4444-8757-bdc18b6cd3e0",
        "gone_girl": "1c7f8e9e-7c81-4c13-b7ca-956d3f82a94c",
        "prisoners": "d3b01e92-0e1c-4a15-9fa7-1bb4ae70543f",
        "zodiac": "c415ba7b-5bf7-48a7-b4c1-3b8a4acb43da",
        "shutter_island": "aa49d1c8-10e2-4e14-9f32-c29ea3d30768",
        "lion_king": "6a7bb3c0-2e18-4d21-a5d7-f62d938c65f4",
        "harry_potter": "e3eae01f-1d8c-4f90-91d7-1b2f94d81e8c",
        "narnia": "2f7f8e7d-6e23-4d67-8341-909d84d77a16",
        "inception": "replace_with_actual_id",
        "interstellar": "replace_with_actual_id",
        "truman_show": "replace_with_actual_id",
        "matrix": "replace_with_actual_id",
        "lotr": "e6b9e3da-cbae-4bfb-8b3e-2272b2dfe9c7",
        "hobbit": "a1d4e3fc-3f24-48a8-9f4a-5b67e324a76a",
        "pirates": "3d71d194-710d-44c3-9e0b-fcfcf4e3d4f3",
        "forrest_gump": "9bc4eaae-f632-4a2f-9288-54de8a5f782d",
        "whiplash": "2f5c8e2b-17a3-45b9-80dd-c3e9b2b4bc65",
        # Add other needed mappings here...
    }

    ground_truth_list = [
        {
            "query": "I just went through a breakup. I want something emotional and romantic.",
            "relevant_ids": [
                id_map["notebook"],
                id_map["call_me_by_your_name"],
                id_map["la_la_land"],
                id_map["pride_prejudice"],
                id_map["fault_in_our_stars"]
            ]
        },
        {
            "query": "I need something that gives me hope or motivation.",
            "relevant_ids": [
                id_map["forrest_gump"],
                id_map["lion_king"],
                id_map["whiplash"]
            ]
        },
        {
            "query": "Give me something intense to distract me — like a thriller.",
            "relevant_ids": [
                id_map["se7en"],
                id_map["gone_girl"],
                id_map["prisoners"],
                id_map["zodiac"],
                id_map["shutter_island"]
            ]
        },
        {
            "query": "I want something comforting and nostalgic.",
            "relevant_ids": [
                id_map["lion_king"],
                id_map["harry_potter"],
                id_map["narnia"],
                id_map["spirited_away"] if "spirited_away" in id_map else "replace_with_id"
            ]
        },
        {
            "query": "I want something that makes me question reality or life.",
            "relevant_ids": [
                id_map["inception"],
                id_map["shutter_island"],
                id_map["interstellar"],
                id_map["truman_show"],
                id_map["matrix"]
            ]
        },
        {
            "query": "I loved Titanic — give me something similar.",
            "relevant_ids": [
                id_map["titanic"],
                id_map["notebook"],
                id_map["pride_prejudice"],
                id_map["la_la_land"]
            ]
        },
        {
            "query": "I want a fantasy adventure like The Lord of the Rings.",
            "relevant_ids": [
                id_map["lotr"],
                id_map["hobbit"],
                id_map["harry_potter"],
                id_map["narnia"],
                id_map["pirates"]
            ]
        }
    ]

    # Convert list of dicts to dict mapping query -> relevant_ids
    return {item["query"]: item["relevant_ids"] for item in ground_truth_list}
