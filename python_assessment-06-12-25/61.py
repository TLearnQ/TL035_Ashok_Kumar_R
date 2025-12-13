# QUESTION NO:61

BOOK_DATA = {
    101: {"title": "Python Basics", "status": "Available", "category": "Tech"},
    102: {"title": "The Art of Data", "status": "Checked Out", "category": "Tech"}
}
NEXT_ID = 103 

def api_router(request_string, payload=None):
    global NEXT_ID 

    try:
        method, path = request_string.split(' ', 1)
        method = method.upper()
    except ValueError:
        return {"error": 400, "message": "bad Request give the input properly"}

    if method == "GET":
        
        if path == "/items":
            return list(BOOK_DATA.values())
        
        elif path == "/stats":
            available_count = sum(1 for book in BOOK_DATA.values() if book.get('status') == 'Available')
            return {
                "total_items": len(BOOK_DATA),
                "available_count": available_count
            }
            
        elif path.startswith("/items?category="):
            _, filter_value = path.split("category=")
            filtered_list = [
                book for book in BOOK_DATA.values() 
                if book.get('category') == filter_value
            ]
            return filtered_list

    elif method == "POST":
        
        if path == "/items":
            if not payload:
                 return {"error": 400, "message": "POST requires a payload."}
            
            BOOK_DATA[NEXT_ID] = payload
            response = {"id": NEXT_ID, "status": "created"}
            NEXT_ID += 1
            return response
    
    if method not in ["GET", "POST"]:
        return {"error": 405, "message": f"Method Not Allowed: {method}"}
    
    return {"error": 404, "message": f"Resource Not Found: {path}"}


print(api_router("GET /items"))
print(api_router("GET /stats"))
new_book = {"title": "Cloud Basics", "status": "Available", "category": "Tech"}
print(api_router("POST /items", payload=new_book))
print(api_router("GET /items?category=Tech"))
print(api_router("GET /users"))
