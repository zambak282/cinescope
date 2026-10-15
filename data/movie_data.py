from utils.data_generator import DataGenerator


def build_movie_payload(
        *,
        name: str | None = None,
        image_url: str = "https://image.url",
        price: int | None = None,
        description: str | None = None,
        location: str = "MSK",
        published: bool = True,
        genre_id: int = 5,
        **kwargs,
) -> dict:
    payload = {
        "name": name or DataGenerator.generate_random_movie_name(),
        "imageUrl": image_url,
        "price": price if price is not None else DataGenerator.generate_random_movie_price(),
        "description": description or DataGenerator.generate_random_movie_description(),
        "location": location,
        "published": published,
        "genreId": genre_id,
    }
    payload.update(kwargs)
    return payload