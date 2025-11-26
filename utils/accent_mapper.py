"""
Accent Normalization for Ghanaian English
Maps common Ghanaian accent variations to standard English words
"""

# 200+ accent mappings for Ghanaian English
ACCENT_MAP = {
    # Cart/Shopping related
    "cut": "cart",
    "cot": "cart",
    "cats": "cart",
    "kot": "cart",
    "kart": "cart",
    "kat": "cart",
    
    # Shoes/Footwear
    "snekas": "sneakers",
    "sneekas": "sneakers",
    "sneakaz": "sneakers",
    "shuz": "shoes",
    "shooz": "shoes",
    "shoos": "shoes",
    "sandas": "sandals",
    "sandalz": "sandals",
    "slippas": "slippers",
    "slipaz": "slippers",
    
    # Common words
    "fo": "for",
    "foh": "for",
    "dis": "this",
    "diz": "this",
    "dat": "that",
    "dhat": "that",
    "de": "the",
    "deh": "the",
    "dem": "them",
    "wey": "where",
    "wetin": "what",
    "abi": "or",
    "dey": "is",
    "na": "is",
    "sef": "self",
    
    # Electronics
    "fone": "phone",
    "fones": "phones",
    "phon": "phone",
    "laptap": "laptop",
    "laptob": "laptop",
    "computa": "computer",
    "computah": "computer",
    "tivi": "tv",
    "teevee": "tv",
    "televishon": "television",
    "headfone": "headphone",
    "headfones": "headphones",
    "earfone": "earphone",
    "earfones": "earphones",
    "chaja": "charger",
    "chargah": "charger",
    
    # Clothing
    "clodes": "clothes",
    "clodez": "clothes",
    "cloting": "clothing",
    "shert": "shirt",
    "sherts": "shirts",
    "tshert": "t-shirt",
    "tshirt": "t-shirt",
    "trousa": "trousers",
    "trousaz": "trousers",
    "jeans": "jeans",
    "jeanz": "jeans",
    "dres": "dress",
    "dreses": "dresses",
    "sket": "skirt",
    "skets": "skirts",
    "jaket": "jacket",
    "jakets": "jackets",
    "kap": "cap",
    "kaps": "caps",
    "hat": "hat",
    "hatz": "hats",
    
    # Actions
    "ad": "add",
    "addit": "add it",
    "remov": "remove",
    "removit": "remove it",
    "serch": "search",
    "sech": "search",
    "fain": "find",
    "faind": "find",
    "luk": "look",
    "lukfor": "look for",
    "sho": "show",
    "shomi": "show me",
    "bai": "buy",
    "boi": "buy",
    "oda": "order",
    "odah": "order",
    "chekout": "checkout",
    "chek": "check",
    "pei": "pay",
    "paiment": "payment",
    
    # Numbers (Ghanaian pronunciation)
    "wan": "one",
    "tu": "two",
    "tree": "three",
    "fo": "four",
    "faiv": "five",
    "siks": "six",
    "seven": "seven",
    "eit": "eight",
    "nain": "nine",
    "ten": "ten",
    "twenti": "twenty",
    "teti": "thirty",
    "foti": "forty",
    "fifti": "fifty",
    "handred": "hundred",
    "tausand": "thousand",
    
    # Currency
    "cedis": "cedis",
    "cedi": "cedi",
    "ghana cedis": "ghana cedis",
    "pesewas": "pesewas",
    
    # Categories
    "elektroniks": "electronics",
    "elektronic": "electronic",
    "fashon": "fashion",
    "fashun": "fashion",
    "buti": "beauty",
    "biuti": "beauty",
    "helth": "health",
    "helt": "health",
    "hom": "home",
    "hous": "house",
    "kichen": "kitchen",
    "kitchin": "kitchen",
    "spoting": "sporting",
    "spots": "sports",
    "buk": "book",
    "buks": "books",
    "toi": "toy",
    "toiz": "toys",
    "beibi": "baby",
    "bebi": "baby",
    
    # Directions/Navigation
    "go": "go",
    "gotu": "go to",
    "bak": "back",
    "forwad": "forward",
    "neks": "next",
    "previus": "previous",
    "hom": "home",
    "profail": "profile",
    "profil": "profile",
    "setings": "settings",
    "seting": "setting",
    "odas": "orders",
    "oda": "order",
    "wishlis": "wishlist",
    "wishlst": "wishlist",
    
    # Common phrases
    "ai wan": "i want",
    "ai wont": "i want",
    "pliz": "please",
    "plis": "please",
    "tenk yu": "thank you",
    "tanks": "thanks",
    "sori": "sorry",
    "ekskyuz": "excuse",
    "helo": "hello",
    "hai": "hi",
    "bai": "bye",
    "gudnait": "goodnight",
    "gudmoning": "good morning",
    
    # Product descriptors
    "chip": "cheap",
    "chiper": "cheaper",
    "ekspensiv": "expensive",
    "gud": "good",
    "beter": "better",
    "bes": "best",
    "nyu": "new",
    "ol": "old",
    "big": "big",
    "biga": "bigger",
    "smol": "small",
    "smola": "smaller",
    
    # Mobile Money
    "momo": "mobile money",
    "mobail moni": "mobile money",
    "mtn": "mtn",
    "vodafon": "vodafone",
    "vodafone": "vodafone",
    "airteltigo": "airteltigo",
    "airtel": "airtel",
    "tigo": "tigo",
    
    # Payment
    "kat": "card",
    "kard": "card",
    "kredit": "credit",
    "debit": "debit",
    "kash": "cash",
    "deliveri": "delivery",
    "delivari": "delivery",
    
    # Quantities
    "mor": "more",
    "les": "less",
    "plenti": "plenty",
    "som": "some",
    "ol": "all",
    "evritin": "everything",
    "notin": "nothing",
    "eni": "any",
    
    # Questions
    "wot": "what",
    "wen": "when",
    "wer": "where",
    "hau": "how",
    "hau moch": "how much",
    "hau meni": "how many",
    "wai": "why",
    "hu": "who",
    
    # Misc common words
    "yes": "yes",
    "yea": "yes",
    "yah": "yes",
    "no": "no",
    "noh": "no",
    "ok": "ok",
    "okei": "okay",
    "olrait": "alright",
    "help": "help",
    "helep": "help",
    "repet": "repeat",
    "agen": "again",
    "kansel": "cancel",
    "konfem": "confirm",
    "konfirm": "confirm",
}


