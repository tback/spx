# SPX

Unofficial Edimax Smartplug Libary.



## Usage as a Library

```
import spx

p = spx.SmartPlug('ip_or_hostname')
p.set_state(bool)
p.switch(bool)  # alias for set_state(bool)
p.on()  # alias for set_state(True)
p.off() # alias for set_state(False)
p.get_usage()  # SP-2101W only
p.monitor() #SP-2101W only
#as a convenience all commands are available as functions as well:
spx.on('ip_or_hostname') etc.
```

## Usage of spx.tool
```
$ python -m spx.tool --help
# or
$ spx-tool --help
```
