
# update time_target format 
for id, tt in user['time_targets']['lists'].items():
    if 'within_value' not in tt:
        print("Updating time target to new format ",tt)
        tt['within_value'] = tt['num_days']
        tt['within_unit'] = 'days'
        print(tt)
    if 'status' not in tt:
        tt['status'] = True

        
for id, tt in user['time_targets']['tasks'].items():
    if 'within_value' not in tt:
        print("Updating time target to new format ",tt)
        tt['within_value'] = tt['num_days']
        tt['within_unit'] = 'days'
        print(tt)
    if 'status' not in tt:
        tt['status'] = True
