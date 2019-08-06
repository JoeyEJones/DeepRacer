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
    reward = 100 # This is what we get each step just for being on the track still. It should prevent us from driving really fast right off course and calling that a high score.
    
    '''
    Set the reward based upon the car's speed relative to its steering angle.
    '''
    reward = reward + ((maxSpeed - (speed * ((steeringAbs + 1) / maxSteeringAngle))) * speed + (speed / 2))
    
    '''
    Models that made it further in the track are significantly more desirable
    '''
    
    #reward = reward * (progress / 100)
    
    '''
    Reduce the reward ever so slightly if the car is completely on the track (we want to cut corners).
    '''
    #if on_track:
    #    reward = reward * 0.98
    
    '''
    Reduce the reward if the car is left of center and turning left or right of center and turning right.

    if leftOfCenter and steeringAngle > 3:
        reward = reward * 0.90
    elif (not leftOfCenter) and steeringAngle < -3:
        reward = reward * 0.90
    elif leftOfCenter and steeringAngle < -3:
        reward = reward * 1.10
    elif (not leftOfCenter) and steeringAngle > 3:
        reward = reward * 1.10
    else:
        reward = reward
    '''
    
    # Calculate 3 markers that are at varying distances away from the center line
    marker_near = 0.1 * track_width
    marker_med = 0.25 * track_width
    marker_far = 0.5 * track_width
    
    if leftOfCenter:
        # If we're close to the center we should reward low steering angles.
        if distance_from_center <= marker_near:
            if steeringAbs <= 8:
                reward = reward * 1.5
            elif steeringAbs <= 15:
                reward = reward
            else:
                # Don't knock this too much. We want to be near the middle sometimes while turning.
                reward = reward * 0.85
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
            elif steeringAbs <= 15:
                reward = reward
            else:
                reward = reward * 0.50
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
            
    return float(reward)
