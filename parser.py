import math
from pathlib import Path
import re
import json
import pandas as pd
import datetime as dt

dt_now = dt.datetime.now().strftime("%Y-%m-%d")

def load_html(path: Path) -> str:
    print(path)
    with open(path, "r", encoding="UTF-8") as file:
        html = file.read()
    return html

def parse_score(score):
    try:
        return int(score)
    except ValueError:
        return None

def extract_review_blocks(html: str) -> list:
    # Get all matches in raw data
    pattern = r'<li .*?><span class="mr-3 text-gray-800 w-40 text-md">(.*?)</span><span.*?>(－|\d+)</span></li>'
    block_match = re.search(r'itemtype="https://schema.org/Person"(.*?)クチコミの件数、スコアは一休', html, re.DOTALL)
    raw_matches = None
    if block_match:
        block = block_match.group(1)
        raw_matches = re.findall(pattern, block)
    if len(raw_matches) % 6 != 0:
        print("Warning! Not divisible by 6")

    post_dates = re.findall(r"投稿日[:：]\s*(\d{4}/\d{1,2}/\d{1,2})", html, re.DOTALL)
    post_date_dict = []
    for date in post_dates:
        new_date = {"postDate": date}
        post_date_dict.append(new_date)

    # Translation dict
    rating_labels_map = {
    "客室・アメニティ": "roomAmenityRating",
    "施設・設備": "equipmentRating",
    "接客・サービス": "customerServiceRating",
    "お食事": "mealRating",
    "温泉・お風呂": "bathroomSpringRating",
    "満足度": "satisfactionRating"
}
    filter_matches = [(label, score) for label, score in raw_matches if label in rating_labels_map]
    # Slices all results into 6 key:value dicts.
    clean_matches = [filter_matches[6*i:6*i+6] for i in range(0,math.ceil(len(filter_matches)/6))]
    reviews_list = []
    for match in clean_matches:
        # Starts a default dict for all keys and gives them a None value.
        review = {key: None for key in rating_labels_map.values()}
        for label_jp, score in match:
            if label_jp not in rating_labels_map:
                print(f"Warning! label expected not found: {label_jp}")
            review[rating_labels_map[label_jp]] = parse_score(score)
        reviews_list.append(review)

    all_keys = set(rating_labels_map.values())
    for i, review in enumerate(reviews_list):
        if set(review.keys()) != all_keys:
            print(f"Review {i} Missing or unexpected label!: {review.keys()}")
    final_list = []
    for date, review in zip(post_date_dict, reviews_list):
        # Inserts date, total score and review category scores into a list of dictionaries.
        valid_scores = [value for value in review.values() if value is not None]
        if valid_scores:
            average = sum(valid_scores) / len(valid_scores)
        else:
            average = None
        average_rating = {"totalRating": average}
        new_dict = {}
        new_dict.update(date)
        new_dict.update(average_rating)
        new_dict.update(review)
        final_list.append(new_dict)
    return final_list


def save_json(data: list, io_path: Path, page: int):
    output_path = io_path / "json"
    output_path.mkdir(exist_ok=True)
    target_filename = output_path / f"ikyu-review-p{page + 1}.json"

    with target_filename.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def save_dataframe(data: list, output_path: Path):
    output_path = output_path / f"ikyu_reviews.csv"
    df = pd.DataFrame(data)
    df["postDate"] = pd.to_datetime(df["postDate"])
    df.to_csv(output_path, index=False)

def get_path():
    output_path = Path(__file__).parent / "parsed_files"
    output_path.mkdir(exist_ok=True)
    target_path = output_path / dt_now
    target_path.mkdir(exist_ok=True)
    return target_path


def main():
    df_dict = []
    io_path = get_path()

    for page in range(13):
        input_path = io_path / "html" / f"ikyu-review-p{page + 1}.html"

        html = load_html(input_path)
        reviews = extract_review_blocks(html)
        save_json(reviews, io_path, page)
        df_dict.append(reviews)

        print(f"{len(reviews)} reviews extracted.")
    # Stabilizes the list of lists of dictionaries into one list of dictionaries.
    df_dict = [inner for outer in df_dict for inner in outer]
    save_dataframe(df_dict, io_path)

if __name__ == "__main__":
    main()
