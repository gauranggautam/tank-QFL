import time
from montana import cryocore

DEFAULT_IP = "192.168.0.2"

def start_cryo(ip_address=DEFAULT_IP, cryo=None):
    """Initializes and returns the CryoCore controller instance."""
    if cryo is not None:
        return cryo
    try:
        cryo = cryocore.CryoCore(ip_address)
        print(f"Connected to Montana CryoCore at {ip_address}")
        return cryo
    except Exception as e:
        print(f"ERROR: Failed to connect to CryoCore: {e}")
        return None

# --- Smart State Helpers ---

def _get_val(res):
    """Safely extracts the value whether the API returns a direct value or a (success, value) tuple."""
    if isinstance(res, tuple):
        return res[1]
    return res

def cryo_state(cryo):
    """Returns the current system state as a string."""
    try: return _get_val(cryo.get_system_state())
    except Exception: return "Unknown"

def cryo_goal(cryo):
    """Returns the current system goal as a string."""
    try: return _get_val(cryo.get_system_goal())
    except Exception: return "Unknown"

def cryo_ensure_ready(cryo, timeout=30):
    """Safely aborts active goals and waits until the system is 'Ready'."""
    goal = cryo_goal(cryo)
    state = cryo_state(cryo)
    
    if goal in ['None', None] and state == 'Ready':
        return True # Already ready
        
    print(f"System busy (Goal: {goal}, State: {state}). Aborting current goal...")
    try:
        cryo.abort_goal()
    except Exception as e:
        print(f"Error aborting goal: {e}")
        
    # Wait for the state machine to settle into 'Ready'
    start_time = time.time()
    while time.time() - start_time < timeout:
        if cryo_state(cryo) == 'Ready':
            print("System is now Ready.")
            return True
        time.sleep(1)
        
    print("WARNING: Timed out waiting for system to reach 'Ready' state.")
    return False

# --- Core Command Wrappers ---

def cryo_pullvac(cryo=None):
    """Smartly initiates vacuum pull if not already doing so."""
    cryo = start_cryo(cryo=cryo)
    if cryo is None: return
    
    goal = cryo_goal(cryo)
    if goal == 'PullVacuum':
        print("System is already pulling vacuum.")
        return
        
    if cryo_ensure_ready(cryo):
        try:
            cryo.pull_vacuum()
            print("Vacuum pull initiated.")
        except Exception as e:
            print(f"Error pulling vacuum: {e}")

def cryo_vent(cryo=None):
    """Smartly initiates system vent."""
    cryo = start_cryo(cryo=cryo)
    if cryo is None: return
    
    goal = cryo_goal(cryo)
    if goal == 'Vent':
        print("System is already venting.")
        return
        
    if cryo_ensure_ready(cryo):
        try:
            cryo.vent()
            print("Venting initiated.")
        except Exception as e:
            print(f"Error venting: {e}")

def cryo_set_temp(cryo=None, target_temp=10):
    """Sets the target platform temperature."""
    cryo = start_cryo(cryo=cryo)
    if cryo is None: return
    try:
        cryo.set_platform_target_temperature(target_temp)
        print(f"Platform target temperature set to: {target_temp} K")
    except Exception as e:
        print(f"Error setting platform temperature: {e}")

def cryo_start_cooldown(cryo=None, target_temp=10, bakeout=False, n2purge=False):
    """
    Intelligently transitions to cooling down. Aborts vacuum pulls or warmups, 
    sets configuration, and initiates cooldown.
    """
    cryo = start_cryo(cryo=cryo)
    if cryo is None: return
    
    goal = cryo_goal(cryo)
    
    # If we are pulling vacuum or doing something else conflicting, abort it to reach 'Ready'
    if goal not in ['Cooldown', 'None', None]:
        cryo_ensure_ready(cryo)

    try:
        # Disable extras to ensure clean cooldown
        if hasattr(cryo, 'set_platform_bakeout_enabled'):
            try: cryo.set_platform_bakeout_enabled(bakeout)
            except TypeError: cryo.set_platform_bakeout_enabled = bakeout
            
        if hasattr(cryo, 'set_dry_nitrogen_purge_enabled'):
            try: cryo.set_dry_nitrogen_purge_enabled(n2purge)
            except TypeError: cryo.set_dry_nitrogen_purge_enabled = n2purge

        cryo.set_platform_target_temperature(target_temp)
        print(f"Platform target temperature set to: {target_temp} K")
        
        # Only issue cooldown command if not already actively cooling
        if cryo_goal(cryo) != 'Cooldown':
            cryo.cooldown()
            print(f"Cooldown sequence initiated. (Bakeout: {bakeout}, N2 Purge: {n2purge})")
        else:
            print("System is already in Cooldown mode. Target temperature updated.")
            
    except Exception as e:
        print(f"Error starting cooldown: {e}")

