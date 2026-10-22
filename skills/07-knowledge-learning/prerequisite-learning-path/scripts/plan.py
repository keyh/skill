#!/usr/bin/env python3
"""Plan prerequisites from user-supplied data; stdlib only, no network."""
import argparse, heapq, json, sys
from pathlib import Path

def plan(graph, targets, mastered=()):
    nodes={}
    for n in graph['nodes']:
        i=n['id']
        if not isinstance(i,str) or not i or i in nodes:raise ValueError('Invalid or duplicate node ID')
        if not isinstance(n.get('prerequisites',[]),list) or not all(isinstance(x,str) for x in n.get('prerequisites',[])):raise ValueError('Prerequisites must be ID list')
        nodes[i]=n
    if len(nodes)>10000:raise ValueError('Use a graph of at most 10000 nodes')
    if not targets:raise ValueError('At least one target required')
    unknown=(set(targets)|set(mastered))-nodes.keys()
    if unknown:raise ValueError('Unknown target/mastery: '+','.join(sorted(unknown)))
    parents={i:set(n.get('prerequisites',[])) for i,n in nodes.items()}
    for i,ps in parents.items():
        if ps-nodes.keys():raise ValueError('Missing prerequisite for '+i+': '+','.join(sorted(ps-nodes.keys())))
    children={i:set() for i in nodes};degrees={i:len(ps) for i,ps in parents.items()}
    for i,ps in parents.items():
        for p in ps:children[p].add(i)
    ready=[i for i,d in degrees.items() if d==0];heapq.heapify(ready);order=[]
    while ready:
        i=heapq.heappop(ready);order.append(i)
        for child in sorted(children[i]):
            degrees[child]-=1
            if degrees[child]==0:heapq.heappush(ready,child)
    if len(order)!=len(nodes):raise ValueError('Cycle detected: '+','.join(i for i,d in degrees.items() if d))
    needed=set();todo=list(targets)
    while todo:
        i=todo.pop()
        if i not in needed:needed.add(i);todo.extend(parents[i])
    known=set(mastered)
    missing=[{'id':i,'title':nodes[i].get('title',i),'prerequisites':sorted(parents[i]),'evidence':nodes[i].get('evidence','未提供来源')} for i in order if i in needed-known]
    warnings=[{'id':i,'unconfirmed_prerequisites':sorted(parents[i]-known)} for i in sorted(known&needed) if parents[i]-known]
    return {'targets':sorted(set(targets)),'mastered':sorted(known),'ordered_missing':missing,'mastery_warnings':warnings,'structural_validation':'passed','pedagogical_validation':'not assessed by this script'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('graph');ap.add_argument('--target',required=True);ap.add_argument('--mastered',default='');a=ap.parse_args()
    try:
        result=plan(json.loads(Path(a.graph).read_text()),a.target.split(','),[x for x in a.mastered.split(',') if x])
    except (ValueError,KeyError,TypeError) as e:
        print(str(e),file=sys.stderr);return 2
    print(json.dumps(result,ensure_ascii=False,indent=2));return 0
if __name__=='__main__':sys.exit(main())
