import time
from filter_wheel_control import FilterWheel

# A list of different starting positions to test homing time from
STARTING_POSITIONS = [5000, 15000, 25000, 10000]

print("--- Starting Homing Time Test ---")

try:
    # The 'with' statement automatically handles connecting and closing the port
    with FilterWheel(port='COM4') as wheel:
        
        # Loop through each starting position to test
        for start_pos in STARTING_POSITIONS:
            print(f"\n--- Testing from position: {start_pos} ---")
            
            # 1. Move to the starting position
            print(f"Moving to starting position: {start_pos}")
            wheel.move_to_position(start_pos)
            
            # Verify we are at the correct starting point
            position_before_homing = wheel.get_position()
            if position_before_homing != start_pos:
                print(f"❌ FAILED to reach starting position. Expected {start_pos}, got {position_before_homing}")
                continue # Skip to the next test if we can't get to the start

            time.sleep(1)

            # 2. Measure the time it takes to home the device
            print("Starting homing and timing...")
            start_time = time.monotonic()
            wheel.home()
            end_time = time.monotonic()
            
            # 3. Calculate and report the duration
            duration = end_time - start_time
            print(f"✅ Homing complete. Time taken: {duration:.2f} seconds.")
            
            # 4. Verify that the position is now 0
            position_after_homing = wheel.get_position()
            if position_after_homing != 0:
                print("❌ Homing FAILED, position is not 0.")
                break

except Exception as e:
    print(f"\n❌ An error occurred during the test: {e}")

print("\n--- Homing Time Test Finished ---")