# Store for learned mappings (loaded from database)
LEARNED_MAPPINGS: dict = {}

# Store unknown words for admin review
UNKNOWN_WORDS_LOG: list = []


def load_learned_mappings(mappings: dict) -> None:
    """
    Load learned mappings from database.
    Called on startup to sync with Supabase.
    """
    global LEARNED_MAPPINGS
    LEARNED_MAPPINGS.update(mappings)


def log_unknown_word(word: str, context: str) -> dict:
    """
    Log an unknown word for admin review and future training.
    
    Args:
        word: The unrecognized word
        context: The full sentence for context
        
    Returns:
        Log entry dict
    """
    entry = {
        "word": word.lower(),
        "context": context,
        "timestamp": __import__('datetime').datetime.utcnow().isoformat(),
        "suggested_mapping": None  # Admin will fill this
    }
    UNKNOWN_WORDS_LOG.append(entry)
    return entry


def get_unknown_words() -> list:
    """Get all logged unknown words for admin review."""
    return UNKNOWN_WORDS_LOG


def add_learned_mapping(ghanaian: str, standard: str) -> None:
    """
    Add a new learned mapping (approved by admin).
    
    Args:
        ghanaian: The Ghanaian accent word
        standard: The standard English word
    """
    LEARNED_MAPPINGS[ghanaian.lower()] = standard.lower()


def normalize_accent(text: str, custom_map: dict = None) -> str:
    """
    Normalize Ghanaian accent variations to standard English.
    Uses static mappings + learned mappings from user interactions.
    
    Args:
        text: Raw transcribed text
        custom_map: Optional additional mappings to use
        
    Returns:
        Normalized text with accent variations replaced
    """
    if not text:
        return ""
    
    # Combine all mappings: static + learned + custom
    accent_map = {**ACCENT_MAP, **LEARNED_MAPPINGS}
    if custom_map:
        accent_map.update(custom_map)
    
    # Convert to lowercase for matching
    words = text.lower().split()
    normalized_words = []
    unknown_found = []
    
    for word in words:
        # Check if word needs normalization
        if word in accent_map:
            normalized_words.append(accent_map[word])
        else:
            # Check for partial matches (word might have punctuation)
            clean_word = ''.join(c for c in word if c.isalnum())
            if clean_word in accent_map:
                # Preserve any trailing punctuation
                suffix = word[len(clean_word):] if len(word) > len(clean_word) else ""
                normalized_words.append(accent_map[clean_word] + suffix)
            else:
                normalized_words.append(word)
                # Log potentially unknown accent words (not common English)
                if len(clean_word) > 2 and not is_common_english(clean_word):
                    unknown_found.append(clean_word)
    
    # Log unknown words for self-learning
    if unknown_found:
        for unknown in unknown_found:
            log_unknown_word(unknown, text)
    
    return ' '.join(normalized_words)


# Common English words to skip logging
COMMON_ENGLISH = {
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare',
    'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as',
    'i', 'me', 'my', 'we', 'our', 'you', 'your', 'he', 'him', 'his',
    'she', 'her', 'it', 'its', 'they', 'them', 'their', 'this', 'that',
    'and', 'or', 'but', 'if', 'then', 'else', 'when', 'where', 'why',
    'how', 'what', 'which', 'who', 'whom', 'whose', 'all', 'each',
    'search', 'find', 'show', 'open', 'go', 'add', 'remove', 'cart',
    'home', 'profile', 'orders', 'checkout', 'pay', 'help', 'back',
    'product', 'products', 'category', 'price', 'item', 'items',
}


def is_common_english(word: str) -> bool:
    """Check if a word is common English (don't log these)."""
    return word.lower() in COMMON_ENGLISH


def get_accent_suggestions(word: str) -> list:
    """
    Get possible standard English words for a Ghanaian accent word.
    
    Args:
        word: The word to find suggestions for
        
    Returns:
        List of possible standard English words
    """
    word = word.lower()
    suggestions = []
    
    # Direct match
    if word in ACCENT_MAP:
        suggestions.append(ACCENT_MAP[word])
    
    # Find similar keys
    for key, value in ACCENT_MAP.items():
        if key.startswith(word) or word.startswith(key):
            if value not in suggestions:
                suggestions.append(value)
    
    return suggestions
