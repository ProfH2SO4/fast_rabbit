from fast_rabbit import fast_rabbit
from uvicorn import run


if __name__ == "__main__":
    run(fast_rabbit, host="0.0.0.0", port=8000)
