import json
import os
import re
import urllib.parse
from datetime import UTC, datetime
from typing import Any

import psycopg  # type: ignore
import requests
from bs4 import BeautifulSoup, Comment

# custom type list[dict[str, Any]]
list_dict = list[dict[str, Any]]


# Function to generate a unique slug for a given text
def slugify_text(text: str) -> str:
    # Remove non-alphanumeric characters and convert to lowercase
    slug = re.sub(r"[^\w\s-]", "", text.lower())

    # Replace spaces with underscores
    slug = slug.replace(" ", "_")

    # Remove consecutive underscores
    slug = re.sub(r"_{2,}", "_", slug)

    # Remove leading and trailing underscores
    slug = slug.strip("_")

    return slug


# If the slug is already in the set, add a number to the end
# Example, if "hello-world" is already in the set, the next slug will be "hello-world-2"
# If "hello-world-2" is also in the set, the next slug will be "hello-world-3"
def dynamic_slugify(text: str, slugs: set[str]) -> str:
    slug = slugify_text(text)

    # URL encode the slug with UTF-8 encoding
    encoded_slug = urllib.parse.quote(slug.encode("utf-8"), safe="")

    # if the slug is already in the set, add a number to the end
    if encoded_slug in slugs:
        num = 2

        # keep incrementing the number until the slug is unique
        while f"{encoded_slug}-{num}" in slugs:
            num += 1

        encoded_slug = f"{encoded_slug}-{num}"

    return encoded_slug


def get_wikinews_articles() -> list_dict:
    print(f"Function get_wikinews_articles Started At: {datetime.now(UTC).isoformat()}")

    try:
        date = datetime.now(UTC).strftime("%Y/%m/%d")
        print(f"UTC Date: {date}")

        url = "https://api.wikimedia.org/feed/v1/wikipedia/en/featured/" + date

        headers = {
            "User-Agent": os.environ.get("APP_NAME"),
            "Authorization": os.environ.get("ACCESS_TOKEN"),
        }

        response = requests.get(url, headers=headers)
        print(f"Wikinews Response Status Code: {response.status_code}")

        response_json = response.json()
        resp_news: list_dict = response_json.get("news", [])

        print(f"Fetched News Article(s): {len(resp_news)}")
        return resp_news
    except requests.exceptions.RequestException as e:
        print(f"Func get_wikinews_articles Request Error: {e}")
    except json.JSONDecodeError as e:
        print(f"Func get_wikinews_articles JSON Error: {e}")
    except Exception as e:
        print(f"Func get_wikinews_articles Error: {e}")

    return []


def get_news_objects(data: list_dict) -> list_dict:
    print(f"Function get_news_objects Started At: {datetime.now(UTC).isoformat()}")

    try:
        news = []

        for item in data:
            if item.get("story"):
                soup = BeautifulSoup(item["story"], "html.parser")

                # Remove all comments
                comments = soup.find_all(string=lambda text: isinstance(text, Comment))
                for comment in comments:
                    comment.extract()

                # In <a> tags, replace the href attribute with the correct URL and remove all other attributes
                a_tags = soup.find_all("a")
                for a_tag in a_tags:
                    check = False

                    for url_title in item.get("links", []):
                        if url_title.get("title") == a_tag["href"][2:]:
                            check = True

                            a_tag.attrs = {}
                            a_tag["href"] = (
                                url_title.get("content_urls", {})
                                .get("desktop", {})
                                .get("page")
                            )

                            break

                    if not check:
                        a_tag.extract()

                # Remove attributes from all tags except for <a> tags
                for tag in soup.find_all():
                    if tag.name != "a":
                        tag.attrs = {}

                title = soup.prettify().replace("(pictured)", "").strip()
                title_text = re.sub(
                    " +", " ", soup.text.replace("(pictured)", "").strip()
                )

                news.append(
                    {
                        "title": title,
                        "title_text": title_text,
                        "wiki_title_raw": item["story"],
                        "details": [
                            {
                                "wiki_tid": item.get("tid"),
                                "summary": item.get("titles", {}).get("normalized"),
                                "description": item.get("description"),
                                "thumbnail": item.get("thumbnail", {}).get("source"),
                                "image": item.get("originalimage", {}).get("source"),
                                "timestamp": item.get("timestamp"),
                                "url": item.get("content_urls", {})
                                .get("desktop", {})
                                .get("page"),
                            }
                            for item in item.get("links", [])
                            if item.get("lang", "") == "en"
                        ],
                    }
                )

        print(f"News Article(s) Processed: {len(news)}")
        return news
    except KeyError as e:
        print(f"Func get_news_objects KeyError: {e}")
    except Exception as e:
        print(f"Func get_news_objects Error: {e}")

    return []


