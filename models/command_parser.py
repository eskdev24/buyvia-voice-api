"""
Voice Command Parser
Parses normalized text into actionable commands
Supports 100+ commands across navigation, search, cart, checkout, and more
"""

import re
from typing import Dict, List, Optional, Any


# Command patterns organized by category
COMMAND_PATTERNS = {
    # ==========================================
    # NAVIGATION COMMANDS (20+)
    # ==========================================
    "go_home": [
        "go home", "go to home", "home page", "take me home", 
        "back to home", "main page", "home screen", "start page"
    ],
    "open_cart": [
        "open cart", "show cart", "view cart", "go to cart",
        "my cart", "shopping cart", "see cart", "check cart"
    ],
    "open_profile": [
        "open profile", "my profile", "view profile", "go to profile",
        "account", "my account", "profile page", "user profile"
    ],
    "open_orders": [
        "show orders", "my orders", "view orders", "order history",
        "past orders", "previous orders", "check orders", "see orders"
    ],
    "open_wishlist": [
        "open wishlist", "my wishlist", "view wishlist", "saved items",
        "favorites", "my favorites", "show wishlist", "wish list"
    ],
    "open_settings": [
        "open settings", "settings", "preferences", "app settings",
        "my settings", "configuration", "options"
    ],
    "open_categories": [
        "show categories", "all categories", "browse categories",
        "category list", "view categories", "product categories"
    ],
    "go_back": [
        "go back", "back", "previous", "previous page",
        "return", "go previous", "back button"
    ],
    "go_forward": [
        "go forward", "forward", "next", "next page"
    ],
    
    # ==========================================
    # SEARCH COMMANDS (30+)
    # ==========================================
    "search_product": [
        r"(search|find|look for|show me|i want|looking for|get me|find me) (.+)",
        r"(where can i find|where is|do you have) (.+)",
        r"(i need|i'm looking for|searching for) (.+)"
    ],
    "filter_category": [
        r"(show|filter|display|browse) (.+) category",
        r"(only|just) (.+) products",
        r"(.+) section"
    ],
    "filter_price_under": [
        r"(under|below|less than|cheaper than|maximum) (\d+) (cedis|ghana cedis|ghc)",
        r"(under|below|less than) (\d+)",
        r"budget (\d+)"
    ],
    "filter_price_over": [
        r"(over|above|more than|minimum) (\d+) (cedis|ghana cedis|ghc)",
        r"(over|above|more than) (\d+)"
    ],
    "sort_price_low": [
        "sort by price", "cheapest first", "lowest price",
        "price low to high", "sort cheap", "affordable first"
    ],
    "sort_price_high": [
        "expensive first", "highest price", "price high to low",
        "most expensive", "premium first"
    ],
    "sort_newest": [
        "newest first", "latest products", "new arrivals",
        "sort by new", "recently added", "just arrived"
    ],
    "sort_popular": [
        "most popular", "best selling", "trending",
        "top rated", "popular first", "hot items"
    ],
    "clear_filters": [
        "clear filters", "reset filters", "remove filters",
        "show all", "no filter", "clear all filters"
    ],
    
    # ==========================================
    # CART COMMANDS (25+)
    # ==========================================
    "add_to_cart": [
        "add to cart", "add this", "put in cart", "add item",
        "buy this", "i want this", "add to basket", "get this",
        "add it", "put this in cart", "add to my cart"
    ],
    "add_multiple": [
        r"add (\d+) (of these|of this|items|pieces)",
        r"(add|put) (\d+) (to cart|in cart)"
    ],
    "remove_from_cart": [
        "remove from cart", "delete this", "remove this",
        "take out", "remove item", "delete from cart"
    ],
    "increase_quantity": [
        "add one more", "increase", "plus one", "one more",
        "increase quantity", "add another", "more of this"
    ],
    "decrease_quantity": [
        "reduce", "minus one", "decrease", "one less",
        "decrease quantity", "remove one", "less of this"
    ],
    "set_quantity": [
        r"(set|change) quantity to (\d+)",
        r"i want (\d+) (of these|of this|pieces|items)",
        r"make it (\d+)"
    ],
    "clear_cart": [
        "clear cart", "empty cart", "delete all",
        "remove everything", "clear basket", "empty basket",
        "remove all items", "start fresh"
    ],
    "view_cart_total": [
        "cart total", "how much", "total price",
        "what's the total", "show total", "calculate total"
    ],
    
    # ==========================================
    # CHECKOUT COMMANDS (15+)
    # ==========================================
    "checkout": [
        "checkout", "proceed to checkout", "pay now",
        "complete order", "finish order", "place order",
        "buy now", "proceed to payment", "go to checkout"
    ],
    "pay_with_momo": [
        "pay with mobile money", "use momo", "mobile money",
        "mtn money", "vodafone cash", "airteltigo money",
        "pay with momo", "mobile payment"
    ],
    "pay_with_card": [
        "pay with card", "use card", "credit card",
        "debit card", "card payment", "visa", "mastercard"
    ],
    "pay_with_cash": [
        "cash on delivery", "pay cash", "pay on delivery",
        "cod", "cash payment", "pay when delivered"
    ],
    "apply_coupon": [
        r"(apply|use) coupon (.+)",
        r"(apply|use) code (.+)",
        r"discount code (.+)",
        "apply discount", "use promo code"
    ],
    "select_address": [
        "change address", "select address", "different address",
        "delivery address", "shipping address", "use another address"
    ],
    
    # ==========================================
    # WISHLIST COMMANDS (10+)
    # ==========================================
    "add_to_wishlist": [
        "add to wishlist", "save for later", "bookmark this",
        "save this", "add to favorites", "favorite this",
        "remember this", "save item"
    ],
    "remove_from_wishlist": [
        "remove from wishlist", "unsave", "remove from favorites",
        "delete from wishlist", "unfavorite"
    ],
    "move_to_cart": [
        "move to cart", "add from wishlist", "buy from wishlist",
        "move to basket", "add saved item to cart"
    ],
    
    # ==========================================
    # PRODUCT COMMANDS (15+)
    # ==========================================
    "view_product": [
        "view product", "show details", "more info",
        "product details", "tell me more", "see details"
    ],
    "view_reviews": [
        "show reviews", "read reviews", "customer reviews",
        "what do people say", "ratings", "see ratings"
    ],
    "check_stock": [
        "is it available", "in stock", "check availability",
        "do you have it", "is it in stock", "availability"
    ],
    "view_images": [
        "show images", "more pictures", "view photos",
        "see images", "product images", "gallery"
    ],
    "related_products": [
        "similar products", "related items", "like this",
        "show similar", "alternatives", "other options"
    ],
    
    # ==========================================
    # ORDER TRACKING (10+)
    # ==========================================
    "track_order": [
        r"track order (.+)",
        r"where is (my order|order) (.+)",
        "track my order", "order status", "delivery status",
        "where is my package", "shipping status"
    ],
    "cancel_order": [
        r"cancel order (.+)",
        "cancel my order", "cancel this order",
        "i want to cancel", "stop order"
    ],
    "reorder": [
        "order again", "reorder", "buy again",
        "repeat order", "same order"
    ],
    
    # ==========================================
    # HELP & MISC COMMANDS (10+)
    # ==========================================
    "help": [
        "help", "what can you do", "commands",
        "voice commands", "how to use", "assist me",
        "i need help", "show commands"
    ],
    "repeat": [
        "repeat", "say again", "what did you say",
        "come again", "pardon", "repeat that"
    ],
    "cancel_voice": [
        "cancel", "never mind", "stop", "forget it",
        "dismiss", "close"
    ],
    "confirm": [
        "yes", "confirm", "correct", "that's right",
        "proceed", "continue", "okay", "ok"
    ],
    "deny": [
        "no", "wrong", "incorrect", "that's wrong",
        "not that", "cancel that"
    ],
}

