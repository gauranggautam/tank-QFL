import time
from filter_wheel_control import FilterWheel

# A list of different positions to test
POSITIONS_TO_TEST = [
    10000,
    25000,
    5000,
    0
]

print("--- Starting Final Movement and Verification Test ---")

try:
    # The 'with' statement automatically handles connecting and closing the port
    with FilterWheel(port='COM4') as wheel:
        
        # 1. Home the device to establish a reliable zero point
        wheel.home()
        position_after_homing = wheel.get_position()
        print(f"Position after homing: {position_after_homing}\n")
        
        # 2. Loop through each target position in the test list
        for target in POSITIONS_TO_TEST:
            
            # Command the wheel to move to the target position
            wheel.move_to_position(target)
            
            # Verify the position after the move is complete
            actual_position = wheel.get_position()
            print(f"Move to {target} finished. Software position is: {actual_position}")
            
            # Compare the actual position to the target and report success/failure
            if actual_position == target:
                print("✅ Position Verified\n")
            else:
                print(f"❌ Verification FAILED. Expected {target}, got {actual_position}\n")
            
            time.sleep(1) # Pause briefly between moves

except Exception as e:
    print(f"\n❌ An error occurred during the test: {e}")

print("--- Test Finished ---")
