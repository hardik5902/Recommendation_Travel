recommended_place_info = {
            "name": place,
            "latitude": recommended_place["lat"].values[0],
            "longitude": recommended_place["lng"].values[0],
            "image_url": recommended_place["ImageUrl"].tolist()
        }