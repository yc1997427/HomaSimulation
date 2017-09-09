import threading
import os
import Queue
import time 

def worker():
	while True:
		try:
			j = q.get(block = 0)
		except Queue.Empty:
			return
		#Make directory to save results
		os.system('mkdir -p '+j[1])
		os.system(j[0])

q = Queue.Queue()

sim_end = 100000
link_rate = 10
mean_link_delay = 0.000000250
host_delay = 0.0000005
queueSize = 240
#load_arr = [0.9, 0.8, 0.7, 0.6, 0.5]
load_arr = [0.8, 0.5]
connections_per_pair = 10
meanFlowSize = 1745 * 1460 
gptp_ratio = 2547262.0/2686844.0 # ratio of goodput over throughput. Throughput
                                 # will include pkt headers and acks
paretoShape = 1
flow_cdf = 'CDF_search.tcl'

enableMultiPath = 1
perflowMP = 0

sourceAlg = 'DCTCP-Sack'
#sourceAlg='LLDCT-Sack'
initWindow = 70
ackRatio = 1
slowstartrestart = 'true'
DCTCP_g = 0.0625
min_rto = 0.002
prob_cap_ = 5

switchAlg = 'Priority'
DCTCP_K = 65.0
drop_prio_ = 'true'
prio_scheme_ = 2
deque_prio_ = 'true'
keep_order_ = 'true'
prio_num_arr = [8]
ECN_scheme_ = 2 #Per-port ECN marking
#pias_thresh_0 = [759*1460 , 909*1460 , 999*1460 , 956*1460 , 1059*1460]
#pias_thresh_1 = [1132*1460, 1329*1460, 1305*1460, 1381*1460, 1412*1460]
#pias_thresh_2 = [1456*1460, 1648*1460, 1564*1460, 1718*1460, 1643*1460]
#pias_thresh_3 = [1737*1460, 1960*1460, 1763*1460, 2028*1460, 1869*1460]
#pias_thresh_4 = [2010*1460, 2143*1460, 1956*1460, 2297*1460, 2008*1460]
#pias_thresh_5 = [2199*1460, 2337*1460, 2149*1460, 2551*1460, 2115*1460]
#pias_thresh_6 = [2325*1460, 2484*1460, 2309*1460, 2660*1460, 2184*1460]

pias_thresh_0 = [909*1460 , 1059*1460]
pias_thresh_1 = [1329*1460, 1412*1460]
pias_thresh_2 = [1648*1460, 1643*1460]
pias_thresh_3 = [1960*1460, 1869*1460]
pias_thresh_4 = [2143*1460, 2008*1460]
pias_thresh_5 = [2337*1460, 2115*1460]
pias_thresh_6 = [2484*1460, 2184*1460]

topology_spt = 16
topology_tors = 9
topology_spines = 4
topology_x = 1

ns_path = '/home/neverhood/Research/RpcTransportDesign/'\
    'ns2_Simulations/ns-allinone-2.34/bin/ns'
sim_script = 'search_pias.tcl'

for prio_num_ in prio_num_arr:
	for i in range(len(load_arr)):

		scheme = 'unknown'
		if switchAlg == 'Priority' and prio_num_ > 1 and\
                            sourceAlg == 'DCTCP-Sack':
			scheme = 'pias'
		elif switchAlg == 'Priority' and prio_num_ == 1:
			if sourceAlg == 'DCTCP-Sack':
				scheme = 'dctcp'
			elif sourceAlg == 'LLDCT-Sack':
				scheme = 'lldct'

		if scheme == 'unknown':
			print 'Unknown scheme'
			sys.exit(0)

		#Directory name: workload_scheme_load_[load]
		directory_name = 'search_%s_%d' % (scheme,int(load_arr[i]*100))
		directory_name = directory_name.lower()
                localtime = time.localtime()
                directory_name = 'traces'+ '/' + '%.4d%.2d%.2d_%.2d%.2d' % (
                    localtime.tm_year, localtime.tm_mon, localtime.tm_mday, 
                    localtime.tm_hour,localtime.tm_min) + '/' + directory_name

		#Simulation command
		cmd = ns_path+' '+sim_script+' '\
			+str(sim_end)+' '\
			+str(link_rate)+' '\
			+str(mean_link_delay)+' '\
			+str(host_delay)+' '\
			+str(queueSize)+' '\
			+str(load_arr[i])+' '\
			+str(connections_per_pair)+' '\
			+str(meanFlowSize)+' '\
			+str(gptp_ratio)+' '\
			+str(paretoShape)+' '\
			+str(flow_cdf)+' '\
			+str(enableMultiPath)+' '\
			+str(perflowMP)+' '\
			+str(sourceAlg)+' '\
			+str(initWindow)+' '\
			+str(ackRatio)+' '\
			+str(slowstartrestart)+' '\
			+str(DCTCP_g)+' '\
			+str(min_rto)+' '\
			+str(prob_cap_)+' '\
			+str(switchAlg)+' '\
			+str(DCTCP_K)+' '\
			+str(drop_prio_)+' '\
			+str(prio_scheme_)+' '\
			+str(deque_prio_)+' '\
			+str(keep_order_)+' '\
			+str(prio_num_)+' '\
			+str(ECN_scheme_)+' '\
			+str(pias_thresh_0[i])+' '\
			+str(pias_thresh_1[i])+' '\
			+str(pias_thresh_2[i])+' '\
			+str(pias_thresh_3[i])+' '\
			+str(pias_thresh_4[i])+' '\
			+str(pias_thresh_5[i])+' '\
			+str(pias_thresh_6[i])+' '\
			+str(topology_spt)+' '\
			+str(topology_tors)+' '\
			+str(topology_spines)+' '\
			+str(topology_x)+' '\
			+str('./'+directory_name+'/flow.tr')+'  >'\
			+str('./'+directory_name+'/logFile.tr')
                print cmd
		q.put([cmd, directory_name])

#Create all worker threads
threads = []
number_worker_threads = 4

#Start threads to process jobs
for i in range(number_worker_threads):
	t = threading.Thread(target = worker)
	threads.append(t)
	t.start()

#Join all completed threads
for t in threads:
	t.join()