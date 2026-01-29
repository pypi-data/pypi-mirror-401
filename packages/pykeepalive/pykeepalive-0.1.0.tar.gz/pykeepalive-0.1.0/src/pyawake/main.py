import time
import random
import typer
from pynput.mouse import Controller

mouse = Controller()
app = typer.Typer()

def run(min_interval: int = 20, max_interval: int = 60, duration: int = None):
    """
    Keeps the system awake by making tiny mouse movements.
    """
    print("pykeepalivelive running. Press Ctrl+C to stop.")
    
    start_time = time.time() if duration else None

    try:
        while True:
            if duration and time.time() - start_time >= duration:
                print(f"\npykeepalivelive stopped after {duration} seconds.")
                break
            
            dx = random.randint(-2, 2)
            dy = random.randint(-2, 2)

            mouse.move(dx, dy)
            time.sleep(random.randint(min_interval, max_interval))

    except KeyboardInterrupt:
        print("\npykeepalivelive stopped.")

@app.command()
def pykeepalivelive(
    min_interval: int = typer.Option(20, help="Minimum interval between movements in seconds"),
    max_interval: int = typer.Option(60, help="Maximum interval between movements in seconds"),
    duration: int = typer.Option(None, help="Run for this many seconds, then stop (for testing)")
):
    run(min_interval, max_interval, duration)

def main():
    app()

if __name__ == "__main__":
    main()