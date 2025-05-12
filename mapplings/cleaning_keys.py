# These give names to the cleaning_function_map keys so they show up for autocomplete
# The value assigned to each dictates the order in which the associated function will be applied
# Function maps are defined beneath each cleaner class

# Mappling Cleaner Keys
# Prefix with mc_
mc_try_to_kill = 0
mc_tidy_containers = 1
mc_insert_avoiders = 2
mc_backmap = 4
mc_reap_contradictions = 3
mc_remove_empty = 5
mc_clean_params = 6
mc_redundancy_check = 7
mc_full = -1  # Flags a full cleanup

# Parameter Cleaner keys
# Prefix with pc_
pc_fusion = 3
pc_reduce_empty = 1
pc_remove_blank = 0
pc_unplace_points = 2
pc_full = -1  # Flags a full cleanup
