from app import server

if __name__ == "__main__":
    from waitress import serve
    serve(server, host="0.0.0.0", port=8080)