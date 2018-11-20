import geocoder



g = geocoder.google([45.15, -75.14], method='reverse')
print (g.city)
print (g.state)
print(g.state_long)
g.country
g.country_long



# import module_manager
# module_manager.review()
# 
# 
# #got conda, got rtree, network x, osmnx, requests
# 
# 
# #import networkx as nx
# import osmnx as ox
# #import requests
# # import matplotlib.cm as cm
# # import matplotlib.colors as colors
# # ox.config(use_cache=True, log_console=True)
# # ox.__version__
