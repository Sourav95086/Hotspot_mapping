from thematic.supabase_client import supabase


def get_or_create_category(category_name: str):

    category_name = category_name.strip()

    # Fetch existing categories
    response = (
        supabase
        .table("issue_categories")
        .select("category_id, category_name")
        .execute()
    )

    categories = response.data

    # Check whether category already exists
    for category in categories:

        if category["category_name"].lower() == category_name.lower():

            return {
                "category_id": category["category_id"],
                "category_name": category["category_name"],
                "created": False
            }

    # Category does not exist → create it
    response = (
        supabase
        .table("issue_categories")
        .insert({
            "category_name": category_name
        })
        .execute()
    )

    new_category = response.data[0]

    return {
        "category_id": new_category["category_id"],
        "category_name": new_category["category_name"],
        "created": True
    }


def update_city_category_count(city: str, category_id: int):

    # Check if this city + category combination already exists
    response = (
        supabase
        .table("city_category_counts")
        .select("id, report_count")
        .eq("city", city)
        .eq("category_id", category_id)
        .execute()
    )

    existing = response.data

    # --------------------------------
    # EXISTS → INCREMENT COUNT
    # --------------------------------

    if existing:

        row = existing[0]

        new_count = row["report_count"] + 1

        response = (
            supabase
            .table("city_category_counts")
            .update({
                "report_count": new_count
            })
            .eq("id", row["id"])
            .execute()
        )

        return {
            "created": False,
            "city": city,
            "category_id": category_id,
            "report_count": new_count
        }

    # --------------------------------
    # DOES NOT EXIST → CREATE
    # --------------------------------

    response = (
        supabase
        .table("city_category_counts")
        .insert({
            "city": city,
            "category_id": category_id,
            "report_count": 1
        })
        .execute()
    )

    row = response.data[0]

    return {
        "created": True,
        "city": city,
        "category_id": category_id,
        "report_count": row["report_count"]
    }