# Number word mappings
NUMBER_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
    "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40,
    "fifty": 50, "hundred": 100, "thousand": 1000,
}


def is_regex_pattern(pattern: str) -> bool:
    """Check if a pattern string is a regex (contains regex special chars)."""
    regex_indicators = ['(', ')', '+', '*', '?', '[', ']', '\\d', '|', '^', '$']
    return any(indicator in pattern for indicator in regex_indicators)


def parse_command(text: str) -> Dict[str, Any]:
    """
    Parse normalized text into a command structure.
    
    Args:
        text: Normalized text from speech recognition
        
    Returns:
        Dictionary with command type and parameters
    """
    if not text:
        return {"type": "unknown", "params": {}, "confidence": 0.0}
    
    text = text.lower().strip()
    
    # Try to match each command pattern
    for command_type, patterns in COMMAND_PATTERNS.items():
        if isinstance(patterns, list):
            for pattern in patterns:
                if isinstance(pattern, str):
                    # Check if it's a regex pattern
                    if is_regex_pattern(pattern):
                        try:
                            match = re.search(pattern, text)
                            if match:
                                return {
                                    "type": command_type,
                                    "params": extract_regex_params(match, command_type),
                                    "confidence": 0.9
                                }
                        except re.error:
                            pass  # Invalid regex, treat as string
                    else:
                        # Simple string matching
                        if pattern in text or text in pattern:
                            return {
                                "type": command_type,
                                "params": extract_params(text, command_type),
                                "confidence": calculate_confidence(text, pattern)
                            }
    
    # No match found
    return {
        "type": "unknown",
        "params": {"raw_text": text},
        "confidence": 0.0
    }


