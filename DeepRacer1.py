def reward_function(params):
    '''
    Example of rewarding the agent to follow center line
    '''
    
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    on_track = params['all_wheels_on_track']
    
    steeringAngle = params['steering_angle']
    steeringAbs = abs(steeringAngle)
    leftOfCenter = params['is_left_of_center']
    speed = params['speed']
    steps = params['steps']
    progress = params['progress']
    maxSteeringAngle = 22.0
    maxSpeed = 8.0
    
    # Our AWS re:Invent 2018 target is currently consistent 10 second consistent laps.
    desiredSeconds = 10
    stepsPerSecond = 15
    
    # This is the calculated desired maximum steps before we are going way too slow.
    maxStepsBeforeTooSlow = desiredSeconds * stepsPerSecond
    
    # This is what we get each step just for being on the track still. It should prevent us from driving really fast right off course and calling that a high score.
    reward = 100 
    
    # Set the reward based upon the car's speed relative to its steering angle.
    reward = reward + ((maxSpeed - (speed * ((steeringAbs + 1) / maxSteeringAngle))) * speed)
    
    # Models that made it further in the track are significantly more desirable
    #reward = reward * (progress / 100)
    
    # Incentivize speed straight up.
    #reward = reward + speed
    
    '''
    If we're dipping one, two, or three wheels off the track we can ever so slightly reward that to incentivize cutting corners. This, combined with a minimum steps algorithm should slowly instruct the car to find a true racing line.
    '''
    if not on_track:
        reward = reward * 1.03
    
    # Calculate 3 markers that are at varying distances away from the center line
    marker_near = 0.15 * track_width
    marker_med = 0.30 * track_width
    marker_far = 0.50 * track_width
    
    if leftOfCenter:
        # If we're close to the center we should reward low steering angles.
        if distance_from_center <= marker_near:
            if steeringAbs <= 8:
                reward = reward * 1.5
                if speed == maxSpeed:
                    # Reward going very fast if we're near the middle and have a low steering angle.
                    reward = reward * 1.15
            elif steeringAbs <= 15 and speed > 4:
                reward = reward * 1.15
            else:
                # Don't knock this too much. We want to be near the middle sometimes while turning.
                reward = reward * 0.90
        # If we're sort of far from the center we should try to be turning back towards it.
        elif distance_from_center <= marker_med:
            if steeringAngle < 0:
                reward = reward * 1.25
            elif steeringAngle <= 8:
                reward = reward * 0.75
            else:
                reward = reward * 0.25 # We are turning towards the side of the course fast!
        # If we're out near the edge this is an immediate problem.
        elif distance_from_center <= marker_far:
            # Turn sharp to the right = VERY GOOD!
            if steeringAngle <= -13:
                reward = reward * 1.50
            # Anything else = BYE BYE!
            else:
                reward = reward * 0.25
        # If we're not full opposite lock we're probably done.
        elif steeringAngle != -22:
            reward = 1e-3
    else: # Right of center
        # If we're close to the center we should reward low steering angles.
        if distance_from_center <= marker_near:
            if steeringAbs <= 8:
                reward = reward * 1.5
                if speed == maxSpeed:
                    # Reward going very fast if we're near the middle and have a low steering angle.
                    reward = reward * 1.15
            elif steeringAbs <= 15 and speed > 4:
                reward = reward * 1.15
            else:
                # Don't knock this too much. We want to be near the middle sometimes while turning.
                reward = reward * 0.90
        # If we're sort of far from the center we should try to be turning back towards it.
        elif distance_from_center <= marker_med:
            if steeringAngle > 0:
                reward = reward * 1.25
            elif steeringAngle >= -8:
                reward = reward * 0.75
            else:
                reward = reward * 0.25 # We are turning towards the side of the course fast!
        # If we're out near the edge this is an immediate problem.
        elif distance_from_center <= marker_far:
            # Turn sharp to the right = VERY GOOD!
            if steeringAngle >= 13:
                reward = reward * 1.50
            # Anything else = BYE BYE!
            else:
                reward = reward * 0.25
        # If we're not full opposite lock we're probably done.
        elif steeringAngle != 22:
            reward = 1e-3
    '''
    We want to incentivize the program to use as few steps as possible so it should start getting negative points if it gets over 225 steps (roughly 15 seconds of course time). By adding in the progress multiplier the program will trend towards a middle ground where it tries to follow the track while making progress as quickly as possible. 
    '''
    reward = reward + ((1 - (steps / maxStepsBeforeTooSlow)) * progress)
    
    return float(reward)
