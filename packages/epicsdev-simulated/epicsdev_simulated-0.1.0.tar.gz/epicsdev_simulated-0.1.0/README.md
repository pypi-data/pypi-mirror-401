# epicsdev_simulated
EPICS PVAccess servers for simulated devices

Start: ```python -m epicsdev_simulated.simscope -l```<br.
Access:<br>
```
python -m p4p.client.cli get simScope1:cycle
python -m p4p.client.cli monitor simScope1:WaveForm_RBV
```
Plot: ```python -m pvplot -a'V:simScope1:' WaveForm_RBV```
