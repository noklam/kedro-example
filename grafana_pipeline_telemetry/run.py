

# https://hub.docker.com/r/statsd/statsd
from statsd import StatsClient
client = StatsClient('localhost',8125)

pipe = client.pipeline()
pipe.incr('Nok')
pipe.decr('Nok')
pipe.timing('baz', 520)
pipe.send()