def insert_news_to_db(news: list_dict) -> bool:
    print(f"Function insert_news_to_db Started At: {datetime.now(UTC).isoformat()}")

    try:
        with psycopg.connect(
            f"host={os.environ.get('DB_HOST')} "
            f"port={os.environ.get('DB_PORT')} "
            f"dbname={os.environ.get('DB_NAME')} "
            f"user={os.environ.get('DB_USER')} "
            f"password={os.environ.get('DB_PASS')}"
        ) as conn:
            count = 0

            with conn.cursor() as cur:
                wiki_title_raw = set()
                existing_slugs = set()

                for record in cur.execute(
                    "SELECT wiki_title_raw, slug FROM news"
                ).fetchall():
                    wiki_title_raw.add(record[0])
                    existing_slugs.add(record[1])

                for item in news:
                    # Check if the wiki_title_raw is already in the database
                    # Only insert if it is not already in the database
                    if item["wiki_title_raw"] not in wiki_title_raw:
                        try:
                            slug = dynamic_slugify(item["title_text"], existing_slugs)

                            cur.execute(
                                """
                                INSERT INTO news (title, title_text, wiki_title_raw, slug)
                                VALUES (%s, %s, %s, %s)
                                RETURNING id
                                """,
                                (
                                    item["title"],
                                    item["title_text"],
                                    item["wiki_title_raw"],
                                    slug,
                                ),
                            )

                            # Get the news_id of the inserted record
                            # This will be used to insert the details
                            result = cur.fetchone()

                            if result:
                                news_id = result[0]

                                for detail in item["details"]:
                                    cur.execute(
                                        """
                                        INSERT INTO news_detail (
                                            wiki_tid, summary, description, thumbnail, image, timestamp, url, news_id
                                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                        """,
                                        (
                                            detail["wiki_tid"],
                                            detail["summary"],
                                            detail["description"],
                                            detail["thumbnail"],
                                            detail["image"],
                                            detail["timestamp"],
                                            detail["url"],
                                            news_id,
                                        ),
                                    )

                                conn.commit()
                                count += 1
                        except psycopg.errors.ConnectionException as e:
                            print(
                                f"Func insert_news_to_db PostgreSQL Connection Error: {e}"
                            )
                            conn.rollback()
                        except psycopg.errors.UniqueViolation as e:
                            print(
                                f"Func insert_news_to_db PostgreSQL Uniqueness Error: {e}"
                            )
                            conn.rollback()
                        except psycopg.errors.NotNullViolation as e:
                            print(
                                f"Func insert_news_to_db PostgreSQL NotNull Error: {e}"
                            )
                            conn.rollback()
                        except psycopg.Error as e:
                            print(f"Func insert_news_to_db PostgreSQL Error: {e}")
                            conn.rollback()
                        except Exception as e:
                            print(
                                f"Func insert_news_to_db Error (during loop iteration): {e}"
                            )
                            conn.rollback()

        print(f"News Article(s) Inserted: {count}")
        return True
    except Exception as e:
        print(f"Func insert_news_to_db Error: {e}")

    return False


def lambda_handler(event: Any = None, context: Any = None) -> None:
    print(f"Function Started At: {datetime.now(UTC).isoformat()}")

    data: list_dict = get_wikinews_articles()
    news: list_dict = get_news_objects(data)
    status: bool = insert_news_to_db(news)

    print(f"Success: {status}")

    print(f"Function Ended At: {datetime.now(UTC).isoformat()}")
    return