def cryo_get_temp_p1(cryo=None):
    """Returns the current platform temperature (P1) as a float."""
    cryo = start_cryo(cryo=cryo)
    if cryo is None: return None
    try: return float(_get_val(cryo.get_platform_temperature()))
    except Exception as e:
        print(f"Error reading platform temperature: {e}")
        return None

def cryo_get_temp_u1(cryo=None):
    """Returns the current user 1 temperature (U1) as a float."""
    cryo = start_cryo(cryo=cryo)
    if cryo is None: return None
    try: return float(_get_val(cryo.get_user1_temperature()))
    except Exception as e:
        print(f"Error reading user 1 temperature: {e}")
        return None

def cryo_waitfortemp_p1(req_temp, cryo=None, tolerance=1.0, poll_interval=2):
    """Blocks infinitely until platform temperature (P1) matches req_temp within tolerance."""
    cryo = start_cryo(cryo=cryo)
    if cryo is None: return
    print(f"Waiting for platform temperature to reach {req_temp} K (tolerance: ±{tolerance}K)...")
    
    while True:
        current_temp = cryo_get_temp_p1(cryo)
        if current_temp is not None:
            diff = abs(current_temp - req_temp)
            print(f"Current Platform Temp: {current_temp:.2f} K (Target: {req_temp} K) | State: {cryo_state(cryo)}", end='\r')
            if diff <= tolerance:
                print(f"\nPlatform reached target temperature: {current_temp:.2f} K")
                break
        time.sleep(poll_interval)

def cryo_waitfortemp_u1(req_temp, cryo=None, tolerance=1.0, poll_interval=2):
    """Blocks infinitely until user 1 temperature (U1) matches req_temp within tolerance."""
    cryo = start_cryo(cryo=cryo)
    if cryo is None: return
    print(f"Waiting for User 1 temperature to reach {req_temp} K (tolerance: ±{tolerance}K)...")
    
    while True:
        current_temp = cryo_get_temp_u1(cryo)
        if current_temp is not None:
            diff = abs(current_temp - req_temp)
            print(f"Current User 1 Temp: {current_temp:.2f} K (Target: {req_temp} K) | State: {cryo_state(cryo)}", end='\r')
            if diff <= tolerance:
                print(f"\nUser 1 reached target temperature: {current_temp:.2f} K")
                break
        time.sleep(poll_interval)

def cryo_waitforvac(target_pressure=0.1, cryo=None, timeout_s=1800, poll_interval=2):
    """Blocks until the sample chamber reaches the target vacuum pressure."""
    cryo = start_cryo(cryo=cryo)
    if cryo is None: return
    print("Waiting for vacuum target...")
    
    start_time = time.time()
    while time.time() - start_time < timeout_s:
        try:
            pressure = _get_val(cryo.get_sample_chamber_pressure())
            state = cryo_state(cryo)
            
            if pressure is not None:
                print(f"Current Pressure: {pressure:.4f} (Target: {target_pressure}) | State: {state}", end='\r')
                if pressure <= target_pressure:
                    print(f"\nVacuum target reached: {pressure:.4f}")
                    return True
        except Exception:
            pass
        time.sleep(poll_interval)
    print("\nWARNING: Timeout reached waiting for vacuum.")
    return False

def cryo_waitforvent(vent_pressure_threshold=700, cryo=None, timeout_s=600, poll_interval=2):
    """Blocks until the system pressure rises near atmospheric pressure."""
    cryo = start_cryo(cryo=cryo)
    if cryo is None: return
    print("Waiting for system to vent...")
    
    start_time = time.time()
    while time.time() - start_time < timeout_s:
        try:
            pressure = _get_val(cryo.get_sample_chamber_pressure())
            state = cryo_state(cryo)
            
            if pressure is not None:
                print(f"Current Pressure: {pressure:.1f} (Target: >={vent_pressure_threshold}) | State: {state}", end='\r')
                if pressure >= vent_pressure_threshold:
                    print(f"\nVenting complete. Current pressure: {pressure:.1f}")
                    return True
        except Exception:
            pass
        time.sleep(poll_interval)
    print("\nWARNING: Timeout reached waiting for vent.")
    return False