def extract_params(text: str, command_type: str) -> Dict[str, Any]:
    """Extract parameters from command text."""
    params = {}
    
    # Extract quantity if present
    quantity = extract_quantity(text)
    if quantity:
        params["quantity"] = quantity
    
    # Extract product name for search commands
    if "search" in command_type or command_type == "add_to_cart":
        product = extract_product_name(text)
        if product:
            params["query"] = product
    
    # Extract price for filter commands
    if "price" in command_type:
        price = extract_price(text)
        if price:
            params["price"] = price
    
    return params


def extract_regex_params(match: re.Match, command_type: str) -> Dict[str, Any]:
    """Extract parameters from regex match."""
    params = {}
    groups = match.groups()
    
    if command_type == "search_product" and len(groups) >= 2:
        params["query"] = groups[1].strip()
    elif command_type == "filter_category" and len(groups) >= 2:
        params["category"] = groups[1].strip()
    elif "price" in command_type and len(groups) >= 2:
        try:
            params["price"] = int(groups[1])
        except:
            pass
    elif command_type == "add_multiple" and len(groups) >= 2:
        try:
            params["quantity"] = int(groups[0]) if groups[0].isdigit() else int(groups[1])
        except:
            params["quantity"] = 1
    elif command_type == "set_quantity" and len(groups) >= 1:
        for g in groups:
            if g and g.isdigit():
                params["quantity"] = int(g)
                break
    elif command_type == "track_order" and len(groups) >= 1:
        params["order_id"] = groups[-1].strip() if groups[-1] else None
    elif command_type == "apply_coupon" and len(groups) >= 1:
        params["coupon_code"] = groups[-1].strip() if groups[-1] else None
    
    return params


def extract_quantity(text: str) -> Optional[int]:
    """Extract quantity from text."""
    # Check for number words
    for word, num in NUMBER_WORDS.items():
        if word in text.split():
            return num
    
    # Check for digits
    numbers = re.findall(r'\d+', text)
    if numbers:
        return int(numbers[0])
    
    return None


def extract_product_name(text: str) -> Optional[str]:
    """Extract product name from search text."""
    # Remove common command words
    remove_words = [
        "search", "find", "look for", "show me", "i want",
        "looking for", "get me", "find me", "where can i find",
        "where is", "do you have", "i need", "searching for"
    ]
    
    result = text.lower()
    for word in remove_words:
        result = result.replace(word, "")
    
    return result.strip() if result.strip() else None


def extract_price(text: str) -> Optional[int]:
    """Extract price value from text."""
    # Look for number followed by currency
    match = re.search(r'(\d+)\s*(cedis|ghana cedis|ghc)?', text)
    if match:
        return int(match.group(1))
    return None


def calculate_confidence(text: str, pattern: str) -> float:
    """Calculate confidence score for a match."""
    if text == pattern:
        return 1.0
    elif pattern in text:
        return 0.9
    elif text in pattern:
        return 0.8
    else:
        # Calculate word overlap
        text_words = set(text.split())
        pattern_words = set(pattern.split())
        overlap = len(text_words & pattern_words)
        total = len(text_words | pattern_words)
        return overlap / total if total > 0 else 0.0


def get_command_help() -> Dict[str, List[str]]:
    """Get help text for all available commands."""
    help_text = {}
    
    categories = {
        "Navigation": ["go_home", "open_cart", "open_profile", "open_orders", "go_back"],
        "Search": ["search_product", "filter_category", "sort_price_low", "sort_newest"],
        "Cart": ["add_to_cart", "remove_from_cart", "increase_quantity", "clear_cart"],
        "Checkout": ["checkout", "pay_with_momo", "pay_with_card", "pay_with_cash"],
        "Wishlist": ["add_to_wishlist", "remove_from_wishlist", "move_to_cart"],
        "Help": ["help", "repeat", "cancel_voice"]
    }
    
    for category, commands in categories.items():
        examples = []
        for cmd in commands:
            if cmd in COMMAND_PATTERNS:
                patterns = COMMAND_PATTERNS[cmd]
                if isinstance(patterns, list) and patterns:
                    first_pattern = patterns[0]
                    if isinstance(first_pattern, str):
                        examples.append(f'"{first_pattern}"')
        help_text[category] = examples
    
    return help_text
