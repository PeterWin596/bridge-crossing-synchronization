import threading
import time

# Define semaphores and mutex
direction_lock = threading.Semaphore(1)     # Controls access to ensure only one direction is on the bridge at a time
bridge_capacity = threading.Semaphore(5)    # Limits the number of people on the bridge to 5 at any given time
count_lock = threading.Lock()               # Protects updates to the count of people crossing from each side

# State variables for managing bridge crossing
north_count = 0
south_count = 0
first_north_reported = False
first_south_reported = False

# Function to handle a person crossing the bridge from the north
def cross_from_north(person_id):
    global north_count, first_north_reported

    # Ensure exclusive access to northbound traffic by acquiring direction_lock
    with direction_lock:
        # Check if this is the first northbound person to cross and print a message if so
        with count_lock:
            if not first_north_reported:
                print("First person crossing the bridge to north")
                first_north_reported = True

    # Control the number of people on the bridge by acquiring bridge_capacity
    with bridge_capacity:
        print(f"Person {person_id} is crossing the bridge from the north.")
        
        # Increment north_count to track the number of northbound people crossing
        with count_lock:
            north_count += 1

        time.sleep(1)  # Simulate the time taken to cross the bridge

        # Decrement north_count after crossing and allow southbound access if last person
        with count_lock:
            north_count -= 1
            if north_count == 0:  # If no more northbound people, release direction_lock for southbound traffic
                direction_lock.release()

# Function to handle a person crossing the bridge from the south
def cross_from_south(person_id):
    global south_count, first_south_reported

    # Ensure exclusive access to southbound traffic by acquiring direction_lock
    with direction_lock:
        # Check if this is the first southbound person to cross and print a message if so
        with count_lock:
            if not first_south_reported:
                print("First person crossing the bridge to south")
                first_south_reported = True

    # Control the number of people on the bridge by acquiring bridge_capacity
    with bridge_capacity:
        print(f"Person {person_id} is crossing the bridge from the south.")
        
        # Increment south_count to track the number of southbound people crossing
        with count_lock:
            south_count += 1

        time.sleep(1)  # Simulate the time taken to cross the bridge

        # Decrement south_count after crossing and allow northbound access if last person
        with count_lock:
            south_count -= 1
            if south_count == 0:  # If no more southbound people, release direction_lock for northbound traffic
                direction_lock.release()

# Main execution: create and start threads for people crossing the bridge
print("Maximum number of people that can cross the bridge: 5")
threads = []

# Create threads for northbound and southbound people
for i in range(1, 6):
    threads.append(threading.Thread(target=cross_from_north, args=(i,)))
    threads.append(threading.Thread(target=cross_from_south, args=(i,)))

# Start all threads to simulate crossing
for thread in threads:
    thread.start()

# Wait for all threads to finish crossing
for thread in threads:
    thread.join()
