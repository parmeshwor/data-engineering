"""

if you go to google or bing, and start typing it will suggest lot of similar and relevant result in the
autocomplete

constraint : no spell check, no locale information, no personalized suggestion , only english

# Trie is the answer .
# With Autocomplete we should atleast think of two conditions,
  1. request flow : get a request ; look into the tire ; get a bunch of results and send it back to the user
  2. data collection  : get a list of string from back ground process and take strings ; aggregate and apply to Trie


Design request path :
api :
get: prefix -> return :list of autocomplete words for the prefix

# store top k terms for every node ;

# There are millions of different sentences so trie can be really use, so using a single node is neither durable
nor scalable

# distribute trie into multiple machines.

Client

request

load balancer
(can be round robin or least connections)

Zookeeper
[ a-$-> T1, T2, T3]     a-e   f-p    q-z   ==> zookeeper has this information
                        N1     N2    N3 => zookeeper nodes

N1 ; looks in distributed cache; if it is not there, consult zookeeper for which Trie to go.
     zookeeper can direct to T2. gets result from T2 and returns the result to user;
     then populate the result to distributed cache.

[Distributed cache]   T1   T2   T3    => Trie ( 3 Nodes with same replica) ; for availability

What happens data does not fit in single Trie ?
Split data across multiple nodes.
change in design is for each chunk of data zookeeper can direct to specific Trie


Zookeeper [ a-k => T1, T2 T3
            K=z => T4 t5 t6 ]

Trie  :          T1 t2 t3
(replication )   t4 t5 t6




Data collection Technique/ Data Collection Flow :

collection flow has api that gets ; phrase and weight



[ Distributed aggregators; route data to aggregators by hashing etc to send same phrase to same aggregator for aggregation)
send data to aggregators for a certain period of time, and flush that information to database.

schema

[ Phrase Time  Sumofweights ]

Aggregarte all the hourly data and create daily data

if weight is less than threshold we can get rid of that word.

granularity is by hour
sort data by weight ; fresh result can be given more weight
optiimization ; get rid of old data ; get rid of data with weight less than threshold.

recent data can be given more weight; so that sorting by weight with time attached helps;
so that algorithm can choose data based on time and sum of weights.



Appliers get data from database and apply them to Trie; they can run every 1 hour and work on their respective range [ a-k, k-z etc]

Build trie in appliers with top k data for each node and write that to Trie.
We have appliers, builds tire with fresh data and take that trie and dump it to T1, T2 T3....


2 optimiizations : if user is searching for seattle; CDN in seattle can help
search for `ba` we can return for bat etc etc so that use dont have to type that. recursively go to next level etc etc.



"""