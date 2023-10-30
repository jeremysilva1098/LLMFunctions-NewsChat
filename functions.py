functions = [
    {
        "name": "get_news_by_keyword",
        "description": "Get the latest news articles by keyword",
        "parameters": {
            "type": "object",
            "properties": {"keywords": {
                "type": "string",
                "description": '''
                Keywords or phrases to search for in the article title and body
                Advanced search is supported here:
                * Surround phrases with quotes (") for exact match.
                * Prepend words or phrases that must appear with a + symbol. Eg: +bitcoin
                * Prepend words that must not appear with a - symbol. Eg: -bitcoin
                * Alternatively you can use the AND / OR / NOT keywords, and optionally group these with parenthesis. Eg: crypto AND (ethereum OR litecoin) NOT bitcoin.
                The complete value for q must be URL-encoded. Max length: 500 chars.
                '''
            }
            }
        }
    },
    {
        "name": "get_top_headlines_by_topic",
        "description": "Get the top headlines by topic",
        "parameters": {
            "type": "object",
            "properties": {"topic": {
                "type": "string",
                "enum": ["business", "entertainment", "general", "health", "science", "sports", "technology"],
                "description": "The category for which you want to get headlines for."
            }}
        }
    }
]