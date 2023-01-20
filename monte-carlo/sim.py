import pandas as pd
import time
import math
import random
random.seed(42)
from matplotlib import pyplot as plt
starttime=time.time()


def rand(minimum, maximum):
    randomPercent=random.random()    
    return minimum+randomPercent*(maximum-minimum)


def rand_params(params) :
    for i in range(len(params)):
        params.loc[i,'v']=rand(params['min'][i],params['max'][i])
    
    params=params.T
    params.columns=params.loc['param']
    sim=params.drop('param')
    return sim

def run_sim(sim):
    results=[]
    breaking_time=sim.daily_kg.v/sim.num_rovers.v/sim.breaking_rate.v*3600
    loading_time=sim.daily_kg.v/sim.num_rovers.v/sim.loading_rate.v*3600
    loaded_mass=sim.payload_capacity.v-sim.excavation_mass.v-sim.bucket_mass.v
    num_trips=round(sim.daily_kg.v/loaded_mass+0.5,0)/sim.num_rovers.v
    one_way_distance=num_trips*sim.distance_traveled.v
    loaded_travel_time=one_way_distance/sim.loaded_speed.v
    unloaded_travel_time=one_way_distance/sim.loaded_speed.v #using loaded speed for similiarity
    loading_time=sim.daily_kg.v/sim.num_rovers.v/sim.loading_rate.v*3600
    unloading_time=sim.daily_kg.v/sim.num_rovers.v/sim.unloading_rate.v*3600
    power_used=(breaking_time*sim.breaking_power.v+\
        (loaded_travel_time+unloaded_travel_time)*sim.moving_power.v+\
            (loading_time+unloading_time)*sim.loading_power.v+\
                3600*24*sim.base_power.v)
    charging_time=power_used/sim.charging_power.v
    total_time=(breaking_time+\
        loading_time+unloading_time+\
            loaded_travel_time+unloaded_travel_time+\
                charging_time)/3600
        
    variables=['breaking_time', 'loaded_mass', 'num_trips', \
               'one_way_distance', 'loaded_travel_time', 'unloaded_travel_time',\
                   'loading_time', 'unloading_time', 'power_used','charging_time', 'total_time']
    for var in variables:
        results.append(eval(var))
    return results, variables






file='input-params.csv'
params=pd.read_csv(file)

result_cat=[]
for i in range(1000):
    sim=rand_params(params)
    results, variables=run_sim(sim)
    sim_list=sim.loc['v'].tolist()
    result_cat.append(sim_list+results)
sim_cols=sim.columns.tolist()
df=pd.DataFrame(result_cat, columns=sim_cols+variables)

endtime=time.time()
print('Runtime: {} seconds'.format(int(endtime-starttime)))


######################################################

def plot_scatter(x_vars, y_var, df, sim):
    fig, axs = plt.subplots(1, len(x_vars), figsize=(20,6), sharey=True)
    for i,var in enumerate(x_vars):
        axs[i].scatter(df[var], df[y_var])
        axs[i].set_title(var)
        axs[i].set_xlabel(eval('sim.'+var+'.units'))
    axs[0].set_ylabel(y_var +' hrs')
    return


plot_scatter(['breaking_rate', 'loading_rate', 'loaded_speed',\
              'bucket_mass', 'excavation_mass', 'payload_capacity'],\
             'total_time',\
                 df, sim)

