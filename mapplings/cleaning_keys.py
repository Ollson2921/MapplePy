from mapped_tiling import Cleaner
from parameter import ParamCleaner

#Mappling keys
kill_if_empty = 0
tidy_containing_parameters = 1
insert_avoiders = 2
reap_contradictions = 3
backmap_points = 4
remove_empty_ghosts = 5
remove_empty_rows_and_cols = 6
clean_parameter_lists = 7
remove_redundant_parameters = 8

mappling_function_map = {0: Cleaner.method_name0, 1: Cleaner.method_name1}

#Parameter keys
purge_redundant_obs_and_reqs = 0
unplace_points = 1
remove_empty_rows_and_cols = 2
remove_blank_rows_and_cols = 3
fuse_when_able = 4

parameter_function_map = {0: ParamCleaner.method_name0, 1: ParamCleaner.method_name1}